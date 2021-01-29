from app import db
from exception import ForbiddenException
from exception.messages import MESSAGE_CODE_PCE_42_CANNOT_BE_PROCESSED_WITHOUT_PCE_R2
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021 import TALLY_SHEET_CODES
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.TEMPLATE_ROW_TYPE import \
    TEMPLATE_ROW_TYPE_SEATS_ALLOCATED, TEMPLATE_ROW_TYPE_ELECTED_CANDIDATE, TEMPLATE_ROW_TYPE_DRAFT_ELECTED_CANDIDATE
from ext.ExtendedTallySheet import ExtendedEditableTallySheetReport
from orm.entities.Meta import MetaData
from orm.entities.TallySheet import TallySheetTallySheetModel
from orm.entities.Template import TemplateRowModel, TemplateModel
import math

from flask import render_template
import re
from orm.entities import Area, Template, TallySheet
from orm.entities.Workflow import WorkflowInstance
from orm.enums import AreaTypeEnum
from util import convert_image_to_data_uri


class ExtendedTallySheet_PCE_42(ExtendedEditableTallySheetReport):

    def get_template_column_to_query_filter_map(self, only_group_by_columns=False):
        extended_election = self.tallySheet.election.get_extended_election()

        template_column_to_query_filter_map = super(
            ExtendedTallySheet_PCE_42, self).get_template_column_to_query_filter_map(
            only_group_by_columns=only_group_by_columns)
        template_column_to_query_column_map = self.get_template_column_to_query_column_map()

        party_ids_to_be_filtered = []
        pce_r2_tally_sheets = db.session.query(TallySheet.Model).filter(
            TallySheet.Model.tallySheetId == TallySheetTallySheetModel.childTallySheetId,
            TallySheet.Model.latestVersionId != None,
            TallySheetTallySheetModel.parentTallySheetId == self.tallySheet.tallySheetId,
            TallySheet.Model.templateId == Template.Model.templateId,
            Template.Model.templateName == TALLY_SHEET_CODES.PCE_R2,
            WorkflowInstance.Model.workflowInstanceId == TallySheet.Model.workflowInstanceId,
            WorkflowInstance.Model.status.in_(
                extended_election.tally_sheet_verified_statuses_list()
            ),
        ).all()

        if len(pce_r2_tally_sheets) == 0:
            raise ForbiddenException(
                message="PCE-42 cannot be processed before PCE-R2 is completed and verified.",
                code=MESSAGE_CODE_PCE_42_CANNOT_BE_PROCESSED_WITHOUT_PCE_R2
            )

        pce_r2_tally_sheet_ids = [tallySheet.tallySheetId for tallySheet in pce_r2_tally_sheets]

        for pce_r2_tally_sheet in pce_r2_tally_sheets:
            pe_r2_extended_tally_sheet_version = pce_r2_tally_sheet.get_extended_tally_sheet_version(
                tallySheetVersionId=pce_r2_tally_sheet.latestVersionId)
            party_wise_seat_calculation_df = pe_r2_extended_tally_sheet_version.get_party_wise_seat_calculations()
            for party_wise_seat_calculation_df_index in party_wise_seat_calculation_df.index:
                seats_allocated = party_wise_seat_calculation_df.at[
                    party_wise_seat_calculation_df_index, 'seatsAllocated']

                if seats_allocated > 0:
                    party_id = party_wise_seat_calculation_df.at[party_wise_seat_calculation_df_index, 'partyId']
                    party_ids_to_be_filtered.append(int(party_id))

        pe_ce_ro_pr_3_tally_sheets = db.session.query(
            TallySheet.Model.tallySheetId
        ).filter(
            TallySheet.Model.tallySheetId == TallySheetTallySheetModel.childTallySheetId,
            TallySheetTallySheetModel.parentTallySheetId == self.tallySheet.tallySheetId,
            TallySheet.Model.templateId == Template.Model.templateId,
            Template.Model.templateName == TALLY_SHEET_CODES.PCE_CE_RO_PR_3,
            MetaData.Model.metaId == TallySheet.Model.metaId,
            MetaData.Model.metaDataKey == "partyId",
            MetaData.Model.metaDataValue.in_(party_ids_to_be_filtered)
        ).all()
        pe_ce_ro_pr_3_tally_sheet_ids = [tallySheet.tallySheetId for tallySheet in pe_ce_ro_pr_3_tally_sheets]

        template_column_to_query_filter_map["partyId"] += [
            template_column_to_query_column_map["partyId"].in_(party_ids_to_be_filtered),
            TallySheet.Model.tallySheetId.in_(pe_ce_ro_pr_3_tally_sheet_ids + pce_r2_tally_sheet_ids)
        ]

        return template_column_to_query_filter_map

    def on_get_release_result_params(self):
        pd_code = None
        pd_name = None

        administrative_district = self.tallySheet.area
        ed_name_regex_search = re.match('([0-9a-zA-Z]*) *- *(.*)', administrative_district.areaName)
        ed_code = ed_name_regex_search.group(1)
        ed_name = ed_name_regex_search.group(2)

        result_type = "RE_SC"
        result_code = ed_code
        result_level = "ADMINISTRATIVE-DISTRICT"

        return result_type, result_code, result_level, ed_code, ed_name, pd_code, pd_name

    class ExtendedTallySheetVersion(ExtendedEditableTallySheetReport.ExtendedTallySheetVersion):
        def json(self):
            extended_tally_sheet = self.tallySheet.get_extended_tally_sheet()
            result_type, result_code, result_level, ed_code, ed_name, pd_code, pd_name = extended_tally_sheet.on_get_release_result_params()

            candidate_wise_results = self.get_candidate_wise_results().sort_values(
                by=['electionPartyId', "candidateId"], ascending=[True, True]
            ).reset_index()

            return {
                "type": result_type,
                "level": result_level,
                "ed_code": ed_code,
                "ed_name": ed_name,
                "by_candidate": [
                    {
                        "party_code": candidate_wise_result.partyAbbreviation,
                        "party_name": candidate_wise_result.partyName,
                        "candidate_number": str(candidate_wise_result.candidateNumber),
                        "candidate_name": candidate_wise_result.candidateName,
                        "candidate_type": candidate_wise_result.candidateType
                    } for candidate_wise_result in candidate_wise_results.itertuples()
                ]
            }

        def get_candidate_wise_results(self):

            candidate_wise_results_df = self.df.loc[
                (self.df['templateRowType'] == TEMPLATE_ROW_TYPE_ELECTED_CANDIDATE) & (self.df['numValue'] == 0)]

            candidate_wise_results_df["seatsAllocated"] = [0 for i in range(len(candidate_wise_results_df))]
            candidate_wise_results_df["preferenceCount"] = [0 for i in range(len(candidate_wise_results_df))]

            for index in candidate_wise_results_df.index:
                party_id = candidate_wise_results_df.at[index, "partyId"]
                candidate_id = candidate_wise_results_df.at[index, "candidateId"]

                seats_allocated = self.df.loc[(self.df["partyId"] == party_id) & (
                            self.df['templateRowType'] == TEMPLATE_ROW_TYPE_SEATS_ALLOCATED)]["numValue"].values[0]

                preference_count = self.df.loc[(self.df["candidateId"] == candidate_id) & (
                            self.df['templateRowType'] == "CANDIDATE_FIRST_PREFERENCE")]["numValue"].values[0]

                candidate_wise_results_df.at[index, "seatsAllocated"] = seats_allocated
                candidate_wise_results_df.at[index, "preferenceCount"] = preference_count

            candidate_wise_results_df = candidate_wise_results_df.sort_values(
                by=["seatsAllocated", "electionPartyId", "preferenceCount", "candidateId"],
                ascending=[False, True, False, True]
            )

            return candidate_wise_results_df

        def get_post_save_request_content(self):
            tally_sheet_id = self.tallySheetVersion.tallySheetId

            template_rows = db.session.query(
                TemplateRowModel.templateRowId,
                TemplateRowModel.templateRowType
            ).filter(
                TemplateModel.templateId == TallySheet.Model.templateId,
                TemplateRowModel.templateId == TemplateModel.templateId,
                TemplateRowModel.templateRowType.in_([
                    TEMPLATE_ROW_TYPE_ELECTED_CANDIDATE, TEMPLATE_ROW_TYPE_DRAFT_ELECTED_CANDIDATE
                ]),
                TallySheet.Model.tallySheetId == tally_sheet_id
            ).group_by(
                TemplateRowModel.templateRowId
            ).all()

            content = []

            seats_allocated_per_party_df = self.df.loc[
                (self.df['templateRowType'] == TEMPLATE_ROW_TYPE_SEATS_ALLOCATED) & (self.df['numValue'] > 0)]

            # The derived rows are calculated only if the PCE-R2 is available and verified.
            if len(seats_allocated_per_party_df) > 0:
                candidate_wise_valid_vote_count_result = self.get_candidate_wise_valid_vote_count_result().sort_values(
                    by=['numValue'], ascending=False
                )
                for index_1 in seats_allocated_per_party_df.index:
                    party_id = seats_allocated_per_party_df.at[index_1, "partyId"]
                    number_of_seats_allocated = seats_allocated_per_party_df.at[index_1, "numValue"]

                    if number_of_seats_allocated is not None and not math.isnan(number_of_seats_allocated):
                        filtered_candidate_wise_valid_vote_count_result = candidate_wise_valid_vote_count_result.loc[
                            candidate_wise_valid_vote_count_result["partyId"] == party_id]
                        for index_2 in filtered_candidate_wise_valid_vote_count_result.index:
                            if number_of_seats_allocated > 0:
                                for template_row in template_rows:
                                    num_value = filtered_candidate_wise_valid_vote_count_result.at[
                                        index_2, "incompleteNumValue"]
                                    candidate_id = filtered_candidate_wise_valid_vote_count_result.at[
                                        index_2, "candidateId"]
                                    if not math.isnan(num_value):
                                        content.append({
                                            "templateRowId": template_row.templateRowId,
                                            "templateRowType": template_row.templateRowType,
                                            "partyId": int(party_id),
                                            "candidateId": int(candidate_id),

                                            # TODO remove once the complete validation has been fixed.
                                            "numValue": 0
                                        })
                                    else:
                                        content.append({
                                            "templateRowId": template_row.templateRowId,
                                            "templateRowType": template_row.templateRowType,
                                            "partyId": int(party_id),
                                            "candidateId": None,

                                            # TODO remove once the complete validation has been fixed.
                                            "numValue": 0
                                        })

                                number_of_seats_allocated -= 1

            return content

        def html(self, title="", total_registered_voters=None):
            tallySheetVersion = self.tallySheetVersion

            stamp = tallySheetVersion.stamp

            content = {
                "election": {
                    "electionName": tallySheetVersion.tallySheet.election.get_official_name()
                },
                "stamp": {
                    "createdAt": stamp.createdAt,
                    "createdBy": stamp.createdBy,
                    "barcodeString": stamp.barcodeString
                },
                "tallySheetCode": "PCE-21",
                "provinceNo": Area.get_associated_areas(
                    tallySheetVersion.tallySheet.area, AreaTypeEnum.Province)[0].areaId,
                "province": Area.get_associated_areas(
                    tallySheetVersion.tallySheet.area, AreaTypeEnum.Province)[0].areaName,
                "administrativeDistrictNo": Area.get_associated_areas(
                    tallySheetVersion.tallySheet.area, AreaTypeEnum.AdministrativeDistrict)[0].areaId,
                "administrativeDistrict": Area.get_associated_areas(
                    tallySheetVersion.tallySheet.area, AreaTypeEnum.AdministrativeDistrict)[0].areaName,
                "countingCentre": tallySheetVersion.tallySheet.area.areaName,
                "data": []
            }

            candidate_wise_results = self.get_candidate_wise_results().sort_values(
                by=["seatsAllocated", "electionPartyId", "preferenceCount", "candidateId"],
                ascending=[False, True, False, True]
            ).reset_index()

            for index in candidate_wise_results.index:
                candidate_name = candidate_wise_results.at[index, "candidateName"]
                party_name = candidate_wise_results.at[index, "partyName"]
                content["data"].append({
                    "candidateName": "" if candidate_name is None else candidate_name,
                    "partyName": party_name
                })

            html = render_template(
                'ProvincialCouncilElection2021/PCE-42.html',
                content=content
            )

            return html

        def html_letter(self, title="", total_registered_voters=None, signatures=[]):
            tallySheetVersion = self.tallySheetVersion
            stamp = tallySheetVersion.stamp

            content = {
                "election": {
                    "electionName": tallySheetVersion.tallySheet.election.get_official_name()
                },
                "stamp": {
                    "createdAt": stamp.createdAt,
                    "createdBy": stamp.createdBy,
                    "barcodeString": stamp.barcodeString
                },
                "signatures": signatures,
                "province": Area.get_associated_areas(
                    tallySheetVersion.tallySheet.area, AreaTypeEnum.Province)[0].areaName,
                "administrativeDistrict": Area.get_associated_areas(
                    tallySheetVersion.tallySheet.area, AreaTypeEnum.AdministrativeDistrict)[0].areaName,
                "data": [],
                "logo": convert_image_to_data_uri("static/Emblem_of_Sri_Lanka.png"),
                "date": stamp.createdAt.strftime("%d/%m/%Y"),
                "time": stamp.createdAt.strftime("%H:%M:%S %p")
            }

            candidate_wise_results = self.get_candidate_wise_results().sort_values(
                by=["seatsAllocated", "electionPartyId", "preferenceCount", "candidateId"],
                ascending=[False, True, False, True]
            ).reset_index()

            for index in candidate_wise_results.index:
                data_row = [
                    candidate_wise_results.at[index, "partyName"],
                    candidate_wise_results.at[index, "partyAbbreviation"],
                    candidate_wise_results.at[index, "candidateNumber"],
                    candidate_wise_results.at[index, "candidateName"]
                ]

                content["data"].append(data_row)

            html = render_template(
                'ProvincialCouncilElection2021/PCE-42-LETTER.html',
                content=content
            )

            return html
