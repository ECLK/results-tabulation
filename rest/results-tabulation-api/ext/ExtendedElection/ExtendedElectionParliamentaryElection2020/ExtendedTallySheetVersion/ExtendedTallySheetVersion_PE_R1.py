from flask import render_template
from ext.ExtendedTallySheetVersion import ExtendedTallySheetVersion
from orm.entities import Area
from constants.VOTE_TYPES import Postal
from util import to_comma_seperated_num
from orm.enums import AreaTypeEnum


class ExtendedTallySheetVersion_PE_R1(ExtendedTallySheetVersion):

    def html_letter(self, title="", total_registered_voters=None):
        return super(ExtendedTallySheetVersion_PE_R1, self).html_letter(
            title="Results of Polling Division %s" % self.tallySheetVersion.submission.area.areaName,
            total_registered_voters=float(get_polling_division_total_registered_voters(tallySheetVersion=self))
        )

    def html(self, title="", total_registered_voters=None):
        tallySheetVersion = self.tallySheetVersion

        party_and_area_wise_valid_vote_count_result = self.get_party_and_area_wise_valid_vote_count_result()
        party_wise_valid_vote_count_result = self.get_party_wise_valid_vote_count_result()
        area_wise_valid_vote_count_result = self.get_area_wise_valid_vote_count_result()
        area_wise_rejected_vote_count_result = self.get_area_wise_rejected_vote_count_result()
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
            "tallySheetCode": "PE/R1",
            "electoralDistrict": Area.get_associated_areas(
                tallySheetVersion.submission.area, AreaTypeEnum.ElectoralDistrict)[0].areaName,
            "pollingDivision": pollingDivision,
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
            total_valid_vote_count += area_wise_valid_vote_count_result_item.numValue

        for area_wise_rejected_vote_count_result_item_index, area_wise_rejected_vote_count_result_item in area_wise_rejected_vote_count_result.iterrows():
            total_rejected_vote_count += area_wise_rejected_vote_count_result_item.numValue

        for area_wise_vote_count_result_item_index, area_wise_vote_count_result_item in area_wise_vote_count_result.iterrows():
            total_vote_count += area_wise_vote_count_result_item.numValue

        # Append the grand totals
        content["validVoteCounts"].append(to_comma_seperated_num(total_valid_vote_count))
        content["rejectedVoteCounts"].append(to_comma_seperated_num(total_rejected_vote_count))
        content["totalVoteCounts"].append(to_comma_seperated_num(total_vote_count))

        if tallySheetVersion.submission.election.voteType == Postal:
            content["tallySheetCode"] = "PE/R1"

        number_of_counting_centres = len(area_wise_vote_count_result)

        for party_wise_valid_vote_count_result_item_index, party_wise_valid_vote_count_result_item in party_wise_valid_vote_count_result.iterrows():
            data_row = []

            data_row_number = party_wise_valid_vote_count_result_item_index + 1
            data_row.append(data_row_number)

            data_row.append(party_wise_valid_vote_count_result_item.partyName)

            data_row.append(to_comma_seperated_num(party_wise_valid_vote_count_result_item.numValue))

            content["data"].append(data_row)

        html = render_template(
            'PE-R1.html',
            content=content
        )

        return html
