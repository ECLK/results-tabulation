from app import db

from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.TEMPLATE_ROW_TYPE import \
    TEMPLATE_ROW_TYPE_SEATS_ALLOCATED, TEMPLATE_ROW_TYPE_ELECTED_CANDIDATE, TEMPLATE_ROW_TYPE_DRAFT_ELECTED_CANDIDATE
from ext.ExtendedTallySheet import ExtendedEditableTallySheetReport
from orm.entities.Election.ElectionCandidate import ElectionCandidateModel
from orm.entities.Submission import TallySheet
from orm.entities.Template import TemplateRowModel, TemplateModel
import math

from flask import render_template
from orm.entities import Area, Candidate
from orm.enums import AreaTypeEnum
from util import convert_image_to_data_uri


class ExtendedTallySheet_PE_AI_NL_2(ExtendedEditableTallySheetReport):
    # def get_template_column_to_query_filter_map(self, only_group_by_columns=False):
    #     extended_election = self.tallySheet.election.get_extended_election()
    #
    #     template_column_to_query_filter_map = super(
    #         ExtendedTallySheet_PE_AI_NL_2, self).get_template_column_to_query_filter_map(
    #         only_group_by_columns=only_group_by_columns)
    #     template_column_to_query_column_map = self.get_template_column_to_query_column_map()
    #
    #     party_ids_to_be_filtered = []
    #     pe_ai_nl_1_tally_sheets = db.session.query(TallySheet.Model).filter(
    #         TallySheet.Model.tallySheetId == TallySheetTallySheetModel.childTallySheetId,
    #         TallySheet.Model.tallySheetId == Submission.Model.submissionId,
    #         Submission.Model.latestVersionId != None,
    #         TallySheetTallySheetModel.parentTallySheetId == self.tallySheet.tallySheetId,
    #         TallySheet.Model.templateId == Template.Model.templateId,
    #         Template.Model.templateName == TALLY_SHEET_CODES.PE_AI_NL_1,
    #         WorkflowInstance.Model.workflowInstanceId == TallySheet.Model.workflowInstanceId,
    #         WorkflowInstance.Model.status.in_(
    #             extended_election.tally_sheet_verified_statuses_list()
    #         ),
    #     ).all()
    #
    #     if len(pe_ai_nl_1_tally_sheets) == 0:
    #         raise ForbiddenException(
    #             message="National list candidates cannot be allocated until the national list seat calculation (PE-AI-NL-1) is completed and verified.",
    #             code=MESSAGE_CODE_PE_21_CANNOT_BE_PROCESSED_WITHOUT_PE_R2
    #         )
    #
    #     pe_ai_nl_1_tally_sheet_ids = [tallySheet.tallySheetId for tallySheet in pe_ai_nl_1_tally_sheets]
    #
    #     for pe_ai_nl_1_tally_sheet in pe_ai_nl_1_tally_sheets:
    #         pe_ai_nl_1_extended_tally_sheet_version = pe_ai_nl_1_tally_sheet.get_extended_tally_sheet_version(
    #             tallySheetVersionId=pe_ai_nl_1_tally_sheet.latestVersionId)
    #         party_wise_seat_calculation_df = pe_ai_nl_1_extended_tally_sheet_version.get_party_wise_seat_calculations()
    #         for party_wise_seat_calculation_df_index in party_wise_seat_calculation_df.index:
    #             seats_allocated = party_wise_seat_calculation_df.at[
    #                 party_wise_seat_calculation_df_index, 'seatsAllocated']
    #
    #             if seats_allocated > 0:
    #                 party_id = party_wise_seat_calculation_df.at[party_wise_seat_calculation_df_index, 'partyId']
    #                 party_ids_to_be_filtered.append(int(party_id))
    #
    #     pe_ce_ro_pr_3_tally_sheets = db.session.query(
    #         TallySheet.Model.tallySheetId
    #     ).filter(
    #         TallySheet.Model.tallySheetId == TallySheetTallySheetModel.childTallySheetId,
    #         TallySheetTallySheetModel.parentTallySheetId == self.tallySheet.tallySheetId,
    #         TallySheet.Model.templateId == Template.Model.templateId,
    #         Template.Model.templateName == TALLY_SHEET_CODES.PE_CE_RO_PR_3,
    #         MetaData.Model.metaId == TallySheet.Model.metaId,
    #         MetaData.Model.metaDataKey == "partyId",
    #         MetaData.Model.metaDataValue.in_(party_ids_to_be_filtered)
    #     ).all()
    #     pe_ce_ro_pr_3_tally_sheet_ids = [tallySheet.tallySheetId for tallySheet in pe_ce_ro_pr_3_tally_sheets]
    #
    #     template_column_to_query_filter_map["partyId"] += [
    #         template_column_to_query_column_map["partyId"].in_(party_ids_to_be_filtered),
    #         TallySheet.Model.tallySheetId.in_(pe_ce_ro_pr_3_tally_sheet_ids + pe_r2_tally_sheet_ids)
    #     ]
    #
    #     return template_column_to_query_filter_map

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
                    TEMPLATE_ROW_TYPE_ELECTED_CANDIDATE,
                    TEMPLATE_ROW_TYPE_DRAFT_ELECTED_CANDIDATE
                ]),
                TallySheet.Model.tallySheetId == tally_sheet_id
            ).group_by(
                TemplateRowModel.templateRowId
            ).all()

            content = []

            seats_allocated_per_party_df = self.df.loc[self.df['templateRowType'] == TEMPLATE_ROW_TYPE_SEATS_ALLOCATED]

            # The derived rows are calculated only if the PE-R2 is available and verified.
            if len(seats_allocated_per_party_df) > 0:
                for index_1 in seats_allocated_per_party_df.index:
                    party_id = int(seats_allocated_per_party_df.at[index_1, "partyId"])
                    number_of_seats_allocated = seats_allocated_per_party_df.at[index_1, "numValue"]
                    print("========== party ", party_id)

                    if number_of_seats_allocated is not None and not math.isnan(number_of_seats_allocated):

                        candidates = db.session.query(Candidate.Model.candidateId).filter(
                            Candidate.Model.candidateId == ElectionCandidateModel.candidateId,
                            ElectionCandidateModel.partyId == party_id
                        ).group_by(Candidate.Model.candidateId).order_by(Candidate.Model.candidateId).all()

                        for candidate in candidates:
                            if number_of_seats_allocated > 0:
                                for template_row in template_rows:
                                    candidate_id = candidate.candidateId
                                    content.append({
                                        "templateRowId": template_row.templateRowId,
                                        "templateRowType": template_row.templateRowType,
                                        "partyId": int(party_id),
                                        "candidateId": int(candidate_id),

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

            elected_candidates_df = self.df.loc[
                self.df['templateRowType'] == TEMPLATE_ROW_TYPE_ELECTED_CANDIDATE]
            elected_candidates_df = elected_candidates_df.sort_values(
                by=['partyId', 'candidateId'], ascending=True
            )

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

        def html_letter(self, title="", total_registered_voters=None):
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
                "electoralDistrict": Area.get_associated_areas(
                    tallySheetVersion.submission.area, AreaTypeEnum.ElectoralDistrict)[0].areaName,
                "data": [],
                "logo": convert_image_to_data_uri("static/Emblem_of_Sri_Lanka.png"),
                "date": stamp.createdAt.strftime("%d/%m/%Y"),
                "time": stamp.createdAt.strftime("%H:%M:%S %p")
            }

            elected_candidates_df = self.df.loc[self.df['templateRowType'] == TEMPLATE_ROW_TYPE_ELECTED_CANDIDATE]

            for index in elected_candidates_df.index:
                candidateId = elected_candidates_df.at[index, "candidateId"]
                preference_count_df = self.df.loc[(self.df['templateRowType'] == "CANDIDATE_FIRST_PREFERENCE") & (
                        self.df['candidateId'] == candidateId)]

                data_row = [
                    elected_candidates_df.at[index, "partyName"],
                    elected_candidates_df.at[index, "partyAbbreviation"],
                    elected_candidates_df.at[index, "candidateName"],
                    elected_candidates_df.at[index, "candidateNumber"]
                ]

                content["data"].append(data_row)

            html = render_template(
                'ParliamentaryElection2020/PE-21-LETTER.html',
                content=content
            )

            return html
