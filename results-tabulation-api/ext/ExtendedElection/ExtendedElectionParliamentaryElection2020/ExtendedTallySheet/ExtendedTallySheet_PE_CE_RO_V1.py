from flask import render_template

from constants.VOTE_TYPES import NonPostal
from ext.ExtendedTallySheet import ExtendedTallySheetReport
from orm.entities import Area
from util import to_comma_seperated_num, convert_image_to_data_uri, to_percentage
from orm.enums import AreaTypeEnum


class ExtendedTallySheet_PE_CE_RO_V1(ExtendedTallySheetReport):
    class ExtendedTallySheetVersion(ExtendedTallySheetReport.ExtendedTallySheetVersion):

        def html_letter(self, title="", total_registered_voters=None):
            tallySheetVersion = self.tallySheetVersion
            party_wise_valid_vote_count_result = self.get_party_wise_valid_vote_count_result()
            area_wise_valid_vote_count_result = self.get_area_wise_valid_vote_count_result()
            area_wise_rejected_vote_count_result = self.get_area_wise_rejected_vote_count_result()
            area_wise_vote_count_result = self.get_area_wise_vote_count_result()
            stamp = tallySheetVersion.stamp
            pollingDivision = tallySheetVersion.submission.area.areaName
            if tallySheetVersion.submission.election.voteType == Postal:
                pollingDivision = 'Postal'

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
                "electoralDistrict": Area.get_associated_areas(
                    tallySheetVersion.submission.area, AreaTypeEnum.ElectoralDistrict)[0].areaName,
                "pollingDivision": pollingDivision,
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
                'ParliamentaryElection2020/PE-CE-RO-V1-LETTER.html',
                content=content
            )

            return html

        def html(self, title="", total_registered_voters=None):
            tallySheetVersion = self.tallySheetVersion
            party_and_area_wise_valid_vote_count_result = self.get_party_and_area_wise_valid_vote_count_result()
            party_wise_valid_vote_count_result = self.get_party_wise_valid_vote_count_result()
            area_wise_valid_vote_count_result = self.get_area_wise_valid_vote_count_result()
            area_wise_rejected_vote_count_result = self.get_area_wise_rejected_vote_count_result()
            area_wise_vote_count_result = self.get_area_wise_vote_count_result()
            stamp = tallySheetVersion.stamp

            polling_division_name = tallySheetVersion.submission.area.areaName
            if tallySheetVersion.submission.election.voteType != NonPostal:
                polling_division_name = tallySheetVersion.submission.election.voteType

            content = {
                "election": {
                    "electionName": tallySheetVersion.submission.election.get_official_name()
                },
                "stamp": {
                    "createdAt": stamp.createdAt,
                    "createdBy": stamp.createdBy,
                    "barcodeString": stamp.barcodeString
                },
                "tallySheetCode": "CE/RO/V1",
                "electoralDistrict": Area.get_associated_areas(
                    tallySheetVersion.submission.area, AreaTypeEnum.ElectoralDistrict)[0].areaName,
                "pollingDivision": polling_division_name,
                "data": [],
                "countingCentres": [],
                "validVoteCounts": [],
                "rejectedVoteCounts": [],
                "totalVoteCounts": []
            }
            total_valid_vote_count = 0
            total_rejected_vote_count = 0
            total_vote_count = 0
            # Append the area wise column totals
            for area_wise_valid_vote_count_result_item in area_wise_valid_vote_count_result.itertuples():
                content["countingCentres"].append(area_wise_valid_vote_count_result_item.areaName)
                content["validVoteCounts"].append(
                    to_comma_seperated_num(area_wise_valid_vote_count_result_item.incompleteNumValue))
                total_valid_vote_count += area_wise_valid_vote_count_result_item.incompleteNumValue
            for area_wise_rejected_vote_count_result_item_index, area_wise_rejected_vote_count_result_item in area_wise_rejected_vote_count_result.iterrows():
                content["rejectedVoteCounts"].append(
                    to_comma_seperated_num(area_wise_rejected_vote_count_result_item.numValue))
                total_rejected_vote_count += area_wise_rejected_vote_count_result_item.numValue
            for area_wise_vote_count_result_item_index, area_wise_vote_count_result_item in area_wise_vote_count_result.iterrows():
                content["totalVoteCounts"].append(
                    to_comma_seperated_num(area_wise_vote_count_result_item.incompleteNumValue))
                total_vote_count += area_wise_vote_count_result_item.incompleteNumValue
            # Append the grand totals
            content["validVoteCounts"].append(to_comma_seperated_num(total_valid_vote_count))
            content["rejectedVoteCounts"].append(to_comma_seperated_num(total_rejected_vote_count))
            content["totalVoteCounts"].append(to_comma_seperated_num(total_vote_count))

            if tallySheetVersion.submission.election.voteType != NonPostal:
                content["tallySheetCode"] = "CE/RO/V1"

            number_of_counting_centres = len(area_wise_vote_count_result)
            for party_wise_valid_vote_count_result_item_index, party_wise_valid_vote_count_result_item in party_wise_valid_vote_count_result.iterrows():
                data_row = []

                data_row_number = party_wise_valid_vote_count_result_item_index + 1
                data_row.append(data_row_number)

                data_row.append(party_wise_valid_vote_count_result_item.partyName)

                for counting_centre_index in range(number_of_counting_centres):
                    party_and_area_wise_valid_vote_count_result_item_index = \
                        (
                                number_of_counting_centres * party_wise_valid_vote_count_result_item_index) + counting_centre_index

                    data_row.append(
                        to_comma_seperated_num(party_and_area_wise_valid_vote_count_result["numValue"].values[
                                                   party_and_area_wise_valid_vote_count_result_item_index]))

                data_row.append(to_comma_seperated_num(party_wise_valid_vote_count_result_item.incompleteNumValue))

                content["data"].append(data_row)

            html = render_template(
                'PE-CE-RO-V1.html',
                content=content
            )

            return html
