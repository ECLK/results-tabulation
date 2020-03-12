from flask import render_template
from ext.ExtendedTallySheet import ExtendedTallySheet
from orm.entities import Area
from constants.VOTE_TYPES import Postal
from util import to_comma_seperated_num
from orm.enums import AreaTypeEnum


class ExtendedTallySheet_PE_39(ExtendedTallySheet):
    class ExtendedTallySheetVersion(ExtendedTallySheet.ExtendedTallySheetVersion):

        def __init__(self, tallySheetVersion):
            super(ExtendedTallySheet_PE_39.ExtendedTallySheetVersion, self).__init__(tallySheetVersion)

        #
        # def html_letter(self, title="", total_registered_voters=None):
        #     # TODO: implement
        #     pass
        #
        def html(self, title="", total_registered_voters=None):
            tallySheetVersion = self.tallySheetVersion

            invalid_vote_category_counts = self.get_invalid_vote_category_count()

            stamp = tallySheetVersion.stamp

            polling_divisions = Area.get_associated_areas(tallySheetVersion.submission.area,
                                                          AreaTypeEnum.PollingDivision)
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
                "tallySheetCode": "PE-39",
                "electoralDistrict": Area.get_associated_areas(
                    tallySheetVersion.submission.area, AreaTypeEnum.ElectoralDistrict)[0].areaName,
                "pollingDivision": polling_division_name,
                "countingCentre": tallySheetVersion.submission.area.areaName,
                "data": [],
                "rejectedVotes": 0
            }

            total_rejected_count = 0
            for index, invalid_vote_category_count in invalid_vote_category_counts.iterrows():
                data_row = []
                data_row.append(invalid_vote_category_count.invalidVoteCategoryDescription)
                data_row.append(invalid_vote_category_count.numValue)
                content["data"].append(data_row)
                total_rejected_count += invalid_vote_category_count.numValue

            content["rejectedVotes"] = to_comma_seperated_num(total_rejected_count)

            html = render_template(
                'PE-39.html',
                content=content
            )

            return html
