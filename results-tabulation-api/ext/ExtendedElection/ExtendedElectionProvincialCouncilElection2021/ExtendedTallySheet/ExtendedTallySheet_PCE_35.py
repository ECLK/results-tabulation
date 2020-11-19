from flask import render_template

from constants.VOTE_TYPES import NonPostal
from ext.ExtendedTallySheet import ExtendedTallySheetDataEntry
from orm.entities import Area
from util import to_comma_seperated_num
from orm.enums import AreaTypeEnum


class ExtendedTallySheet_PCE_35(ExtendedTallySheetDataEntry):
    class ExtendedTallySheetVersion(ExtendedTallySheetDataEntry.ExtendedTallySheetVersion):

        def html(self, title="", total_registered_voters=None):
            tallySheetVersion = self.tallySheetVersion
            tallySheetContent = tallySheetVersion.content

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
                "title": "PRESIDENTIAL ELECTION ACT NO. 15 OF 1981",
                "electoralDistrict": Area.get_associated_areas(
                    tallySheetVersion.tallySheet.area, AreaTypeEnum.ElectoralDistrict)[0].areaName,
                "pollingDivision": polling_division_name,
                "countingCentre": tallySheetVersion.tallySheet.area.areaName,
                "pollingDistrictNos": ", ".join([
                    pollingDistrict.areaName for pollingDistrict in
                    Area.get_associated_areas(tallySheetVersion.tallySheet.area, AreaTypeEnum.PollingDistrict)
                ]),
                "data": [
                ],
                "total": 0,
                "rejectedVotes": 0,
                "grandTotal": 0
            }

            party_wise_results = self.df.loc[self.df.templateRowType == "PARTY_WISE_VOTE"].sort_values(
                by=["electionPartyId"], ascending=[True]
            )
            rejected_vote_count_results = self.df.loc[self.df.templateRowType == "REJECTED_VOTE"]

            for party_wise_result in party_wise_results.itertuples():
                content["data"].append([
                    len(content["data"]) + 1,
                    party_wise_result.partyName,
                    party_wise_result.partySymbol,
                    "" if party_wise_result.strValue is None else party_wise_result.strValue,
                    "" if party_wise_result.numValue is None else to_comma_seperated_num(party_wise_result.numValue),
                    ""
                ])
                content["total"] += 0 if party_wise_result.numValue is None else party_wise_result.numValue
                content["grandTotal"] += 0 if party_wise_result.numValue is None else party_wise_result.numValue

            for rejected_vote_count_result in rejected_vote_count_results.itertuples():
                content[
                    "rejectedVotes"] += 0 if rejected_vote_count_result.numValue is None else rejected_vote_count_result.numValue
                content[
                    "grandTotal"] += 0 if rejected_vote_count_result.numValue is None else rejected_vote_count_result.numValue

            content["total"] = to_comma_seperated_num(content["total"])
            content["rejectedVotes"] = to_comma_seperated_num(content["rejectedVotes"])
            content["grandTotal"] = to_comma_seperated_num(content["grandTotal"])

            html = render_template(
                'PCE-27.html',
                content=content
            )

            return html
