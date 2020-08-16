import math

from flask import render_template
from ext.ExtendedTallySheet import ExtendedTallySheetReport
from orm.entities import Area
from orm.enums import AreaTypeEnum


class ExtendedTallySheet_PE_CE_RO_PR_3(ExtendedTallySheetReport):
    class ExtendedTallySheetVersion(ExtendedTallySheetReport.ExtendedTallySheetVersion):

        def html(self, title="", total_registered_voters=None):
            tallySheetVersion = self.tallySheetVersion

            candidate_wise_valid_vote_count_result = self.get_candidate_wise_valid_vote_count_result()

            stamp = tallySheetVersion.stamp

            content = {
                "election": {
                    "electionName": tallySheetVersion.tallySheet.election.get_official_name()
                },
                "stamp": {
                    "createdAt": stamp.createdAt,
                    "createdBy": stamp.createdBy,
                    "barcodeString": stamp.barcodeString
                },
                "tallySheetCode": "CE/RO/PR/1",
                "electoralDistrict": Area.get_associated_areas(
                    tallySheetVersion.tallySheet.area, AreaTypeEnum.ElectoralDistrict)[0].areaName,
                "partyName": candidate_wise_valid_vote_count_result["partyName"].values[0],
                "data": []
            }

            candidate_wise_valid_vote_count_result = candidate_wise_valid_vote_count_result.sort_values(
                by=['numValue'], ascending=False)

            position_of_candidate = 0
            for index_1 in candidate_wise_valid_vote_count_result.index:
                data_row = []

                position_of_candidate += 1
                candidate_id = candidate_wise_valid_vote_count_result.at[index_1, "candidateId"]
                candidate_number = candidate_wise_valid_vote_count_result.at[index_1, "candidateNumber"]
                candidate_name = candidate_wise_valid_vote_count_result.at[index_1, "candidateName"]
                num_value = candidate_wise_valid_vote_count_result.at[index_1, "numValue"]

                data_row.append(position_of_candidate)
                data_row.append("%s - %s" % (candidate_number, candidate_name))
                data_row.append("" if math.isnan(num_value) else num_value)
                data_row.append("")
                data_row.append(position_of_candidate)

                content["data"].append(data_row)

            html = render_template(
                'PE-CE-RO-PR-3.html',
                content=content
            )

            return html
