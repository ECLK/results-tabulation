from flask import render_template

from constants.VOTE_TYPES import NonPostal
from ext.ExtendedTallySheet import ExtendedTallySheetDataEntry
from orm.entities import Area
from orm.enums import AreaTypeEnum
from util import to_comma_seperated_num
import math

class ExtendedTallySheet_PCE_CE_CO_PR_4(ExtendedTallySheetDataEntry):
    class ExtendedTallySheetVersion(ExtendedTallySheetDataEntry.ExtendedTallySheetVersion):

        def html(self, title="", total_registered_voters=None):
            tallySheetVersion = self.tallySheetVersion

            candidate_and_area_wise_valid_vote_count = self.get_candidate_and_area_wise_valid_vote_count_result()

            noOfCandidates = candidate_and_area_wise_valid_vote_count.shape[0]
            noOfRows = math.ceil(noOfCandidates / 2)

            stamp = tallySheetVersion.stamp

            polling_divisions = Area.get_associated_areas(tallySheetVersion.tallySheet.area,
                                                          AreaTypeEnum.PollingDivision)
            polling_division_name = ""
            if len(polling_divisions) > 0:
                polling_division_name = polling_divisions[0].areaName

            if tallySheetVersion.tallySheet.election.voteType != NonPostal:
                polling_division_name = tallySheetVersion.tallySheet.election.voteType

            content = {
                "election": {
                    "electionName": tallySheetVersion.tallySheet.election.get_official_name()
                },
                "stamp": {
                    "createdAt": stamp.createdAt,
                    "createdBy": stamp.createdBy,
                    "barcodeString": stamp.barcodeString
                },
                "tallySheetCode": "PE-4",
                "electoralDistrict": Area.get_associated_areas(
                    tallySheetVersion.tallySheet.area, AreaTypeEnum.ElectoralDistrict)[0].areaName,
                "pollingDivision": polling_division_name,
                "countingCentre": tallySheetVersion.tallySheet.area.areaName,
                "partyName": candidate_and_area_wise_valid_vote_count["partyName"].values[0],
                "data1": [],
                "data2": []
            }

            # Appending canditate wise vote count
            i = 0

            for index, row in candidate_and_area_wise_valid_vote_count.iterrows():
                if i < noOfRows:
                    data_row1 = []
                    data_row1.append(row.candidateNumber)
                    data_row1.append(row.strValue)
                    data_row1.append(to_comma_seperated_num(row.numValue))
                    content["data1"].append(data_row1)
                    i += 1
                else:
                    data_row2 = []
                    data_row2.append(row.candidateNumber)
                    # print(row.candidateName)
                    data_row2.append(row.strValue)
                    data_row2.append(to_comma_seperated_num(row.numValue))
                    content["data2"].append(data_row2)

            html = render_template(
                'PE-4.html',
                content=content
            )

            return html
