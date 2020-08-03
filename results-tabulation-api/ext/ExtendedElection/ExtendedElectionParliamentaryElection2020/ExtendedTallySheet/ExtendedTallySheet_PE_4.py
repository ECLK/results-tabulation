from flask import render_template

from constants.VOTE_TYPES import NonPostal
from ext.ExtendedTallySheet import ExtendedTallySheetDataEntry
from orm.entities import Area
from orm.enums import AreaTypeEnum
from util import to_comma_seperated_num


class ExtendedTallySheet_PE_4(ExtendedTallySheetDataEntry):
    class ExtendedTallySheetVersion(ExtendedTallySheetDataEntry.ExtendedTallySheetVersion):

        def html(self, title="", total_registered_voters=None):
            tallySheetVersion = self.tallySheetVersion

            candidate_and_area_wise_valid_vote_count = self.get_candidate_and_area_wise_valid_vote_count_result()

            noOfCandidates = candidate_and_area_wise_valid_vote_count.shape[0]
            noOfRows = round(noOfCandidates / 2)

            stamp = tallySheetVersion.stamp

            polling_divisions = Area.get_associated_areas(tallySheetVersion.submission.area,
                                                          AreaTypeEnum.PollingDivision)
            polling_division_name = ""
            if len(polling_divisions) > 0:
                polling_division_name = polling_divisions[0].areaName

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
                "tallySheetCode": "PE-4",
                "electoralDistrict": Area.get_associated_areas(
                    tallySheetVersion.submission.area, AreaTypeEnum.ElectoralDistrict)[0].areaName,
                "pollingDivision": polling_division_name,
                "countingCentre": tallySheetVersion.submission.area.areaName,
                "partyName": candidate_and_area_wise_valid_vote_count["partyName"].values[0],
                "data1": [],
                "data2": []
            }

            # Appending canditate wise vote count
            i = 0

            for index, row in candidate_and_area_wise_valid_vote_count.iterrows():

                if i < noOfRows:
                    data_row1 = []
                    data_row1.append(row.candidateName)
                    data_row1.append(row.strValue)
                    data_row1.append(to_comma_seperated_num(row.numValue))
                    content["data1"].append(data_row1)
                    i += 1
                else:
                    data_row2 = []
                    data_row2.append(row.candidateName)
                    print(row.candidateName)
                    data_row2.append(row.strValue)
                    data_row2.append(to_comma_seperated_num(row.numValue))
                    content["data2"].append(data_row2)

            html = render_template(
                'PE-4.html',
                content=content
            )

            return html
