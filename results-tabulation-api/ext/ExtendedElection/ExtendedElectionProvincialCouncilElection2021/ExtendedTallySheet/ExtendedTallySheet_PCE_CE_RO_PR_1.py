from flask import render_template

from constants.VOTE_TYPES import NonPostal
from ext.ExtendedTallySheet import ExtendedTallySheetReport
from orm.entities import Area
from util import to_comma_seperated_num
from orm.enums import AreaTypeEnum


class ExtendedTallySheet_PCE_CE_RO_PR_1(ExtendedTallySheetReport):
    class ExtendedTallySheetVersion(ExtendedTallySheetReport.ExtendedTallySheetVersion):

        def html(self, title="", total_registered_voters=None):
            tallySheetVersion = self.tallySheetVersion

            candidate_and_area_wise_valid_vote_count_result = self.get_candidate_and_area_wise_valid_vote_count_result()
            candidate_wise_valid_vote_count_result = self.get_candidate_wise_valid_vote_count_result()
            area_wise_valid_vote_count_result = self.get_area_wise_valid_vote_count_result()

            stamp = tallySheetVersion.stamp

            polling_division_name = tallySheetVersion.tallySheet.area.areaName

            if tallySheetVersion.tallySheet.election.voteType != NonPostal:
                polling_division_name = tallySheetVersion.tallySheet.election.voteType

            content = {
                "election": {
                    "electionName": tallySheetVersion.tallySheet.election.get_official_name()
                },
                "stamp": {
                    "createdAt": stamp.createdAt,
                    "createdBy": stamp.createdBy,
                    "barcodeString": stamp.barcodeString
                },
                "tallySheetCode": "CE/RO/PR/1",
                "electoralDistrict": Area.get_associated_areas(
                    tallySheetVersion.tallySheet.area, AreaTypeEnum.ElectoralDistrict)[0].areaName,
                "pollingDivision": polling_division_name,
                "partyName": candidate_and_area_wise_valid_vote_count_result["partyName"].values[0],
                "data": [],
                "countingCentres": [],
                "totalVoteCounts": []
            }

            # Append the area wise column totals
            for area_wise_valid_vote_count_result_item in area_wise_valid_vote_count_result.itertuples():
                content["countingCentres"].append(area_wise_valid_vote_count_result_item.areaName)
                content["totalVoteCounts"].append(
                    to_comma_seperated_num(area_wise_valid_vote_count_result_item.incompleteNumValue))

            for index_1 in candidate_wise_valid_vote_count_result.index:
                data_row = []

                candidate_id = candidate_wise_valid_vote_count_result.at[index_1, "candidateId"]
                candidate_number = candidate_wise_valid_vote_count_result.at[index_1, "candidateNumber"]

                data_row.append(candidate_number)

                for index_2 in candidate_and_area_wise_valid_vote_count_result.index:
                    if candidate_and_area_wise_valid_vote_count_result.at[index_2, "candidateId"] == candidate_id:
                        data_row.append(to_comma_seperated_num(
                            candidate_and_area_wise_valid_vote_count_result.at[index_2, "numValue"]
                        ))

                data_row.append(to_comma_seperated_num(
                    candidate_wise_valid_vote_count_result.at[index_1, "incompleteNumValue"]
                ))

                content["data"].append(data_row)

            content["totalVoteCounts"].append(to_comma_seperated_num(
                candidate_wise_valid_vote_count_result["numValue"].sum()
            ))

            html = render_template(
                'ProvincialCouncilElection2021/PCE-CE-RO-PR-1.html',
                content=content
            )

            return html
