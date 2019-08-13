from flask import render_template

from exception import NotFoundException
from orm.entities import ReportVersion
from orm.entities.Submission.Report import Report_PRE_41
from orm.entities.SubmissionVersion.TallySheetVersion import TallySheetVersionPRE41
from orm.enums import ReportCodeEnum


class ReportVersion_PRE_41_Model(ReportVersion.Model):

    def __init__(self, reportId):
        report = Report_PRE_41.get_by_id(reportId=reportId)
        if report is None:
            raise NotFoundException("Report not found. (reportId=%d)" % reportId)

        print("$$$$$$$$$$$$$$$$$$$", [report.tallySheet.tallySheetId, report.tallySheet.versions])

        tallySheetContent = TallySheetVersionPRE41.get_by_id(
            tallySheetId=report.tallySheet.tallySheetId,
            tallySheetVersionId=report.tallySheet.latestVersionId
        ).tallySheetContent

        data = []

        for row in tallySheetContent:
            data.append([
                row.partyWiseResultId,
                row.partyId,
                row.count,
                row.countInWords
            ])

        html = render_template(
            'test-report-template.html',
            title="Test Template PRE-41",
            data=data
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
