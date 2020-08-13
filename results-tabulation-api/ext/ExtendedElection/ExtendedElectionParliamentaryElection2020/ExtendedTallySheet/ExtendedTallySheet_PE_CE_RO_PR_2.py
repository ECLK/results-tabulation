from flask import render_template

from constants.VOTE_TYPES import NonPostal
from ext.ExtendedTallySheet import ExtendedTallySheetReport
from orm.entities import Area
from util import to_comma_seperated_num
from orm.enums import AreaTypeEnum


class ExtendedTallySheet_PE_CE_RO_PR_2(ExtendedTallySheetReport):
    class ExtendedTallySheetVersion(ExtendedTallySheetReport.ExtendedTallySheetVersion):

        def html(self, title="", total_registered_voters=None):
            tallySheetVersion = self.tallySheetVersion

            candidate_and_area_wise_valid_non_postal_vote_count_result = self.get_candidate_and_area_wise_valid_non_postal_vote_count_result()
            candidate_wise_valid_vote_count_result = self.get_candidate_wise_valid_vote_count_result()
            area_wise_non_postal_vote_count_result = self.get_area_wise_non_postal_vote_count_result()

            stamp = tallySheetVersion.stamp
            election = tallySheetVersion.tallySheet.election

            non_postal_vote_types = []
            vote_type_to_candidate_wise_valid_vote_count_result_map = {}

            for sub_election in election.subElections:
                vote_type_to_candidate_wise_valid_vote_count_result_map[
                    sub_election.voteType] = self.get_candidate_wise_valid_vote_count_result(
                    vote_type=sub_election.voteType)

                if sub_election.voteType != NonPostal:
                    non_postal_vote_types.append(sub_election.voteType)

            content = {
                "election": {
                    "electionName": election.get_official_name()
                },
                "stamp": {
                    "createdAt": stamp.createdAt,
                    "createdBy": stamp.createdBy,
                    "barcodeString": stamp.barcodeString
                },
                "tallySheetCode": "CE/RO/PR/2",
                "electoralDistrict": tallySheetVersion.tallySheet.area.areaName,
                "nonPostalVoteTypes": non_postal_vote_types,
                "partyName": candidate_and_area_wise_valid_non_postal_vote_count_result["partyName"].values[0],
                "data": [],
                "pollingDivisions": [],
                "totalVoteCounts": []
            }

            # Append the area wise column totals
            for area_wise_non_postal_vote_count_result_item in area_wise_non_postal_vote_count_result.itertuples():
                print(area_wise_non_postal_vote_count_result_item.areaName)
                content["pollingDivisions"].append(area_wise_non_postal_vote_count_result_item.areaName)
                content["totalVoteCounts"].append(
                    to_comma_seperated_num(area_wise_non_postal_vote_count_result_item.incompleteNumValue)
                )

            for vote_type in non_postal_vote_types:
                content["pollingDivisions"].append(vote_type)
                content["totalVoteCounts"].append(to_comma_seperated_num(
                    vote_type_to_candidate_wise_valid_vote_count_result_map[vote_type]["numValue"].sum()))

            if tallySheetVersion.tallySheet.election.voteType != NonPostal:
                content["tallySheetCode"] = "CE/RO/PR/2"

            for index_1 in candidate_wise_valid_vote_count_result.index:
                data_row = []

                candidate_id = candidate_wise_valid_vote_count_result.at[index_1, "candidateId"]
                candidate_number = candidate_wise_valid_vote_count_result.at[index_1, "candidateNumber"]

                data_row.append(candidate_number)

                for index_2 in candidate_and_area_wise_valid_non_postal_vote_count_result.index:
                    if candidate_and_area_wise_valid_non_postal_vote_count_result.at[
                        index_2, "candidateId"] == candidate_id:
                        data_row.append(to_comma_seperated_num(
                            candidate_and_area_wise_valid_non_postal_vote_count_result.at[index_2, "numValue"]))

                for vote_type in non_postal_vote_types:
                    data_row.append(to_comma_seperated_num(
                        vote_type_to_candidate_wise_valid_vote_count_result_map[vote_type]["numValue"].values[index_1]))

                data_row.append(
                    to_comma_seperated_num(candidate_wise_valid_vote_count_result.at[index_1, "incompleteNumValue"]))

                content["data"].append(data_row)

            content["totalVoteCounts"].append(
                to_comma_seperated_num(candidate_wise_valid_vote_count_result["incompleteNumValue"].sum()))

            html = render_template(
                'PE-CE-RO-PR-2.html',
                content=content
            )

            return html
