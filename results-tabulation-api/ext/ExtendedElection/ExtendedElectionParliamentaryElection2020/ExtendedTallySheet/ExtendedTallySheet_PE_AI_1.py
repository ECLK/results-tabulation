import pandas as pd
import numpy as np
from flask import render_template

from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.TEMPLATE_ROW_TYPE import \
    TEMPLATE_ROW_TYPE_NATIONAL_LIST_SEATS_ALLOCATED, TEMPLATE_ROW_TYPE_SEATS_ALLOCATED
from ext.ExtendedTallySheet import ExtendedTallySheetReport
from util import to_comma_seperated_num, to_percentage, convert_image_to_data_uri, get_sum_of_all_and_nan_otherwise, \
    get_sum_of_numbers_only_and_nan_otherwise


class ExtendedTallySheet_PE_AI_1(ExtendedTallySheetReport):
    class ExtendedTallySheetVersion(ExtendedTallySheetReport.ExtendedTallySheetVersion):
        def get_party_wise_results(self):
            party_wise_calculations_df = self.get_party_wise_valid_vote_count_result()

            for index_1 in party_wise_calculations_df.index:
                party_wise_calculations_df.at[index_1, "seatsAllocated"] = np.nan
                party_wise_calculations_df.at[index_1, "nationalListSeatsAllocated"] = np.nan
                party_wise_calculations_df.at[index_1, "validVoteCount"] = party_wise_calculations_df.at[
                    index_1, "numValue"]

                party_id = party_wise_calculations_df.at[index_1, "partyId"]
                filtered_df = self.df.loc[self.df['partyId'] == party_id]

                for index_2 in filtered_df.index:
                    template_row_type = filtered_df.at[index_2, "templateRowType"]
                    num_value = filtered_df.at[index_2, "numValue"]

                    if num_value is not None and not np.isnan(num_value):
                        if template_row_type == TEMPLATE_ROW_TYPE_SEATS_ALLOCATED:
                            party_wise_calculations_df.at[
                                index_1, "seatsAllocated"] = get_sum_of_numbers_only_and_nan_otherwise(
                                [party_wise_calculations_df.at[index_1, "seatsAllocated"], num_value])

                        if template_row_type == TEMPLATE_ROW_TYPE_NATIONAL_LIST_SEATS_ALLOCATED:
                            party_wise_calculations_df.at[
                                index_1, "nationalListSeatsAllocated"] = get_sum_of_numbers_only_and_nan_otherwise(
                                [party_wise_calculations_df.at[index_1, "nationalListSeatsAllocated"], num_value])

                party_wise_calculations_df.at[
                    index_1, "totalSeatsAllocated"] = get_sum_of_numbers_only_and_nan_otherwise(
                    [party_wise_calculations_df.at[index_1, "seatsAllocated"],
                     party_wise_calculations_df.at[index_1, "nationalListSeatsAllocated"]])

            return party_wise_calculations_df

        def html(self, title="", total_registered_voters=None):
            tallySheetVersion = self.tallySheetVersion
            party_wise_results = self.get_party_wise_results()
            stamp = tallySheetVersion.stamp

            registered_voters_count = tallySheetVersion.submission.area.get_registered_voters_count()
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
            total_rejected_vote_count = self.get_rejected_vote_count_result()["numValue"].values[0]
            for party_wise_result in party_wise_results.itertuples():
                total_valid_vote_count += float(party_wise_result.validVoteCount)
            total_vote_count = total_valid_vote_count + total_rejected_vote_count

            content["validVoteCounts"][0] = to_comma_seperated_num(total_valid_vote_count)
            content["validVoteCounts"][1] = to_percentage((total_valid_vote_count / registered_voters_count) * 100)

            content["rejectedVoteCounts"][0] = to_comma_seperated_num(total_rejected_vote_count)
            content["rejectedVoteCounts"][1] = to_percentage(
                (total_rejected_vote_count / registered_voters_count) * 100)

            content["totalVoteCounts"][0] = to_comma_seperated_num(total_vote_count)
            content["totalVoteCounts"][1] = to_percentage((total_vote_count / registered_voters_count) * 100)

            # sort by total seat count descending
            party_wise_results = party_wise_results.sort_values(
                by=['totalSeatsAllocated'], ascending=False
            ).reset_index()

            for party_wise_result in party_wise_results.itertuples():
                data_row = [
                    party_wise_result.partyName,
                    party_wise_result.partyAbbreviation,
                    to_comma_seperated_num(party_wise_result.validVoteCount)
                ]

                if total_valid_vote_count > 0:
                    data_row.append(to_percentage(
                        party_wise_result.validVoteCount * 100 / total_valid_vote_count))
                else:
                    data_row.append('')

                data_row.append(to_comma_seperated_num(party_wise_result.seatsAllocated))
                data_row.append(to_comma_seperated_num(party_wise_result.nationalListSeatsAllocated))
                data_row.append(to_comma_seperated_num(party_wise_result.totalSeatsAllocated))

                content["data"].append(data_row)

            html = render_template(
                'ParliamentaryElection2020/PE-AI-1.html',
                content=content
            )

            return html

        def html_letter(self, title="", total_registered_voters=None):
            tallySheetVersion = self.tallySheetVersion
            party_wise_results = self.get_party_wise_results()
            stamp = tallySheetVersion.stamp

            registered_voters_count = tallySheetVersion.submission.area.get_registered_voters_count()
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
            total_rejected_vote_count = self.get_rejected_vote_count_result()["numValue"].values[0]
            for party_wise_result in party_wise_results.itertuples():
                total_valid_vote_count += float(party_wise_result.validVoteCount)
            total_vote_count = total_valid_vote_count + total_rejected_vote_count

            content["validVoteCounts"][0] = to_comma_seperated_num(total_valid_vote_count)
            content["validVoteCounts"][1] = to_percentage((total_valid_vote_count / registered_voters_count) * 100)

            content["rejectedVoteCounts"][0] = to_comma_seperated_num(total_rejected_vote_count)
            content["rejectedVoteCounts"][1] = to_percentage(
                (total_rejected_vote_count / registered_voters_count) * 100)

            content["totalVoteCounts"][0] = to_comma_seperated_num(total_vote_count)
            content["totalVoteCounts"][1] = to_percentage((total_vote_count / registered_voters_count) * 100)

            # sort by total seat count descending
            party_wise_results = party_wise_results.sort_values(
                by=['totalSeatsAllocated'], ascending=False
            ).reset_index()

            for party_wise_result in party_wise_results.itertuples():
                data_row = [
                    party_wise_result.partyName,
                    party_wise_result.partyAbbreviation,
                    to_comma_seperated_num(party_wise_result.validVoteCount)
                ]

                if total_valid_vote_count > 0:
                    data_row.append(to_percentage(
                        party_wise_result.validVoteCount * 100 / total_valid_vote_count))
                else:
                    data_row.append('')

                data_row.append(to_comma_seperated_num(party_wise_result.seatsAllocated))
                data_row.append(to_comma_seperated_num(party_wise_result.nationalListSeatsAllocated))
                data_row.append(to_comma_seperated_num(party_wise_result.totalSeatsAllocated))

                content["data"].append(data_row)

            html = render_template(
                'ParliamentaryElection2020/PE-AI-1.html',
                content=content
            )

            return html
