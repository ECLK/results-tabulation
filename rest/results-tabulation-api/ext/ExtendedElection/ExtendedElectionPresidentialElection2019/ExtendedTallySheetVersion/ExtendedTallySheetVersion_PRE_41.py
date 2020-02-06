from flask import render_template
from ext.ExtendedTallySheetVersion import ExtendedTallySheetVersion
from orm.entities import Area
from util import to_comma_seperated_num
from orm.enums import AreaTypeEnum


class ExtendedTallySheetVersion_PRE_41(ExtendedTallySheetVersion):

    def __init__(self, tallySheetVersion):
        super(ExtendedTallySheetVersion_PRE_41, self).__init__(tallySheetVersion)

    def html_letter(self, title="", total_registered_voters=None):
        return super(ExtendedTallySheetVersion_PRE_41, self).html_letter(
            title="Results of Electoral District %s" % self.tallySheetVersion.submission.area.areaName
        )

    def html(self, title="", total_registered_voters=None):
        tallySheetVersion = self.tallySheetVersion
        tallySheetContent = tallySheetVersion.content

        stamp = tallySheetVersion.stamp

        polling_divisions = Area.get_associated_areas(tallySheetVersion.submission.area, AreaTypeEnum.PollingDivision)
        polling_division_name = ""
        if len(polling_divisions) > 0:
            polling_division_name = polling_divisions[0].areaName

        content = {
            "election": {
                "electionName": tallySheetVersion.submission.election.get_official_name()
            },
            "stamp": {
                "createdAt": stamp.createdAt,
                "createdBy": stamp.createdBy,
                "barcodeString": stamp.barcodeString
            },
            "title": "PRESIDENTIAL ELECTION ACT NO. 15 OF 1981",
            "electoralDistrict": Area.get_associated_areas(
                tallySheetVersion.submission.area, AreaTypeEnum.ElectoralDistrict)[0].areaName,
            "pollingDivision": polling_division_name,
            "countingCentre": tallySheetVersion.submission.area.areaName,
            "pollingDistrictNos": ", ".join([
                pollingDistrict.areaName for pollingDistrict in
                Area.get_associated_areas(tallySheetVersion.submission.area, AreaTypeEnum.PollingDistrict)
            ]),
            "data": [
            ],
            "total": 0,
            "rejectedVotes": 0,
            "grandTotal": 0
        }

        for row_index in range(len(tallySheetContent)):
            row = tallySheetContent[row_index]
            if row.templateRowType == "CANDIDATE_FIRST_PREFERENCE":
                content["data"].append([
                    row_index + 1,
                    row.candidateName,
                    row.partySymbol,
                    "" if row.strValue is None else row.strValue,
                    "" if row.numValue is None else to_comma_seperated_num(row.numValue),
                    ""
                ])
                content["total"] += 0 if row.numValue is None else row.numValue
                content["grandTotal"] += 0 if row.numValue is None else row.numValue
            elif row.templateRowType == "REJECTED_VOTE":
                content["rejectedVotes"] += 0 if row.numValue is None else row.numValue
                content["grandTotal"] += 0 if row.numValue is None else row.numValue

        content["total"] = to_comma_seperated_num(content["total"])
        content["rejectedVotes"] = to_comma_seperated_num(content["rejectedVotes"])
        content["grandTotal"] = to_comma_seperated_num(content["grandTotal"])

        html = render_template(
            'PRE-41.html',
            content=content
        )

        return html
