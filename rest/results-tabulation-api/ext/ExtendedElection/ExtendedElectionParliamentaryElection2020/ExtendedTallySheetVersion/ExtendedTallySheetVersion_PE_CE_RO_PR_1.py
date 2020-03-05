from flask import render_template
from ext.ExtendedTallySheetVersion import ExtendedTallySheetVersion
from orm.entities import Area
from constants.VOTE_TYPES import Postal
from util import to_comma_seperated_num
from orm.enums import AreaTypeEnum
import math


class ExtendedTallySheetVersion_PE_CE_RO_PR_1(ExtendedTallySheetVersion):

    def html_letter(self, title="", total_registered_voters=None):
        return super(ExtendedTallySheetVersion_PE_CE_RO_PR_1, self).html_letter(
            title="Results of Electoral District %s" % self.tallySheetVersion.submission.area.areaName
        )

    def html(self, title="", total_registered_voters=None):
        tallySheetVersion = self.tallySheetVersion

        candidate_and_area_wise_valid_vote_count_result = self.get_candidate_and_area_wise_valid_vote_count_result()
        candidate_wise_valid_vote_count_result = self.get_candidate_wise_valid_vote_count_result()
        area_wise_valid_vote_count_result = self.get_area_wise_valid_vote_count_result()
        area_wise_vote_count_result = self.get_area_wise_vote_count_result()

        stamp = tallySheetVersion.stamp

        pollingDivision = tallySheetVersion.submission.area.areaName
        if tallySheetVersion.submission.election.voteType == Postal:
            pollingDivision = 'Postal'

        content = {
            "election": {
                "electionName": tallySheetVersion.submission.election.get_official_name()
            },
            "stamp": {
                "createdAt": stamp.createdAt,
                "createdBy": stamp.createdBy,
                "barcodeString": stamp.barcodeString
            },
            "tallySheetCode": "CE/RO/PR/1",
            "electoralDistrict": Area.get_associated_areas(
                tallySheetVersion.submission.area, AreaTypeEnum.ElectoralDistrict)[0].areaName,
            "pollingDivision": pollingDivision,
            "partyName": candidate_and_area_wise_valid_vote_count_result["partyName"].values[0],
            "data": [],
            "countingCentres": [],
            "totalVoteCounts": []
        }

        total_vote_count = 0

        # Append the area wise column totals
        for area_wise_valid_vote_count_result_item in area_wise_valid_vote_count_result.itertuples():
            content["countingCentres"].append(area_wise_valid_vote_count_result_item.areaName)
            content["totalVoteCounts"].append(
                to_comma_seperated_num(area_wise_valid_vote_count_result_item.numValue))



        if tallySheetVersion.submission.election.voteType == Postal:
            content["tallySheetCode"] = "CE/RO/PR/1"

        number_of_counting_centres = len(area_wise_vote_count_result)

        for candidate_wise_valid_vote_count_result_item_index, candidate_wise_valid_vote_count_result_item in candidate_wise_valid_vote_count_result.iterrows():
            data_row = []
            total_votes_for_each_candidate = 0

            data_row_number = candidate_wise_valid_vote_count_result_item_index + 1
            data_row.append(data_row_number)

            for counting_centre_index in range(number_of_counting_centres):
                candidate_and_area_wise_valid_vote_count_result_item_index = \
                    (
                            number_of_counting_centres * candidate_wise_valid_vote_count_result_item_index) + counting_centre_index

                candidate_area_vote = candidate_and_area_wise_valid_vote_count_result["numValue"].values[
                                               candidate_and_area_wise_valid_vote_count_result_item_index]
                data_row.append(to_comma_seperated_num(candidate_area_vote))

                if candidate_area_vote is not None and not math.isnan(candidate_area_vote):
                    total_votes_for_each_candidate += candidate_area_vote

            data_row.append(to_comma_seperated_num(total_votes_for_each_candidate))

            total_vote_count += total_votes_for_each_candidate

            content["data"].append(data_row)

        content["totalVoteCounts"].append(to_comma_seperated_num(total_vote_count))


        html = render_template(
            'PE-CE-RO-PR-1.html',
            content=content
        )

        return html
