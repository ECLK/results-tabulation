from app import db
from orm.entities import Area, Submission, Candidate
from orm.entities.Election import ElectionCandidate

from sqlalchemy import func, and_

from orm.entities.TallySheetVersionRow import TallySheetVersionRow_PRE_41
from orm.enums import AreaTypeEnum
from util import get_array


def get_PRE41_candidate_wise_aggregated_result(electionId, areas, subquery=False):
    areas = get_array(areas)

    countingCentres = []

    for area in areas:
        for countingCentre in area.get_associated_areas(AreaTypeEnum.CountingCentre):
            countingCentres.append(countingCentre)

    query = db.session.query(
        ElectionCandidate.Model.candidateId,
        Candidate.Model.candidateName,
        func.sum(TallySheetVersionRow_PRE_41.Model.count).label("count")
    ).join(
        Candidate.Model,
        Candidate.Model.candidateId == ElectionCandidate.Model.candidateId,
        isouter=True
    ).join(
        Submission.Model,
        and_(
            Submission.Model.electionId == ElectionCandidate.Model.electionId,
            Submission.Model.areaId.in_([countingCentre.areaId for countingCentre in countingCentres])
        ),
        isouter=True
    ).join(
        TallySheetVersionRow_PRE_41.Model,
        and_(
            TallySheetVersionRow_PRE_41.Model.tallySheetVersionId == Submission.Model.latestVersionId,
            TallySheetVersionRow_PRE_41.Model.candidateId == ElectionCandidate.Model.candidateId
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
        return query.subquery(), countingCentres
    else:
        return query.all(), countingCentres


def get_PRE41_candidate_and_area_wise_aggregated_result(electionId, areas, subquery=False):
    areas = get_array(areas)

    countingCentres = []

    for area in areas:
        for countingCentre in area.get_associated_areas(AreaTypeEnum.CountingCentre):
            countingCentres.append(countingCentre)

    query = db.session.query(
        ElectionCandidate.Model.candidateId,
        Candidate.Model.candidateName,
        Area.Model.areaId,
        Area.Model.areaName,
        func.sum(TallySheetVersionRow_PRE_41.Model.count).label("count"),
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
        TallySheetVersionRow_PRE_41.Model,
        and_(
            TallySheetVersionRow_PRE_41.Model.tallySheetVersionId == Submission.Model.latestVersionId,
            TallySheetVersionRow_PRE_41.Model.candidateId == ElectionCandidate.Model.candidateId
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
        return query.subquery(), countingCentres
    else:
        return query.all(), countingCentres
