import numpy
from flask import render_template
from sqlalchemy import func, and_
from sqlalchemy.sql import select

from app import db
from exception import NotFoundException
from orm.entities import ReportVersion, Party, Candidate, Submission, SubmissionVersion
from orm.entities.Area.Office import CountingCentre
from orm.entities.Election import ElectionParty, ElectionCandidate
from orm.entities.Result import CandidateWiseResult
from orm.entities.Result.CandidateWiseResult import CandidateCount
from orm.entities.Result.PartyWiseResult import PartyCount
from orm.entities.Submission.Report import Report_PRE_30_ED
from orm.entities.SubmissionVersion.TallySheetVersion import TallySheetVersionPRE41
from orm.enums import ReportCodeEnum, AreaTypeEnum


class ReportVersion_PRE_30_ED_Model(ReportVersion.Model):

    def __init__(self, reportId):
        report = Report_PRE_30_ED.get_by_id(reportId=reportId)
        if report is None:
            raise NotFoundException("Report not found. (reportId=%d)" % reportId)

        content = {
            "electoralDistrict": report.area.areaName,
            "pollingDivisions": [],
            "data": [],
            "validVotes": [],
            "rejectedVotes": 50,
            "grandTotal": 3050
        }

        pollingDivisions = []
        data = []

        candidates = db.session.query(
            ElectionCandidate.Model.candidateId,
            Candidate.Model.candidateName
        ).join(
            Candidate.Model,
            Candidate.Model.candidateId == ElectionCandidate.Model.candidateId
        ).order_by(
            ElectionCandidate.Model.candidateId
        ).all()

        for candidate in candidates:
            content["data"].append([candidate.candidateName])

        for pollingDivision in report.area.get_associated_areas(AreaTypeEnum.PollingDivision):
            content["pollingDivisions"].append(pollingDivision.areaName)
            latestTallySheetVersions = []
            for countingCentre in pollingDivision.get_associated_areas(AreaTypeEnum.CountingCentre):
                for tallySheet in countingCentre.tallySheets_PRE_41:
                    latestTallySheetVersions.append(tallySheet.latestVersionId)

            divisionWiseResult = db.session.query(
                ElectionCandidate.Model.candidateId,
                func.sum(CandidateCount.Model.count).label("count")
            ).join(
                CandidateCount.Model,
                CandidateCount.Model.candidateId == ElectionCandidate.Model.candidateId,
                isouter=True
            ).join(
                CandidateWiseResult.Model,
                CandidateWiseResult.Model.candidateWiseResultId == CandidateCount.Model.candidateWiseResultId,
                isouter=True
            ).join(
                TallySheetVersionPRE41.Model,
                and_(
                    TallySheetVersionPRE41.Model.candidateWiseResultId == CandidateWiseResult.Model.candidateWiseResultId,
                    TallySheetVersionPRE41.Model.tallySheetVersionId.in_(latestTallySheetVersions)
                ),
                isouter=True
            ).filter(
                ElectionCandidate.Model.electionId == report.electionId
            ).group_by(
                ElectionCandidate.Model.candidateId
            ).order_by(
                ElectionCandidate.Model.candidateId
            ).all()

            for divisionWiseResultIndex in range(len(divisionWiseResult)):
                if divisionWiseResult[divisionWiseResultIndex].count is not None:
                    content["data"][divisionWiseResultIndex].append(divisionWiseResult[divisionWiseResultIndex].count)
                else:
                    content["data"][divisionWiseResultIndex].append("")

        for data_row in content["data"]:
            data_row.append(sum(filter(lambda e: isinstance(e, int), data_row[1:])))

        html = render_template(
            'PRE-30-ED.html',
            content=content
        )

        print("HTML ", html)

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
