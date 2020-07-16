from flask import render_template

from ext.ExtendedTallySheet import ExtendedTallySheetReport
from constants.VOTE_TYPES import NonPostal
from util import to_comma_seperated_num


class ExtendedTallySheet_PE_CE_RO_V2(ExtendedTallySheetReport):
    class ExtendedTallySheetVersion(ExtendedTallySheetReport.ExtendedTallySheetVersion):

        def html_letter(self, title="", total_registered_voters=None):
            return super(ExtendedTallySheet_PE_CE_RO_V2.ExtendedTallySheetVersion, self).html_letter(
                title="Results of Electoral District %s" % self.tallySheetVersion.submission.area.areaName
            )

        def html(self, title="", total_registered_voters=None):
            tallySheetVersion = self.tallySheetVersion

            party_and_area_wise_valid_non_postal_vote_count_result = self.get_party_and_area_wise_valid_non_postal_vote_count_result()
            area_wise_valid_non_postal_vote_count_result = self.get_area_wise_valid_non_postal_vote_count_result()
            area_wise_rejected_non_postal_vote_count_result = self.get_area_wise_rejected_non_postal_vote_count_result()
            area_wise_non_postal_vote_count_result = self.get_area_wise_non_postal_vote_count_result()
            party_wise_valid_vote_count_result = self.get_party_wise_valid_vote_count_result()

            vote_count_result = self.get_vote_count_result()
            valid_vote_count_result = self.get_valid_vote_count_result()
            rejected_vote_count_result = self.get_rejected_vote_count_result()

            stamp = tallySheetVersion.stamp
            election = tallySheetVersion.submission.election
            non_postal_vote_types = []
            for sub_election in election.subElections:
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
                "tallySheetCode": "CE/RO/V/2",
                "electoralDistrict": tallySheetVersion.submission.area.areaName,
                "nonPostalVoteTypes": non_postal_vote_types,
                "data": [],
                "pollingDivisions": [],
                "validVoteCounts": [],
                "rejectedVoteCounts": [],
                "totalVoteCounts": []
            }

            total_valid_vote_count = 0
            total_rejected_vote_count = 0
            total_vote_count = 0

            # Append the area wise column totals
            print(area_wise_valid_non_postal_vote_count_result)
            for area_wise_valid_non_postal_vote_count_result_item in area_wise_valid_non_postal_vote_count_result.itertuples():
                content["pollingDivisions"].append(area_wise_valid_non_postal_vote_count_result_item.areaName)
                content["validVoteCounts"].append(
                    to_comma_seperated_num(area_wise_valid_non_postal_vote_count_result_item.incompleteNumValue))
                total_valid_vote_count += area_wise_valid_non_postal_vote_count_result_item.incompleteNumValue

            for area_wise_rejected_non_postal_vote_count_result_item_index, area_wise_rejected_non_postal_vote_count_result_item in area_wise_rejected_non_postal_vote_count_result.iterrows():
                content["rejectedVoteCounts"].append(
                    to_comma_seperated_num(area_wise_rejected_non_postal_vote_count_result_item.numValue))
                total_rejected_vote_count += area_wise_rejected_non_postal_vote_count_result_item.numValue

            for area_wise_non_postal_vote_count_result_item_index, area_wise_non_postal_vote_count_result_item in area_wise_non_postal_vote_count_result.iterrows():
                content["totalVoteCounts"].append(
                    to_comma_seperated_num(area_wise_non_postal_vote_count_result_item.incompleteNumValue))
                total_vote_count += area_wise_non_postal_vote_count_result_item.incompleteNumValue

            for vote_type in non_postal_vote_types:
                postal_vote_count_result = self.get_vote_count_result(vote_type=vote_type)
                postal_valid_vote_count_result = self.get_valid_vote_count_result(vote_type=vote_type)
                postal_rejected_vote_count_result = self.get_rejected_vote_count_result(vote_type=vote_type)

                # Append the postal vote count totals
                content["pollingDivisions"].append("%s Votes" % vote_type)
                content["validVoteCounts"].append(
                    to_comma_seperated_num(postal_valid_vote_count_result["incompleteNumValue"].values[0]))
                content["rejectedVoteCounts"].append(
                    to_comma_seperated_num(postal_rejected_vote_count_result["numValue"].values[0]))
                content["totalVoteCounts"].append(
                    to_comma_seperated_num(postal_vote_count_result["incompleteNumValue"].values[0]))

            # Append the grand totals
            content["validVoteCounts"].append(
                to_comma_seperated_num(valid_vote_count_result["incompleteNumValue"].values[0]))
            content["rejectedVoteCounts"].append(
                to_comma_seperated_num(rejected_vote_count_result["incompleteNumValue"].values[0]))
            content["totalVoteCounts"].append(to_comma_seperated_num(vote_count_result["incompleteNumValue"].values[0]))

            number_of_counting_centres = len(area_wise_non_postal_vote_count_result)

            for party_wise_valid_vote_count_result_item_index, party_wise_valid_vote_count_result_item in party_wise_valid_vote_count_result.iterrows():
                data_row = []

                data_row_number = party_wise_valid_vote_count_result_item_index + 1
                data_row.append(data_row_number)

                data_row.append(party_wise_valid_vote_count_result_item.partyName)

                for counting_centre_index in range(number_of_counting_centres):
                    party_and_area_wise_valid_non_postal_vote_count_result_item_index = \
                        (
                                number_of_counting_centres * party_wise_valid_vote_count_result_item_index) + counting_centre_index

                    data_row.append(
                        to_comma_seperated_num(
                            party_and_area_wise_valid_non_postal_vote_count_result["numValue"].values[
                                party_and_area_wise_valid_non_postal_vote_count_result_item_index]))

                for vote_type in non_postal_vote_types:
                    party_wise_valid_postal_vote_count_result = self.get_party_wise_valid_vote_count_result(
                        vote_type=vote_type)
                    data_row.append(to_comma_seperated_num(party_wise_valid_postal_vote_count_result["numValue"].values[
                                                               party_wise_valid_vote_count_result_item_index]))

                data_row.append(to_comma_seperated_num(party_wise_valid_vote_count_result_item.incompleteNumValue))

                content["data"].append(data_row)

            html = render_template(
                'PE-CE-RO-V2.html',
                content=content
            )

            return html
