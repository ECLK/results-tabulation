from flask import render_template
from ext.ExtendedTallySheetVersion import ExtendedTallySheetVersion
from orm.entities import Area
from constants.VOTE_TYPES import Postal
from util import to_comma_seperated_num
from orm.enums import AreaTypeEnum


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

        # Append the area wise column totals
        for area_wise_valid_vote_count_result_item in area_wise_valid_vote_count_result.itertuples():
            content["countingCentres"].append(area_wise_valid_vote_count_result_item.areaName)
            content["totalVoteCounts"].append(
                to_comma_seperated_num(area_wise_valid_vote_count_result_item.incompleteNumValue))

        for index_1 in candidate_wise_valid_vote_count_result.index:
            data_row = []

            candidate_id = candidate_wise_valid_vote_count_result.at[index_1, "candidateId"]
            candidate_number = candidate_wise_valid_vote_count_result.at[index_1, "candidateNumber"]

            data_row.append(candidate_number)

            for index_2 in candidate_and_area_wise_valid_vote_count_result.index:
                if candidate_and_area_wise_valid_vote_count_result.at[index_2, "candidateId"] == candidate_id:
                    data_row.append(to_comma_seperated_num(
                        candidate_and_area_wise_valid_vote_count_result.at[index_2, "numValue"]
                    ))

            data_row.append(to_comma_seperated_num(
                candidate_wise_valid_vote_count_result.at[index_1, "incompleteNumValue"]
            ))

            content["data"].append(data_row)

        content["totalVoteCounts"].append(to_comma_seperated_num(
            candidate_wise_valid_vote_count_result["numValue"].sum()
        ))

        html = render_template(
            'PE-CE-RO-PR-1.html',
            content=content
        )

        return html
