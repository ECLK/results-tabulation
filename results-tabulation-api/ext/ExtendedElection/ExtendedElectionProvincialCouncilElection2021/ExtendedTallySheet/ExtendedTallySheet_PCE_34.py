from flask import render_template

from constants.VOTE_TYPES import NonPostal
from ext.ExtendedTallySheet import ExtendedTallySheetDataEntry
from orm.entities import Area
from util import to_comma_seperated_num
from orm.enums import AreaTypeEnum


class ExtendedTallySheet_PCE_34(ExtendedTallySheetDataEntry):
    class ExtendedTallySheetVersion(ExtendedTallySheetDataEntry.ExtendedTallySheetVersion):

        def html(self, title="", total_registered_voters=None):
            tallySheetVersion = self.tallySheetVersion

            invalid_vote_category_counts = self.get_invalid_vote_category_count()

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
                "tallySheetCode": "PCE-39",
                "electoralDistrict": Area.get_associated_areas(
                    tallySheetVersion.tallySheet.area, AreaTypeEnum.ElectoralDistrict)[0].areaName,
                "pollingDivision": polling_division_name,
                "countingCentre": tallySheetVersion.tallySheet.area.areaName,
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
                'PCE-39.html',
                content=content
            )

            return html
