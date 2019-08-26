from flask import render_template

from exception import NotFoundException, ForbiddenException
from orm.entities import ReportVersion, Area
from orm.entities.Submission.Report import Report_PRE_41
from orm.enums import ReportCodeEnum, AreaTypeEnum


class ReportVersion_PRE_41_Model(ReportVersion.Model):

    def __init__(self, reportId):
        report = Report_PRE_41.get_by_id(reportId=reportId)
        if report is None:
            raise NotFoundException("Report not found. (reportId=%d)" % reportId)

        if len(report.area.tallySheets_PRE_41) is 0:
            raise ForbiddenException(
                "There's no PRE-41 tally sheet for the counting centre (officeId)" % report.area.areaId)
        elif len(report.area.tallySheets_PRE_41) > 1:
            raise ForbiddenException(
                "There's more than one PRE-41 tally sheet for the counting centre (officeId)" % report.area.areaId)

        tallySheet = report.area.tallySheets_PRE_41[0]
        latestVersion = tallySheet.latestVersion

        if latestVersion is None:
            raise NotFoundException("No tallysheet data filled yet. (tallySheetId=%d)" % tallySheet.tallySheetId)

        tallySheetContent = latestVersion.content

        content = {
            "title": "PRESIDENTIAL ELECTION ACT NO. 15 OF 1981",
            "electoralDistrict": Area.get_associated_areas(report.area, AreaTypeEnum.ElectoralDistrict)[0].areaName,
            "pollingDivision": Area.get_associated_areas(report.area, AreaTypeEnum.PollingDivision)[0].areaName,
            "pollingDistrictNos": ", ".join([
                pollingDistrict.areaName for pollingDistrict in
                Area.get_associated_areas(report.area, AreaTypeEnum.PollingDistrict)
            ]),
            "countingHallNo": report.area.areaName,
            "data": [
            ],
            "total": 0,
            "rejectedVotes": 0,
            "grandTotal": 0
        }

        for row_index in range(len(tallySheetContent)):
            row = tallySheetContent[row_index]
            if row.count is not None:
                content["data"].append([
                    row_index + 1,
                    row.candidateName,
                    row.partySymbol,
                    row.countInWords,
                    row.count,
                    ""
                ])
                content["total"] = content["total"] + row.count
            else:
                content["data"].append([
                    row_index + 1,
                    row.candidateName,
                    row.partySymbol,
                    "",
                    "",
                    ""
                ])

        content["rejectedVotes"] = 0  # TODO
        content["grandTotal"] = content["total"] + content["rejectedVotes"]

        html = render_template(
            'pre-41.html',
            content=content
        )

        super(ReportVersion_PRE_41_Model, self).__init__(reportId=reportId, html=html)

    __mapper_args__ = {
        'polymorphic_identity': ReportCodeEnum.PRE_41
    }


Model = ReportVersion_PRE_41_Model


def get_by_id(reportVersionId):
    result = Model.query.filter(
        Model.reportVersionId == reportVersionId
    ).one_or_none()

    return result


def create(reportId):
    result = Model(reportId=reportId)

    return result
