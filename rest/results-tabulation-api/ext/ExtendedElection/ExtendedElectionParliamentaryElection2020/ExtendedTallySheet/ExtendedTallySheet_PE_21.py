from app import db
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.TEMPLATE_ROW_TYPE import \
    TEMPLATE_ROW_TYPE_SEATS_ALLOCATED, TEMPLATE_ROW_TYPE_ELECTED_CANDIDATE
from ext.ExtendedTallySheet import ExtendedTallySheetReport
from orm.entities.Submission import TallySheet
from orm.entities.Template import TemplateRowModel, TemplateModel
import math

from flask import render_template
from ext.ExtendedTallySheet import ExtendedTallySheet
from orm.entities import Area
from constants.VOTE_TYPES import Postal
from util import to_comma_seperated_num
from orm.enums import AreaTypeEnum


class ExtendedTallySheet_PE_21(ExtendedTallySheetReport):
    class ExtendedTallySheetVersion(ExtendedTallySheetReport.ExtendedTallySheetVersion):

        def html_letter(self, title="", total_registered_voters=None):
            return super(ExtendedTallySheet_PE_21.ExtendedTallySheetVersion, self).html_letter(
                title="Results of Electoral District %s" % self.tallySheetVersion.submission.area.areaName
            )

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

            # Appending canditate wise vote count
            tally_sheet_id = self.tallySheetVersion.tallySheetId
            template_rows = db.session.query(
                TemplateRowModel.templateRowId
            ).filter(
                TemplateModel.templateId == TallySheet.Model.templateId,
                TemplateRowModel.templateId == TemplateModel.templateId,
                TemplateRowModel.templateRowType == TEMPLATE_ROW_TYPE_ELECTED_CANDIDATE,
                TallySheet.Model.tallySheetId == tally_sheet_id
            ).group_by(
                TemplateRowModel.templateRowId
            ).all()

            candidate_wise_valid_vote_count_result = self.get_candidate_wise_valid_vote_count_result().sort_values(
                by=['numValue'], ascending=False
            )
            seats_allocated_per_party_df = self.df.loc[self.df['templateRowType'] == TEMPLATE_ROW_TYPE_SEATS_ALLOCATED]
            for index_1 in seats_allocated_per_party_df.index:
                party_id = seats_allocated_per_party_df.at[index_1, "partyId"]
                number_of_seats_allocated = seats_allocated_per_party_df.at[index_1, "numValue"]

                if number_of_seats_allocated is not None and not math.isnan(number_of_seats_allocated):
                    filtered_candidate_wise_valid_vote_count_result = candidate_wise_valid_vote_count_result.loc[
                        candidate_wise_valid_vote_count_result["partyId"] == party_id]
                    for index_2 in filtered_candidate_wise_valid_vote_count_result.index:
                        if number_of_seats_allocated > 0:
                            for template_row in template_rows:
                                num_value = filtered_candidate_wise_valid_vote_count_result.at[index_2, "numValue"]
                                if num_value is not None and not math.isnan(num_value):
                                    content["data"].append({
                                        "partyId": int(party_id),
                                        "candidateId": int(
                                            filtered_candidate_wise_valid_vote_count_result.at[index_2, "candidateId"]),
                                        "candidateName": filtered_candidate_wise_valid_vote_count_result.at[
                                            index_2, "candidateName"],
                                        "partyName": filtered_candidate_wise_valid_vote_count_result.at[
                                            index_2, "partyName"],
                                        "numValue": float(num_value)
                                    })
                                else:
                                    content["data"].append({
                                        "partyId": int(party_id),
                                        "candidateId": int(
                                            filtered_candidate_wise_valid_vote_count_result.at[index_2, "candidateId"]),
                                        "candidateName": filtered_candidate_wise_valid_vote_count_result.at[
                                            index_2, "candidateName"],
                                        "partyName": filtered_candidate_wise_valid_vote_count_result.at[
                                            index_2, "partyName"],
                                        "numValue": None
                                    })
                            number_of_seats_allocated -= 1

            html = render_template(
                'PE-21.html',
                content=content
            )

            return html
