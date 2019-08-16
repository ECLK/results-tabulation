from flask import render_template
from sqlalchemy import func

from app import db
from exception import NotFoundException
from orm.entities import ReportVersion
from orm.entities.Result.PartyWiseResult import PartyCount
from orm.entities.Submission.Report import Report_PRE_30_ED
from orm.enums import ReportCodeEnum, AreaTypeEnum


class ReportVersion_PRE_30_ED_Model(ReportVersion.Model):

    def __init__(self, reportId):
        report = Report_PRE_30_ED.get_by_id(reportId=reportId)
        if report is None:
            raise NotFoundException("Report not found. (reportId=%d)" % reportId)

        partyWiseResultIds = []
        for countingCentre in report.area.get_associated_areas(AreaTypeEnum.CountingCentre):
            for tallySheet in countingCentre.tallySheets_PRE_41:
                partyWiseResultIds.append(tallySheet.latestVersion.partyWiseResultId)

        print("\n\n============================= partyWiseResultIds \n\n", partyWiseResultIds)

        queryResult = db.session.query(
            func.sum(PartyCount.Model.count).label("count"),
            PartyCount.Model.partyId.label("partyId")
        ).filter(
            PartyCount.Model.partyWiseResultId.in_(partyWiseResultIds)
        ).group_by(
            PartyCount.Model.partyId
        ).all()

        content = {
            "title": "PRESIDENTIAL ELECTION ACT NO. 15 OF 1981",
            "electoralDistrict": "1. Matara",
            "pollingDivision": "Division 1",
            "pollingDistrictNos": "1, 2, 3, 4",
            "countingHallNo": report.area.areaName,
            "data": [
            ],
            "total": 3000,
            "rejectedVotes": 50,
            "grandTotal": 3050
        }

        for row_index in range(len(queryResult)):
            row = queryResult[row_index]
            content["data"].append([
                row_index + 1,
                "candidate.candidateName",
                row[0],
                row[1],
                "N/A"
            ])

        html = render_template(
            'pre-41.html',
            content=content
        )

        super(ReportVersion_PRE_30_ED_Model, self).__init__(reportId=reportId, html=html)

    __mapper_args__ = {
        'polymorphic_identity': ReportCodeEnum.PRE_30_ED
    }


Model = ReportVersion_PRE_30_ED_Model


def get_by_id(reportVersionId):
    result = Model.query.filter(
        Model.reportVersionId == reportVersionId
    ).one_or_none()

    return result


def create(reportId):
    result = Model(reportId=reportId)

    return result
