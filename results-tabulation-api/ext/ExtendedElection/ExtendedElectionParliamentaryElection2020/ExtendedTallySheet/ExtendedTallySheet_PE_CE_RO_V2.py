from flask import render_template
import re

from ext.ExtendedTallySheet import ExtendedTallySheetReport
from constants.VOTE_TYPES import NonPostal
from util import to_comma_seperated_num, to_percentage, convert_image_to_data_uri


class ExtendedTallySheet_PE_CE_RO_V2(ExtendedTallySheetReport):
    def on_get_release_result_params(self):
        pd_code = None
        pd_name = None

        electoral_district = self.tallySheet.submission.area
        ed_name_regex_search = re.match('([0-9a-zA-Z]*) *- *(.*)', electoral_district.areaName)
        ed_code = ed_name_regex_search.group(1)
        ed_name = ed_name_regex_search.group(2)

        result_type = "RE_V"
        result_code = ed_code
        result_level = "ELECTORAL_DISTRICT"

        return result_type, result_code, result_level, ed_code, ed_name, pd_code, pd_name

    class ExtendedTallySheetVersion(ExtendedTallySheetReport.ExtendedTallySheetVersion):
        def json(self):
            extended_tally_sheet = self.tallySheet.get_extended_tally_sheet()
            result_type, result_code, result_level, ed_code, ed_name, pd_code, pd_name = extended_tally_sheet.on_get_release_result_params()

            party_wise_results = self.get_party_wise_valid_vote_count_result().sort_values(
                by=['numValue', "electionPartyId"], ascending=[False, True]
            ).reset_index()

            registered_voters_count = self.tallySheetVersion.submission.area.get_registered_voters_count(
                vote_type=self.tallySheetVersion.submission.election.voteType)
            total_valid_vote_count = 0
            total_rejected_vote_count = self.get_rejected_vote_count_result()["numValue"].values[0]
            for party_wise_result in party_wise_results.itertuples():
                total_valid_vote_count += float(party_wise_result.numValue)
            total_vote_count = total_valid_vote_count + total_rejected_vote_count

            return {
                "type": result_type,
                "level": result_level,
                "ed_code": ed_code,
                "ed_name": ed_name,
                "by_party": [
                    {
                        "party_code": party_wise_result.partyAbbreviation,
                        "party_name": party_wise_result.partyName,
                        "vote_count": int(party_wise_result.numValue),
                        "vote_percentage": to_percentage((party_wise_result.numValue / total_valid_vote_count) * 100),
                        "seat_count": 0,
                        "national_list_seat_count": 0
                    } for party_wise_result in party_wise_results.itertuples()
                ],
                "summary": {
                    "valid": int(total_valid_vote_count),
                    "rejected": int(total_rejected_vote_count),
                    "polled": int(total_vote_count),
                    "electors": int(registered_voters_count),
                    "percent_valid": to_percentage((total_valid_vote_count / registered_voters_count) * 100),
                    "percent_rejected": to_percentage((total_rejected_vote_count / registered_voters_count) * 100),
                    "percent_polled": to_percentage((total_vote_count / registered_voters_count) * 100)
                }
            }

        def html_letter(self, title="", total_registered_voters=None):
            tallySheetVersion = self.tallySheetVersion
            party_wise_valid_vote_count_result = self.get_party_wise_valid_vote_count_result()
            area_wise_valid_vote_count_result = self.get_area_wise_valid_vote_count_result()
            area_wise_rejected_vote_count_result = self.get_area_wise_rejected_vote_count_result()
            area_wise_vote_count_result = self.get_area_wise_vote_count_result()
            stamp = tallySheetVersion.stamp

            registered_voters_count = tallySheetVersion.submission.area.get_registered_voters_count(
                vote_type=tallySheetVersion.submission.election.voteType)

            content = {
                "election": {
                    "electionName": tallySheetVersion.submission.election.get_official_name()
                },
                "stamp": {
                    "createdAt": stamp.createdAt,
                    "createdBy": stamp.createdBy,
                    "barcodeString": stamp.barcodeString
                },
                "electoralDistrict": tallySheetVersion.submission.area.areaName,
                "data": [],
                "validVoteCounts": [0, "0%"],
                "rejectedVoteCounts": [0, "0%"],
                "totalVoteCounts": [0, "0%"],
                "registeredVoters": [
                    to_comma_seperated_num(registered_voters_count),
                    100
                ],
                "logo": convert_image_to_data_uri("static/Emblem_of_Sri_Lanka.png"),
                "date": stamp.createdAt.strftime("%d/%m/%Y"),
                "time": stamp.createdAt.strftime("%H:%M:%S %p")
            }

            total_valid_vote_count = 0
            for area_wise_valid_vote_count_result_item in area_wise_valid_vote_count_result.itertuples():
                total_valid_vote_count += float(area_wise_valid_vote_count_result_item.incompleteNumValue)
            content["validVoteCounts"][0] = to_comma_seperated_num(total_valid_vote_count)
            content["validVoteCounts"][1] = to_percentage((total_valid_vote_count / registered_voters_count) * 100)

            total_rejected_vote_count = 0
            for area_wise_rejected_vote_count_result_item in area_wise_rejected_vote_count_result.itertuples():
                total_rejected_vote_count += float(area_wise_rejected_vote_count_result_item.numValue)
            content["rejectedVoteCounts"][0] = to_comma_seperated_num(total_rejected_vote_count)
            content["rejectedVoteCounts"][1] = to_percentage(
                (total_rejected_vote_count / registered_voters_count) * 100)

            total_vote_count = 0
            for area_wise_vote_count_result_item in area_wise_vote_count_result.itertuples():
                total_vote_count += float(area_wise_vote_count_result_item.incompleteNumValue)
            content["totalVoteCounts"][0] = to_comma_seperated_num(total_vote_count)
            content["totalVoteCounts"][1] = to_percentage((total_vote_count / registered_voters_count) * 100)

            # sort by vote count descending
            party_wise_valid_vote_count_result = party_wise_valid_vote_count_result.sort_values(
                by=['numValue', "electionPartyId"], ascending=[False, True]
            ).reset_index()

            for party_wise_valid_vote_count_result_item_index, party_wise_valid_vote_count_result_item in party_wise_valid_vote_count_result.iterrows():
                data_row = [
                    party_wise_valid_vote_count_result_item.partyName,
                    party_wise_valid_vote_count_result_item.partyAbbreviation,
                    to_comma_seperated_num(party_wise_valid_vote_count_result_item.numValue)
                ]

                if total_valid_vote_count > 0:
                    data_row.append(to_percentage(
                        party_wise_valid_vote_count_result_item.numValue * 100 / total_valid_vote_count))
                else:
                    data_row.append('')

                content["data"].append(data_row)

            html = render_template(
                'ParliamentaryElection2020/PE-CE-RO-V2-LETTER.html',
                content=content
            )

            return html

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
