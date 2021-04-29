from flask import render_template
import re

from ext.ExtendedTallySheet import ExtendedTallySheetReport
from constants.VOTE_TYPES import NonPostal
from util import to_comma_seperated_num, to_percentage, convert_image_to_data_uri
from orm.entities import Area
from orm.enums import AreaTypeEnum


class ExtendedTallySheet_PCE_POST_PC(ExtendedTallySheetReport):
    def on_get_release_result_params(self):
        pd_code = None
        pd_name = None
        ed_code = None
        ed_name = None

        result_type = "RE_V"
        result_code = ed_code
        result_level = "NATIONAL"

        return result_type, result_code, result_level, ed_code, ed_name, pd_code, pd_name

    class ExtendedTallySheetVersion(ExtendedTallySheetReport.ExtendedTallySheetVersion):
        def json(self):
            extended_tally_sheet = self.tallySheet.get_extended_tally_sheet()
            result_type, result_code, result_level, ed_code, ed_name, pd_code, pd_name = extended_tally_sheet.on_get_release_result_params()

            party_wise_results = self.get_party_wise_valid_vote_count_result().sort_values(
                by=['numValue', "electionPartyId"], ascending=[False, True]
            ).reset_index()

            registered_voters_count = self.tallySheetVersion.tallySheet.area.get_registered_voters_count(
                vote_type=self.tallySheetVersion.tallySheet.election.voteType)
            total_valid_vote_count = 0
            total_rejected_vote_count = self.get_rejected_vote_count_result()["numValue"].values[0]
            for party_wise_result in party_wise_results.itertuples():
                total_valid_vote_count += float(party_wise_result.numValue)
            total_vote_count = total_valid_vote_count + total_rejected_vote_count

            print("hello")
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
                        "bonus_seat_count": 0
                    } for party_wise_result in party_wise_results.itertuples()
                ],
                "summary": {
                    "valid": int(total_valid_vote_count),
                    "rejected": int(total_rejected_vote_count),
                    "polled": int(total_vote_count),
                    "electors": int(registered_voters_count),
                    "percent_valid": to_percentage((total_valid_vote_count / total_vote_count) * 100),
                    "percent_rejected": to_percentage((total_rejected_vote_count / total_vote_count) * 100),
                    "percent_polled": to_percentage((total_vote_count / registered_voters_count) * 100)
                }
            }

        def html(self, title="", total_registered_voters=None):
            tallySheetVersion = self.tallySheetVersion

            area_wise_valid_vote_count_result = self.get_area_wise_valid_vote_count_result()
            party_wise_valid_vote_count_result = self.get_party_wise_valid_vote_count_result()
            # party_wise_valid_postal_vote_count_result = self.get_party_wise_valid_postal_vote_count_result()

            stamp = tallySheetVersion.stamp
            election = tallySheetVersion.tallySheet.election

            content = {
                "election": {
                    "electionName": election.get_official_name()
                },
                "stamp": {
                    "createdAt": stamp.createdAt,
                    "createdBy": stamp.createdBy,
                    "barcodeString": stamp.barcodeString
                },
                "tallySheetCode": "PCE/POST/PC",
                "data": [],
                "provinces": {},
                "attributes": ["No. of Votes", "No. of Postal Votes", "Total Votes", "Percentage", "No. of Seats",
                               "No. of Bonus Seats", "Total seats"],
            }

            # Append the grand totals
            number_of_administrative_districts = len(area_wise_valid_vote_count_result)

            for area_wise_valid_vote_count_result_item in area_wise_valid_vote_count_result.itertuples():
                province_name = Area.get_associated_areas(tallySheetVersion.tallySheet.area,
                                                          AreaTypeEnum.Province)[0].areaName
                if province_name not in content['provinces']:
                    content['provinces'][province_name] = []
                content['provinces'][province_name].append(area_wise_valid_vote_count_result_item.areaName)
            print(content['provinces'])
            for party_wise_valid_vote_count_result_item_index, party_wise_valid_vote_count_result_item in party_wise_valid_vote_count_result.iterrows():
                data_row = []

                data_row.append(party_wise_valid_vote_count_result_item.partyName)

                for administrative_district_index in range(number_of_administrative_districts):
                    party_and_area_wise_valid_vote_count_result_item_index = \
                        (
                                number_of_administrative_districts * party_wise_valid_vote_count_result_item_index) + administrative_district_index

                    # data_row.append(
                    #     to_comma_seperated_num(
                    #         party_wise_valid_vote_count_result["numValue"].values[
                    #             party_and_area_wise_valid_vote_count_result_item_index]))
                    data_row.append(
                        to_comma_seperated_num(0))
                content["data"].append(data_row)

            html = render_template(
                'ProvincialCouncilElection2021/PCE-POST-PC.html',
                content=content
            )

            return html
