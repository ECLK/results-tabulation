from flask import render_template
from ext.ExtendedTallySheetVersion import ExtendedTallySheetVersion
from orm.entities import Area
from constants.VOTE_TYPES import Postal
from util import to_comma_seperated_num
from orm.enums import AreaTypeEnum


class ExtendedTallySheetVersion_PE_4(ExtendedTallySheetVersion):

    def html_letter(self, title="", total_registered_voters=None):
        return super(ExtendedTallySheetVersion_PE_4, self).html_letter(
            title="Results of Electoral District %s" % self.tallySheetVersion.submission.area.areaName
        )

    def html(self, title="", total_registered_voters=None):
        tallySheetVersion = self.tallySheetVersion

        candidate_and_area_wise_valid_vote_count = self.get_candidate_and_area_wise_valid_vote_count_result()

        noOfCandidates = candidate_and_area_wise_valid_vote_count.shape[0]
        noOfRows = round(noOfCandidates/2)

        stamp = tallySheetVersion.stamp

        polling_divisions = Area.get_associated_areas(tallySheetVersion.submission.area, AreaTypeEnum.PollingDivision)
        polling_division_name = ""
        if len(polling_divisions) > 0:
            polling_division_name = polling_divisions[0].areaName

        if tallySheetVersion.submission.election.voteType == Postal:
            polling_division_name = 'Postal'

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

        #Appending canditate wise vote count
        i=0

        for index, row in candidate_and_area_wise_valid_vote_count.iterrows():

            if i < noOfRows:
                data_row1 = []
                data_row1.append(row.candidateName)
                data_row1.append(row.strValue)
                data_row1.append(row.numValue)
                content["data1"].append(data_row1)
                i += 1
            else:
                data_row2 = []
                data_row2.append(row.candidateName)
                print(row.candidateName)
                data_row2.append(row.strValue)
                data_row2.append(row.numValue)
                content["data2"].append(data_row2)


        html = render_template(
            'PE-4.html',
            content=content
        )

        return html
