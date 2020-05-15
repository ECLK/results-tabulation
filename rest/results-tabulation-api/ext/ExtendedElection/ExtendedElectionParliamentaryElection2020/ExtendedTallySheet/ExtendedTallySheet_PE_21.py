from app import db
from exception import ForbiddenException
from exception.messages import MESSAGE_CODE_PE_21_CANNOT_BE_PROCESSED_WITHOUT_PE_R2
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020 import TALLY_SHEET_CODES
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.TEMPLATE_ROW_TYPE import \
    TEMPLATE_ROW_TYPE_SEATS_ALLOCATED, TEMPLATE_ROW_TYPE_ELECTED_CANDIDATE, TEMPLATE_ROW_TYPE_DRAFT_ELECTED_CANDIDATE
from ext.ExtendedTallySheet import ExtendedEditableTallySheetReport
from orm.entities.Meta import MetaData
from orm.entities.Submission import TallySheet
from orm.entities.Submission.TallySheet import TallySheetTallySheetModel
from orm.entities.Template import TemplateRowModel, TemplateModel
import math

from flask import render_template
from orm.entities import Area, Template, Submission
from orm.entities.Workflow import WorkflowInstance
from orm.enums import AreaTypeEnum


class ExtendedTallySheet_PE_21(ExtendedEditableTallySheetReport):

    def get_template_column_to_query_filter_map(self, only_group_by_columns=False):
        extended_election = self.tallySheet.election.get_extended_election()

        template_column_to_query_filter_map = super(
            ExtendedTallySheet_PE_21, self).get_template_column_to_query_filter_map(
            only_group_by_columns=only_group_by_columns)
        template_column_to_query_column_map = self.get_template_column_to_query_column_map()

        party_ids_to_be_filtered = []
        pe_r2_tally_sheets = db.session.query(TallySheet.Model).filter(
            TallySheet.Model.tallySheetId == TallySheetTallySheetModel.childTallySheetId,
            TallySheet.Model.tallySheetId == Submission.Model.submissionId,
            Submission.Model.latestVersionId != None,
            TallySheetTallySheetModel.parentTallySheetId == self.tallySheet.tallySheetId,
            TallySheet.Model.templateId == Template.Model.templateId,
            Template.Model.templateName == TALLY_SHEET_CODES.PE_R2,
            WorkflowInstance.Model.workflowInstanceId == TallySheet.Model.workflowInstanceId,
            WorkflowInstance.Model.status.in_(
                extended_election.tally_sheet_verified_statuses_list()
            ),
        ).all()

        if len(pe_r2_tally_sheets) == 0:
            raise ForbiddenException(
                message="Candidates cannot be allocated until the seat calculation (PE-R2) is completed and verified.",
                code=MESSAGE_CODE_PE_21_CANNOT_BE_PROCESSED_WITHOUT_PE_R2
            )

        pe_r2_tally_sheet_ids = [tallySheet.tallySheetId for tallySheet in pe_r2_tally_sheets]

        for pe_r2_tally_sheet in pe_r2_tally_sheets:
            pe_r2_extended_tally_sheet_version = pe_r2_tally_sheet.get_extended_tally_sheet_version(
                tallySheetVersionId=pe_r2_tally_sheet.latestVersionId)
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
            Template.Model.templateName == TALLY_SHEET_CODES.PE_CE_RO_PR_3,
            MetaData.Model.metaId == TallySheet.Model.metaId,
            MetaData.Model.metaDataKey == "partyId",
            MetaData.Model.metaDataValue.in_(party_ids_to_be_filtered)
        ).all()
        pe_ce_ro_pr_3_tally_sheet_ids = [tallySheet.tallySheetId for tallySheet in pe_ce_ro_pr_3_tally_sheets]

        template_column_to_query_filter_map["partyId"] += [
            template_column_to_query_column_map["partyId"].in_(party_ids_to_be_filtered),
            TallySheet.Model.tallySheetId.in_(pe_ce_ro_pr_3_tally_sheet_ids + pe_r2_tally_sheet_ids)
        ]

        return template_column_to_query_filter_map

    class ExtendedTallySheetVersion(ExtendedEditableTallySheetReport.ExtendedTallySheetVersion):

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

            seats_allocated_per_party_df = self.df.loc[self.df['templateRowType'] == TEMPLATE_ROW_TYPE_SEATS_ALLOCATED]

            # The derived rows are calculated only if the PE-R2 is available and verified.
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

        def html_letter(self, title="", total_registered_voters=None):
            return self.html(title=title, total_registered_voters=total_registered_voters)

        def html(self, title="", total_registered_voters=None):
            tallySheetVersion = self.tallySheetVersion

            stamp = tallySheetVersion.stamp

            content = {
                "election": {
                    "electionName": tallySheetVersion.submission.election.get_official_name()
                },
                "stamp": {
                    "createdAt": stamp.createdAt,
                    "createdBy": stamp.createdBy,
                    "barcodeString": stamp.barcodeString
                },
                "tallySheetCode": "PE-21",
                "electoralDistrictNo": Area.get_associated_areas(
                    tallySheetVersion.submission.area, AreaTypeEnum.ElectoralDistrict)[0].areaId,
                "electoralDistrict": Area.get_associated_areas(
                    tallySheetVersion.submission.area, AreaTypeEnum.ElectoralDistrict)[0].areaName,
                "countingCentre": tallySheetVersion.submission.area.areaName,
                "data": []
            }

            elected_candidates_df = self.df.loc[self.df['templateRowType'] == TEMPLATE_ROW_TYPE_ELECTED_CANDIDATE]

            for index in elected_candidates_df.index:
                candidate_name = elected_candidates_df.at[index, "candidateName"]
                party_name = elected_candidates_df.at[index, "partyName"]
                content["data"].append({
                    "candidateName": "" if candidate_name is None else candidate_name,
                    "partyName": party_name
                })

            html = render_template(
                'PE-21.html',
                content=content
            )

            return html
