from flask import render_template

from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.TEMPLATE_ROW_TYPE import \
    TEMPLATE_ROW_TYPE_SEATS_ALLOCATED
from ext.ExtendedTallySheet import ExtendedTallySheetReport
from util import to_comma_seperated_num, convert_image_to_data_uri, to_percentage, \
    get_sum_of_numbers_only_and_nan_otherwise


class ExtendedTallySheet_PE_AI_SA(ExtendedTallySheetReport):
    class ExtendedTallySheetVersion(ExtendedTallySheetReport.ExtendedTallySheetVersion):

        def html(self, title="", total_registered_voters=None):
            tallySheetVersion = self.tallySheetVersion
            party_wise_valid_vote_count_result = self.get_party_wise_valid_vote_count_result()
            area_wise_valid_vote_count_result = self.get_area_wise_valid_vote_count_result()
            area_wise_rejected_vote_count_result = self.get_area_wise_rejected_vote_count_result()
            area_wise_vote_count_result = self.get_area_wise_vote_count_result()
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

            seats_allocated_per_party_df = self.df.loc[
                (self.df['templateRowType'] == TEMPLATE_ROW_TYPE_SEATS_ALLOCATED)]
            seats_allocated_per_party_df = seats_allocated_per_party_df.groupby(['partyId']).agg({
                'numValue': lambda x: x.sum(skipna=False),
                'incompleteNumValue': get_sum_of_numbers_only_and_nan_otherwise
            }).reset_index()

            for party_wise_valid_vote_count_result_item_index, party_wise_valid_vote_count_result_item in party_wise_valid_vote_count_result.iterrows():
                data_row = [
                    party_wise_valid_vote_count_result_item.partyName,
                    party_wise_valid_vote_count_result_item.partyAbbreviation,
                    to_comma_seperated_num(party_wise_valid_vote_count_result_item.incompleteNumValue)
                ]

                if total_valid_vote_count > 0:
                    data_row.append(to_percentage(
                        party_wise_valid_vote_count_result_item.incompleteNumValue * 100 / total_valid_vote_count))
                else:
                    data_row.append('')

                filtered_seats_allocated_per_party_df = seats_allocated_per_party_df.loc[
                    seats_allocated_per_party_df['partyId'] == party_wise_valid_vote_count_result_item.partyId]
                if len(filtered_seats_allocated_per_party_df) > 0:
                    data_row.append(to_comma_seperated_num(filtered_seats_allocated_per_party_df["numValue"].values[0]))
                else:
                    data_row.append('')

                content["data"].append(data_row)

            html = render_template(
                'ParliamentaryElection2020/PE-AI-SA.html',
                content=content
            )

            return html

        def html_letter(self, title="", total_registered_voters=None):
            tallySheetVersion = self.tallySheetVersion
            party_wise_valid_vote_count_result = self.get_party_wise_valid_vote_count_result()
            area_wise_valid_vote_count_result = self.get_area_wise_valid_vote_count_result()
            area_wise_rejected_vote_count_result = self.get_area_wise_rejected_vote_count_result()
            area_wise_vote_count_result = self.get_area_wise_vote_count_result()
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

            seats_allocated_per_party_df = self.df.loc[
                (self.df['templateRowType'] == TEMPLATE_ROW_TYPE_SEATS_ALLOCATED)]
            seats_allocated_per_party_df = seats_allocated_per_party_df.groupby(['partyId']).agg({
                'numValue': lambda x: x.sum(skipna=False),
                'incompleteNumValue': get_sum_of_numbers_only_and_nan_otherwise
            }).reset_index()

            for party_wise_valid_vote_count_result_item_index, party_wise_valid_vote_count_result_item in party_wise_valid_vote_count_result.iterrows():
                data_row = [
                    party_wise_valid_vote_count_result_item.partyName,
                    party_wise_valid_vote_count_result_item.partyAbbreviation,
                    to_comma_seperated_num(party_wise_valid_vote_count_result_item.incompleteNumValue)
                ]

                if total_valid_vote_count > 0:
                    data_row.append(to_percentage(
                        party_wise_valid_vote_count_result_item.incompleteNumValue * 100 / total_valid_vote_count))
                else:
                    data_row.append('')

                filtered_seats_allocated_per_party_df = seats_allocated_per_party_df.loc[
                    seats_allocated_per_party_df['partyId'] == party_wise_valid_vote_count_result_item.partyId]
                if len(filtered_seats_allocated_per_party_df) > 0:
                    data_row.append(to_comma_seperated_num(filtered_seats_allocated_per_party_df["numValue"].values[0]))
                else:
                    data_row.append('')

                content["data"].append(data_row)

            html = render_template(
                'ParliamentaryElection2020/PE-AI-SA-LETTER.html',
                content=content
            )

            return html
