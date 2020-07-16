import math

from flask import render_template

from constants.VOTE_TYPES import NonPostal
from ext.ExtendedTallySheet import ExtendedTallySheetReport
from orm.entities import Area
from orm.entities.Area import AreaModel
from util import to_comma_seperated_num, to_percentage
from orm.enums import AreaTypeEnum


class ExtendedTallySheet_POLLING_DIVISION_RESULTS(ExtendedTallySheetReport):
    class ExtendedTallySheetVersion(ExtendedTallySheetReport.ExtendedTallySheetVersion):

        def html_letter(self, title="", total_registered_voters=None):
            return super(ExtendedTallySheet_POLLING_DIVISION_RESULTS.ExtendedTallySheetVersion, self).html_letter(
                title="Results of Polling Division %s" % self.tallySheetVersion.submission.area.areaName
            )

        def html(self, title="", total_registered_voters=None):
            tallySheetVersion = self.tallySheetVersion

            party_wise_valid_vote_count_result = self.get_party_wise_valid_vote_count_result()
            area_wise_rejected_vote_count_result = self.get_area_wise_rejected_vote_count_result()

            stamp = tallySheetVersion.stamp

            registered_voters_count = tallySheetVersion.submission.area.get_registered_voters_count(
                vote_type=tallySheetVersion.submission.election.voteType)
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
                "tallySheetCode": "POLLING DIVISION RESULTS",
                "electoralDistrict": Area.get_associated_areas(
                    tallySheetVersion.submission.area, AreaTypeEnum.ElectoralDistrict)[0].areaName,
                "pollingDivision": polling_division_name,
                "data": [],
                "totalValidVoteCount": '',
                "totalValidVotePercentage": '',
                "rejectedVoteCount": '',
                "rejectedVotePercentage": '',
                "totalVoteCount": '',
                "totalVotePercentage": '',
                "numberOfElectors": to_comma_seperated_num(registered_voters_count)
            }

            total_valid_vote_count = 0
            total_rejected_vote_count = 0
            total_vote_count = 0
            party_wise_valid_total_votes = []

            for index, party_wise_valid_vote_count_result_item in party_wise_valid_vote_count_result.iterrows():
                data_row = [party_wise_valid_vote_count_result_item.partyName]
                vote_count = party_wise_valid_vote_count_result_item.numValue
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
            total_vote_percentage = (
                        total_vote_count * 100 / registered_voters_count) if registered_voters_count > 0 else 0
            content["totalVotePercentage"] = to_percentage(total_vote_percentage)

            html = render_template(
                'POLLING-DIVISION-RESULTS.html',
                content=content
            )

            return html
