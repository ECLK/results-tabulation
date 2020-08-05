from flask import render_template
from ext.ExtendedTallySheet import ExtendedTallySheetReport
from orm.entities import Area
from constants.VOTE_TYPES import Postal
from util import to_comma_seperated_num
from orm.enums import AreaTypeEnum


class ExtendedTallySheet_PRE_30_ED(ExtendedTallySheetReport):
    class ExtendedTallySheetVersion(ExtendedTallySheetReport.ExtendedTallySheetVersion):

        def html_letter(self, title="", total_registered_voters=None, signatures=[]):
            return super(ExtendedTallySheet_PRE_30_ED.ExtendedTallySheetVersion, self).html_letter(
                title="Results of Electoral District %s" % self.tallySheetVersion.submission.area.areaName
            )

        def html(self, title="", total_registered_voters=None):
            tallySheetVersion = self.tallySheetVersion

            candidate_and_area_wise_valid_non_postal_vote_count_result = self.get_candidate_and_area_wise_valid_non_postal_vote_count_result()
            area_wise_valid_non_postal_vote_count_result = self.get_area_wise_valid_non_postal_vote_count_result()
            area_wise_rejected_non_postal_vote_count_result = self.get_area_wise_rejected_non_postal_vote_count_result()
            area_wise_non_postal_vote_count_result = self.get_area_wise_non_postal_vote_count_result()

            candidate_wise_valid_postal_vote_count_result = self.get_candidate_wise_valid_postal_vote_count_result()
            postal_vote_count_result = self.get_postal_vote_count_result()
            postal_valid_vote_count_result = self.get_postal_valid_vote_count_result()
            postal_rejected_vote_count_result = self.get_postal_rejected_vote_count_result()

            candidate_wise_valid_vote_count_result = self.get_candidate_wise_valid_vote_count_result()
            vote_count_result = self.get_vote_count_result()
            valid_vote_count_result = self.get_valid_vote_count_result()
            rejected_vote_count_result = self.get_rejected_vote_count_result()

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
                "tallySheetCode": "PRE/30/PD",
                "electoralDistrict": Area.get_associated_areas(
                    tallySheetVersion.submission.area, AreaTypeEnum.ElectoralDistrict)[0].areaName,
                "pollingDivision": pollingDivision,
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
            for area_wise_valid_non_postal_vote_count_result_item in area_wise_valid_non_postal_vote_count_result.itertuples():
                content["pollingDivisions"].append(area_wise_valid_non_postal_vote_count_result_item.areaName)
                content["validVoteCounts"].append(
                    to_comma_seperated_num(area_wise_valid_non_postal_vote_count_result_item.numValue))
                total_valid_vote_count += area_wise_valid_non_postal_vote_count_result_item.numValue

            for area_wise_rejected_non_postal_vote_count_result_item_index, area_wise_rejected_non_postal_vote_count_result_item in area_wise_rejected_non_postal_vote_count_result.iterrows():
                content["rejectedVoteCounts"].append(
                    to_comma_seperated_num(area_wise_rejected_non_postal_vote_count_result_item.numValue))
                total_rejected_vote_count += area_wise_rejected_non_postal_vote_count_result_item.numValue

            for area_wise_non_postal_vote_count_result_item_index, area_wise_non_postal_vote_count_result_item in area_wise_non_postal_vote_count_result.iterrows():
                content["totalVoteCounts"].append(
                    to_comma_seperated_num(area_wise_non_postal_vote_count_result_item.numValue))
                total_vote_count += area_wise_non_postal_vote_count_result_item.numValue

            # Append the postal vote count totals
            content["validVoteCounts"].append(
                to_comma_seperated_num(postal_valid_vote_count_result["numValue"].values[0]))
            content["rejectedVoteCounts"].append(
                to_comma_seperated_num(postal_rejected_vote_count_result["numValue"].values[0]))
            content["totalVoteCounts"].append(to_comma_seperated_num(postal_vote_count_result["numValue"].values[0]))

            # Append the grand totals
            content["validVoteCounts"].append(to_comma_seperated_num(valid_vote_count_result["numValue"].values[0]))
            content["rejectedVoteCounts"].append(
                to_comma_seperated_num(rejected_vote_count_result["numValue"].values[0]))
            content["totalVoteCounts"].append(to_comma_seperated_num(vote_count_result["numValue"].values[0]))

            number_of_counting_centres = len(area_wise_non_postal_vote_count_result)

            for candidate_wise_valid_vote_count_result_item_index, candidate_wise_valid_vote_count_result_item in candidate_wise_valid_vote_count_result.iterrows():
                data_row = []

                data_row_number = candidate_wise_valid_vote_count_result_item_index + 1
                data_row.append(data_row_number)

                data_row.append(candidate_wise_valid_vote_count_result_item.candidateName)

                for counting_centre_index in range(number_of_counting_centres):
                    candidate_and_area_wise_valid_non_postal_vote_count_result_item_index = \
                        (
                                number_of_counting_centres * candidate_wise_valid_vote_count_result_item_index) + counting_centre_index

                    data_row.append(
                        to_comma_seperated_num(
                            candidate_and_area_wise_valid_non_postal_vote_count_result["numValue"].values[
                                candidate_and_area_wise_valid_non_postal_vote_count_result_item_index]))

                data_row.append(to_comma_seperated_num(candidate_wise_valid_postal_vote_count_result["numValue"].values[
                                                           candidate_wise_valid_vote_count_result_item_index]))

                data_row.append(to_comma_seperated_num(candidate_wise_valid_vote_count_result_item.numValue))

                content["data"].append(data_row)

            html = render_template(
                'PRE-30-ED.html',
                content=content
            )

            return html
