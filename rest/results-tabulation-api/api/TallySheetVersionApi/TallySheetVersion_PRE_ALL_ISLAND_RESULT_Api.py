from api import TallySheetVersionApi
from app import db
from auth import authorize, NATIONAL_REPORT_VIEWER_ROLE, EC_LEADERSHIP_ROLE, NATIONAL_REPORT_VERIFIER_ROLE
from orm.entities import Submission, SubmissionVersion, Area, Election
from orm.entities.Election import ElectionCandidate
from orm.entities.Submission import TallySheet
from orm.entities.SubmissionVersion import TallySheetVersion
from orm.entities.TallySheetVersionRow import TallySheetVersionRow_PRE_30_ED, TallySheetVersionRow_RejectedVoteCount, \
    TallySheetVersionRow_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS
from orm.enums import AreaTypeEnum, TallySheetCodeEnum
from schemas import TallySheetVersion_PRE_ALL_ISLAND_RESULT_Schema, TallySheetVersionSchema
from sqlalchemy import func, and_


@authorize(required_roles=[NATIONAL_REPORT_VIEWER_ROLE, NATIONAL_REPORT_VERIFIER_ROLE, EC_LEADERSHIP_ROLE])
def get_by_id(tallySheetId, tallySheetVersionId):
    result = TallySheetVersion.get_by_id(
        tallySheetId=tallySheetId,
        tallySheetVersionId=tallySheetVersionId
    )

    return TallySheetVersion_PRE_ALL_ISLAND_RESULT_Schema().dump(result).data


@authorize(required_roles=[NATIONAL_REPORT_VIEWER_ROLE, NATIONAL_REPORT_VERIFIER_ROLE, EC_LEADERSHIP_ROLE])
def create(tallySheetId):
    tallySheet, tallySheetVersion = TallySheet.create_latest_version(
        tallySheetId=tallySheetId,
        tallySheetCode=TallySheetCodeEnum.PRE_ALL_ISLAND_RESULTS
    )

    electoralDistricts = db.session.query(
        Area.Model.areaId
    ).filter(
        Area.Model.areaType == AreaTypeEnum.ElectoralDistrict,
        Area.Model.electionId == tallySheetVersion.submission.electionId
    ).all()

    electionId = tallySheetVersion.submission.electionId

    query = db.session.query(
        func.count(Area.Model.areaId).label("areaCount"),
        ElectionCandidate.Model.candidateId,
        Submission.Model.areaId.label("electoralDistrictId"),
        func.sum(TallySheetVersionRow_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS.Model.count).label("count"),
    ).join(
        Election.Model,
        Election.Model.electionId == Area.Model.electionId
    ).join(
        ElectionCandidate.Model,
        ElectionCandidate.Model.electionId == Election.Model.electionId
    ).join(
        Submission.Model,
        Submission.Model.areaId == Area.Model.areaId
    ).join(
        TallySheet.Model,
        and_(
            TallySheet.Model.tallySheetId == Submission.Model.submissionId,
            TallySheet.Model.tallySheetCode == TallySheetCodeEnum.PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS
        )
    ).join(
        TallySheetVersionRow_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS.Model,
        and_(
            TallySheetVersionRow_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS.Model.tallySheetVersionId == Submission.Model.lockedVersionId,
            TallySheetVersionRow_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS.Model.candidateId == ElectionCandidate.Model.candidateId
        ),
        isouter=True
    ).filter(
        Area.Model.areaType == AreaTypeEnum.Country,
        Area.Model.electionId == electionId
    ).group_by(
        ElectionCandidate.Model.candidateId
    ).order_by(
        ElectionCandidate.Model.candidateId
    ).all()

    is_complete = True
    for row in query:
        if (row.candidateId and row.count) is not None:
            tallySheetVersion.add_row(
                candidateId=row.candidateId,
                count=row.count
            )
        else:
            is_complete = False

    rejected_vote_count_query = db.session.query(
        func.count(Area.Model.areaId).label("areaCount"),
        func.sum(TallySheetVersionRow_RejectedVoteCount.Model.rejectedVoteCount).label("rejectedVoteCount"),
    ).join(
        Submission.Model,
        Submission.Model.areaId == Area.Model.areaId
    ).join(
        TallySheet.Model,
        and_(
            TallySheet.Model.tallySheetId == Submission.Model.submissionId,
            TallySheet.Model.tallySheetCode == TallySheetCodeEnum.PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS
        )
    ).join(
        TallySheetVersionRow_RejectedVoteCount.Model,
        TallySheetVersionRow_RejectedVoteCount.Model.tallySheetVersionId == Submission.Model.lockedVersionId,
        isouter=True
    ).filter(
        Area.Model.areaType == AreaTypeEnum.Country,
        Area.Model.electionId == electionId
    ).all()

    for row in rejected_vote_count_query:
        if row.areaCount > 0 and (electionId and row.rejectedVoteCount) is not None:
            tallySheetVersion.add_invalid_vote_count(
                electionId=electionId,
                rejectedVoteCount=row.rejectedVoteCount
            )
        else:
            is_complete = False

    if is_complete:
        tallySheetVersion.set_complete()
    db.session.commit()

    return TallySheetVersionSchema().dump(tallySheetVersion).data
