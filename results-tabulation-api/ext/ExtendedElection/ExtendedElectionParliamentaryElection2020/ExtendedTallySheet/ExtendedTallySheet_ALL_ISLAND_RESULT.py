import math

from flask import render_template

from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.ExtendedTallySheet.ExtendedTallySheet_PE_R2 import \
    get_party_wise_seat_calculations
from ext.ExtendedTallySheet import ExtendedTallySheetReport
from orm.entities.Area import AreaModel
from util import to_comma_seperated_num, to_percentage, convert_image_to_data_uri


class ExtendedTallySheet_ALL_ISLAND_RESULT(ExtendedTallySheetReport):
    class ExtendedTallySheetVersion(ExtendedTallySheetReport.ExtendedTallySheetVersion):

        def html_letter(self, title="", total_registered_voters=None):
            tallySheetVersion = self.tallySheetVersion
            party_wise_valid_vote_count_result = self.get_party_wise_valid_vote_count_result()
            area_wise_valid_vote_count_result = self.get_area_wise_valid_vote_count_result()
            area_wise_rejected_vote_count_result = self.get_area_wise_rejected_vote_count_result()
            area_wise_vote_count_result = self.get_area_wise_vote_count_result()
            stamp = tallySheetVersion.stamp

            registered_voters_count = float(tallySheetVersion.submission.area.registeredVotersCount)
            content = {
                "election": {
                    "electionName": tallySheetVersion.submission.election.get_official_name()
                },
                "stamp": {
                    "createdAt": stamp.createdAt,
                    "createdBy": stamp.createdBy,
                    "barcodeString": stamp.barcodeString
                },
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
                by=['numValue'], ascending=False
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
                'ParliamentaryElection2020/AI-LETTER.html',
                content=content
            )

            return html

        def html(self, title="", total_registered_voters=None):
            tallySheetVersion = self.tallySheetVersion

            party_wise_valid_vote_count_result = self.get_party_wise_valid_vote_count_result().sort_values(
                by=['incompleteNumValue'], ascending=False).reset_index()
            area_wise_rejected_vote_count_result = self.get_area_wise_rejected_vote_count_result()

            stamp = tallySheetVersion.stamp

            area: AreaModel = tallySheetVersion.submission.area
            number_of_electors = float(area.registeredVotersCount) + float(area.registeredPostalVotersCount)

            content = {
                "election": {
                    "electionName": tallySheetVersion.submission.election.get_official_name()
                },
                "stamp": {
                    "createdAt": stamp.createdAt,
                    "createdBy": stamp.createdBy,
                    "barcodeString": stamp.barcodeString
                },
                "tallySheetCode": "ALL ISLAND RESULTS",
                "data": [],
                "totalValidVoteCount": '',
                "totalValidVotePercentage": '',
                "rejectedVoteCount": '',
                "rejectedVotePercentage": '',
                "totalVoteCount": '',
                "totalVotePercentage": '',
                "numberOfElectors": to_comma_seperated_num(number_of_electors)
            }

            total_valid_vote_count = 0
            total_rejected_vote_count = 0
            total_vote_count = 0
            party_wise_valid_total_votes = []

            for index, party_wise_valid_vote_count_result_item in party_wise_valid_vote_count_result.iterrows():
                data_row = [party_wise_valid_vote_count_result_item.partyName]
                vote_count = party_wise_valid_vote_count_result_item.incompleteNumValue
                party_wise_valid_total_votes.append(vote_count if not math.isnan(vote_count) else 0)
                data_row.append(to_comma_seperated_num(vote_count))
                total_valid_vote_count += vote_count if not math.isnan(vote_count) else 0
                content["data"].append(data_row)

            total_valid_vote_count = total_valid_vote_count if not math.isnan(total_valid_vote_count) else 0
            content["totalValidVoteCount"] = to_comma_seperated_num(total_valid_vote_count)

            # party wise percentage calculation
            for index, party_vote_count in enumerate(party_wise_valid_total_votes):
                percentage_value = to_percentage(0)
                if total_valid_vote_count > 0:
                    percentage_value = to_percentage(party_vote_count * 100 / total_valid_vote_count)
                content["data"][index].append(percentage_value)

            for index, area_wise_rejected_vote_count_result_item in area_wise_rejected_vote_count_result.iterrows():
                rejected_vote_count = area_wise_rejected_vote_count_result_item.numValue
                total_rejected_vote_count += rejected_vote_count if not math.isnan(rejected_vote_count) else 0
            content["rejectedVoteCount"] = to_comma_seperated_num(total_rejected_vote_count)

            total_vote_count = total_valid_vote_count + total_rejected_vote_count
            content["totalVoteCount"] = to_comma_seperated_num(total_vote_count)
            total_valid_vote_percentage = (
                    total_valid_vote_count * 100 / total_vote_count) if total_vote_count > 0 else 0
            content["totalValidVotePercentage"] = to_percentage(total_valid_vote_percentage)
            rejected_vote_percentage = (
                    total_rejected_vote_count * 100 / total_vote_count) if total_vote_count > 0 else 0
            content["rejectedVotePercentage"] = to_percentage(rejected_vote_percentage)
            total_vote_percentage = (total_vote_count * 100 / number_of_electors) if number_of_electors > 0 else 0
            content["totalVotePercentage"] = to_percentage(total_vote_percentage)

            html = render_template(
                'ALL_ISLAND_RESULT.html',
                content=content
            )

            return html
