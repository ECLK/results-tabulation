from flask import render_template
from sqlalchemy.ext.hybrid import hybrid_property

from app import db
from sqlalchemy.orm import relationship
from sqlalchemy import func

from exception import NotFoundException
from orm.entities import ReportVersion, Party, Candidate
from orm.entities.Election import ElectionParty, ElectionCandidate
from orm.entities.Result.PartyWiseResult import PartyCount
from orm.entities.Submission.Report import Report_PRE_30_PD, Report_PRE_41
from orm.enums import ReportCodeEnum, AreaTypeEnum


class ReportVersion_PRE_30_PD_Model(ReportVersion.Model):

    def __init__(self, reportId):
        report = Report_PRE_30_PD.get_by_id(reportId=reportId)
        if report is None:
            raise NotFoundException("Report not found. (reportId=%d)" % reportId)

        partyWiseResultIds = []
        for countingCentre in report.area.get_associated_areas(AreaTypeEnum.CountingCentre):
            for tallySheet in countingCentre.tallySheets_PRE_41:
                partyWiseResultIds.append(tallySheet.latestVersion.partyWiseResultId)

        queryResult = db.session.query(
            func.sum(PartyCount.Model.count).label("count"),
            PartyCount.Model.partyId.label("partyId"),
            PartyCount.Model.countInWords.label("countInWords")
        ).filter(
            PartyCount.Model.partyWiseResultId.in_([4])
        ).group_by(
            PartyCount.Model.partyId
        ).all()

        aggregatedPartyCount = db.session.query(
            func.sum(PartyCount.Model.count).label("count"),
            PartyCount.Model.partyId.label("partyId")
        ).filter(
            PartyCount.Model.partyWiseResultId.in_(partyWiseResultIds)
        ).group_by(
            PartyCount.Model.partyId
        ).subquery()

        queryResult = db.session.query(
            ElectionParty.Model.partyId,
            Party.Model.partyName,
            Party.Model.partySymbol,
            Party.Model.partySymbolFileId,
            ElectionCandidate.Model.candidateId,
            Candidate.Model.candidateName,
            Candidate.Model.candidateProfileImageFileId,
            aggregatedPartyCount.c.count
        ).join(
            Party.Model,
            Party.Model.partyId == ElectionParty.Model.partyId,
            isouter=True
        ).join(
            ElectionCandidate.Model,
            ElectionCandidate.Model.partyId == ElectionParty.Model.partyId,
            isouter=True
        ).join(
            Candidate.Model,
            Candidate.Model.candidateId == ElectionCandidate.Model.candidateId,
            isouter=True
        ).join(
            aggregatedPartyCount,
            aggregatedPartyCount.c.partyId == ElectionParty.Model.partyId,
            isouter=True
        ).filter(
            ElectionParty.Model.electionId == report.electionId,
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
                row[2]
            ])

        html = render_template(
            'pre-41.html',
            content=content
        )

        super(ReportVersion_PRE_30_PD_Model, self).__init__(reportId=reportId, html=html)

    __mapper_args__ = {
        'polymorphic_identity': ReportCodeEnum.PRE_30_PD
    }


Model = ReportVersion_PRE_30_PD_Model


def get_by_id(reportVersionId):
    result = Model.query.filter(
        Model.reportVersionId == reportVersionId
    ).one_or_none()

    return result


def create(reportId):
    result = Model(reportId=reportId)

    return result
