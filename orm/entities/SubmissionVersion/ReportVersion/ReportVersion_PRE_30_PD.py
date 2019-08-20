from sqlalchemy import and_

from flask import render_template
from sqlalchemy.ext.hybrid import hybrid_property

from app import db
from sqlalchemy.orm import relationship
from sqlalchemy import func

from exception import NotFoundException
from orm.entities import ReportVersion, Party, Candidate, Submission, SubmissionVersion, Area
from orm.entities.Area.Office import CountingCentre
from orm.entities.Election import ElectionParty, ElectionCandidate
from orm.entities.Result import PartyWiseResult, CandidateWiseResult
from orm.entities.Result.CandidateWiseResult import CandidateCount
from orm.entities.Result.PartyWiseResult import PartyCount
from orm.entities.Submission import TallySheet
from orm.entities.Submission.Report import Report_PRE_30_PD, Report_PRE_41
from orm.entities.SubmissionVersion.TallySheetVersion import TallySheetVersionPRE41
from orm.enums import ReportCodeEnum, AreaTypeEnum


class ReportVersion_PRE_30_PD_Model(ReportVersion.Model):

    def __init__(self, reportId):
        report = Report_PRE_30_PD.get_by_id(reportId=reportId)
        if report is None:
            raise NotFoundException("Report not found. (reportId=%d)" % reportId)

        areas = report.area.get_associated_areas(AreaTypeEnum.CountingCentre)
        areaIds = [area.areaId for area in areas]
        latestTallySheetVersions = []
        for countingCentre in areas:
            for tallySheet in countingCentre.tallySheets_PRE_41:
                latestTallySheetVersions.append(tallySheet.latestVersionId)

        aggregatedPartyCount = db.session.query(
            CountingCentre.Model.areaId,
            ElectionCandidate.Model.candidateId,
            func.sum(CandidateCount.Model.count).label("count")
        ).join(
            ElectionCandidate.Model,
            ElectionCandidate.Model.electionId == CountingCentre.Model.electionId
        ).join(
            Submission.Model,
            Submission.Model.areaId == CountingCentre.Model.areaId,
            isouter=True
        ).join(
            SubmissionVersion.Model,
            SubmissionVersion.Model.submissionId == Submission.Model.submissionId,
            isouter=True
        ).join(
            TallySheetVersionPRE41.Model,
            and_(
                TallySheetVersionPRE41.Model.tallySheetVersionId == SubmissionVersion.Model.submissionVersionId,
                TallySheetVersionPRE41.Model.tallySheetVersionId.in_(latestTallySheetVersions)
            ),
            isouter=True
        ).join(
            CandidateWiseResult.Model,
            and_(
                CandidateWiseResult.Model.candidateWiseResultId == TallySheetVersionPRE41.Model.candidateWiseResultId
            ),
            isouter=True
        ).join(
            CandidateCount.Model,
            and_(
                CandidateCount.Model.candidateWiseResultId == CandidateWiseResult.Model.candidateWiseResultId,
                CandidateCount.Model.candidateId == ElectionCandidate.Model.candidateId
            ),
            isouter=True
        ).filter(
            CountingCentre.Model.areaId.in_(areaIds)
        ).group_by(
            ElectionCandidate.Model.candidateId,
            CountingCentre.Model.areaId
        ).order_by(
            ElectionCandidate.Model.candidateId,
            CountingCentre.Model.areaId
        ).subquery()

        queryResult = db.session.query(
            Candidate.Model.candidateId,
            Candidate.Model.candidateName,
            Area.Model.areaId,
            Area.Model.areaName,
            aggregatedPartyCount.c.count
        ).join(
            ElectionCandidate.Model,
            ElectionCandidate.Model.candidateId == Candidate.Model.candidateId
        ).join(
            aggregatedPartyCount,
            aggregatedPartyCount.c.candidateId == Candidate.Model.candidateId,
            isouter=True
        ).join(
            Area.Model,
            Area.Model.areaId == aggregatedPartyCount.c.areaId,
            isouter=True
        ).filter(
            ElectionCandidate.Model.electionId == report.electionId,
        ).order_by(
            ElectionCandidate.Model.candidateId,
            Area.Model.areaId
        ).all()

        countingCentres = []
        data = []

        for i in range(0, len(areas)):
            countingCentres.append(queryResult[i].areaName)

        for i in range(0, int(len(queryResult) / len(areas))):
            data_row = [queryResult[i].candidateName]
            data.append(data_row)
            total_count_per_candidate = 0
            for j in range(i, i + len(areas)):
                if queryResult[j].count is None:
                    data_row.append("")
                else:
                    data_row.append(queryResult[j].count)
                    total_count_per_candidate = total_count_per_candidate + queryResult[j].count
            data_row.append(total_count_per_candidate)

        content = {
            "pollingDistrict": report.area.areaName,
            "data": data,
            "countingCentres": countingCentres
        }

        html = render_template(
            'PRE-30-PD.html',
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
