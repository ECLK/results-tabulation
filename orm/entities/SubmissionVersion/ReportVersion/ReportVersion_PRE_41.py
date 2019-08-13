from flask import render_template

from exception import NotFoundException, ForbiddenException
from orm.entities import ReportVersion
from orm.entities.Submission.Report import Report_PRE_41
from orm.entities.SubmissionVersion.TallySheetVersion import TallySheetVersionPRE41
from orm.enums import ReportCodeEnum


class ReportVersion_PRE_41_Model(ReportVersion.Model):

    def __init__(self, reportId):
        report = Report_PRE_41.get_by_id(reportId=reportId)
        if report is None:
            raise NotFoundException("Report not found. (reportId=%d)" % reportId)

        tallySheetContent = TallySheetVersionPRE41.get_by_id(
            tallySheetId=report.tallySheet.tallySheetId,
            tallySheetVersionId=report.tallySheet.latestVersionId
        ).tallySheetContent

        content = {
                "title": "PRESIDENTIAL ELECTION ACT NO. 15 OF 1981",
                "electoralDistrict": "1. Matara",
                "pollingDivision": "Division 1",
                "pollingDistrictNos": "1, 2, 3, 4",
                "countingHallNo": report.area.areaName,
                "data": [
                    # [1, "Yujith Waraniyagoda", "Moon", "Five Hundred", 500, "Saman"],
                    # [2, "Clement Fernando", "Bottle", "Five Hundred", 500, "Saman"],
                    # [3, "Umayanga Gunewardena", "Python", "Five Hundred", 500, "Saman"],
                    # [4, "Sherazad Hamit", "Hammer", "Five Hundred", 500, "Saman"],
                    # [5, "Anushka", "Carrot", "Five Hundred", 500, "Saman"],
                    # [6, "Samudra Weerasinghe", "Fish", "Five Hundred", 500, "Saman"]
                ],
                "total": 3000,
                "rejectedVotes": 50,
                "grandTotal": 3050
            }

        for row_index in range(len(tallySheetContent)):
            row = tallySheetContent[row_index]
            if len(row.party.candidates) is 0:
                raise ForbiddenException("Each party must be having at least one candidate. (partyId=%d)" % row.partyId)

            candidate = row.party.candidates[0]

            content["data"].append([
                row_index + 1,
                candidate.candidateName,
                row.party.partySymbol,
                row.countInWords,
                row.count,
                ""
            ])

        html = render_template(
            'pre-41.html',
            content=content
        )

        # html = render_template(
        #     'test-report-template.html',
        #     title="Test Template PRE-41",
        #     data=data
        # )

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
