from app import db
from orm.entities import Area, Submission, SubmissionVersion, Candidate
from orm.entities.Election import ElectionCandidate
from orm.entities.Result import CandidateWiseResult
from orm.entities.Result.CandidateWiseResult import CandidateCount

from sqlalchemy import func, and_

from orm.entities.Submission import TallySheet
from orm.entities.SubmissionVersion.TallySheetVersion import TallySheetVersionPRE41
from orm.enums import AreaTypeEnum
from util import get_array


def get_PRE41_candidate_wise_aggregated_result(electionId, areas, subquery=False):
    areas = get_array(areas)

    latestTallySheetVersions = []
    countingCentres = []

    for area in areas:
        for countingCentre in area.get_associated_areas(AreaTypeEnum.CountingCentre):
            countingCentres.append(countingCentre)
            for tallySheet in countingCentre.tallySheets_PRE_41:
                if tallySheet.latestVersionId is not None:
                    latestTallySheetVersions.append(tallySheet.latestVersionId)

    query = db.session.query(
        ElectionCandidate.Model.candidateId,
        Candidate.Model.candidateName,
        func.sum(CandidateCount.Model.count).label("count")
    ).join(
        Candidate.Model,
        Candidate.Model.candidateId == ElectionCandidate.Model.candidateId,
        isouter=True
    ).join(
        Submission.Model,
        Submission.Model.electionId == ElectionCandidate.Model.electionId,
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
        CandidateWiseResult.Model.candidateWiseResultId == TallySheetVersionPRE41.Model.candidateWiseResultId,
        isouter=True
    ).join(
        CandidateCount.Model,
        and_(
            CandidateCount.Model.candidateWiseResultId == CandidateWiseResult.Model.candidateWiseResultId,
            CandidateCount.Model.candidateId == ElectionCandidate.Model.candidateId,
        ),
        isouter=True
    ).filter(
        ElectionCandidate.Model.electionId == electionId
    ).group_by(
        ElectionCandidate.Model.candidateId
    ).order_by(
        ElectionCandidate.Model.candidateId
    )

    if subquery is True:
        return query.subquery(), countingCentres, latestTallySheetVersions
    else:
        return query.all(), countingCentres, latestTallySheetVersions


def get_PRE41_candidate_and_area_wise_aggregated_result(electionId, areas, subquery=False):
    areas = get_array(areas)

    latestTallySheetVersions = []
    countingCentres = []

    for area in areas:
        for countingCentre in area.get_associated_areas(AreaTypeEnum.CountingCentre):
            countingCentres.append(countingCentre)
            for tallySheet in countingCentre.tallySheets_PRE_41:
                if tallySheet.latestVersionId is not None:
                    latestTallySheetVersions.append(tallySheet.latestVersionId)

    query = db.session.query(
        ElectionCandidate.Model.candidateId,
        Candidate.Model.candidateName,
        Area.Model.areaId,
        Area.Model.areaName,
        func.sum(CandidateCount.Model.count).label("count"),
    ).join(
        Candidate.Model,
        Candidate.Model.candidateId == ElectionCandidate.Model.candidateId,
        isouter=True
    ).join(
        Area.Model,
        Area.Model.electionId == ElectionCandidate.Model.electionId,
        isouter=True
    ).join(
        Submission.Model,
        Submission.Model.areaId == Area.Model.areaId,
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
        CandidateWiseResult.Model.candidateWiseResultId == TallySheetVersionPRE41.Model.candidateWiseResultId,
        isouter=True
    ).join(
        CandidateCount.Model,
        and_(
            CandidateCount.Model.candidateWiseResultId == CandidateWiseResult.Model.candidateWiseResultId,
            CandidateCount.Model.candidateId == ElectionCandidate.Model.candidateId,
        ),
        isouter=True
    ).filter(
        ElectionCandidate.Model.electionId == electionId,
        Area.Model.areaId.in_([countingCentre.areaId for countingCentre in countingCentres])
    ).group_by(
        ElectionCandidate.Model.candidateId,
        Area.Model.areaId
    ).order_by(
        ElectionCandidate.Model.candidateId,
        Area.Model.areaId
    )

    if subquery is True:
        return query.subquery(), countingCentres, latestTallySheetVersions
    else:
        return query.all(), countingCentres, latestTallySheetVersions
