from app import db
from auth import authorize, ELECTORAL_DISTRICT_REPORT_VERIFIER_ROLE, POLLING_DIVISION_REPORT_VERIFIER_ROLE, \
    NATIONAL_REPORT_VERIFIER_ROLE
from auth.AuthConstants import POLLING_DIVISION_REPORT_VIEWER_ROLE, EC_LEADERSHIP_ROLE, \
    ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE
from orm.entities import Submission, SubmissionVersion, Area, Election
from orm.entities.Election import ElectionCandidate
from orm.entities.Submission import TallySheet
from orm.entities.SubmissionVersion import TallySheetVersion
from orm.entities.TallySheetVersionRow import TallySheetVersionRow_PRE_41, TallySheetVersionRow_RejectedVoteCount
from orm.enums import AreaTypeEnum, TallySheetCodeEnum
from schemas import TallySheetVersion_PRE_30_PD_Schema, TallySheetVersionSchema
from sqlalchemy import func, and_


@authorize(
    required_roles=[POLLING_DIVISION_REPORT_VIEWER_ROLE, POLLING_DIVISION_REPORT_VERIFIER_ROLE,
                    ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE, ELECTORAL_DISTRICT_REPORT_VERIFIER_ROLE,
                    NATIONAL_REPORT_VERIFIER_ROLE, EC_LEADERSHIP_ROLE])
def get_by_id(tallySheetId, tallySheetVersionId):
    result = TallySheetVersion.get_by_id(
        tallySheetId=tallySheetId,
        tallySheetVersionId=tallySheetVersionId
    )

    return TallySheetVersion_PRE_30_PD_Schema().dump(result).data


@authorize(
    required_roles=[POLLING_DIVISION_REPORT_VIEWER_ROLE, POLLING_DIVISION_REPORT_VERIFIER_ROLE,
                    ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE, ELECTORAL_DISTRICT_REPORT_VERIFIER_ROLE, EC_LEADERSHIP_ROLE])
def create(tallySheetId):
    tallySheet, tallySheetVersion = TallySheet.create_latest_version(
        tallySheetId=tallySheetId,
        tallySheetCode=TallySheetCodeEnum.PRE_30_PD
    )

    countingCentres = tallySheetVersion.submission.area.get_associated_areas(
        areaType=AreaTypeEnum.CountingCentre, electionId=tallySheetVersion.submission.electionId
    )

    query = db.session.query(
        Area.Model.areaId,
        ElectionCandidate.Model.candidateId,
        func.sum(TallySheetVersionRow_PRE_41.Model.count).label("count"),
    ).join(
        Election.Model,
        Election.Model.electionId == Area.Model.electionId
    ).join(
        ElectionCandidate.Model,
        ElectionCandidate.Model.electionId == Election.Model.parentElectionId
    ).join(
        Submission.Model,
        Submission.Model.areaId == Area.Model.areaId
    ).join(
        TallySheet.Model,
        and_(
            TallySheet.Model.tallySheetId == Submission.Model.submissionId,
            TallySheet.Model.tallySheetCode == TallySheetCodeEnum.PRE_41
        )
    ).join(
        TallySheetVersionRow_PRE_41.Model,
        and_(
            TallySheetVersionRow_PRE_41.Model.tallySheetVersionId == Submission.Model.lockedVersionId,
            TallySheetVersionRow_PRE_41.Model.candidateId == ElectionCandidate.Model.candidateId
        ),
        isouter=True
    ).filter(
        Area.Model.areaId.in_([area.areaId for area in countingCentres])
    ).group_by(
        Area.Model.areaId,
        ElectionCandidate.Model.candidateId
    ).order_by(
        Area.Model.areaId,
        ElectionCandidate.Model.candidateId
    ).all()

    is_complete = True
    for row in query:
        if (row.candidateId and row.areaId and row.count) is not None:
            tallySheetVersion.add_row(
                candidateId=row.candidateId,
                countingCentreId=row.areaId,
                count=row.count
            )
        else:
            is_complete = False

    rejected_vote_count_query = db.session.query(
        Submission.Model.areaId,
        func.sum(TallySheetVersionRow_RejectedVoteCount.Model.rejectedVoteCount).label("rejectedVoteCount"),
    ).join(
        TallySheet.Model,
        and_(
            TallySheet.Model.tallySheetId == Submission.Model.submissionId,
            TallySheet.Model.tallySheetCode == TallySheetCodeEnum.PRE_41
        )
    ).join(
        TallySheetVersionRow_RejectedVoteCount.Model,
        TallySheetVersionRow_RejectedVoteCount.Model.tallySheetVersionId == Submission.Model.lockedVersionId,
        isouter=True
    ).filter(
        Submission.Model.areaId.in_([area.areaId for area in countingCentres])
    ).group_by(
        Submission.Model.areaId
    ).order_by(
        Submission.Model.areaId
    ).all()

    for row in rejected_vote_count_query:
        if (tallySheetVersion.submission.electionId and row.areaId and row.rejectedVoteCount) is not None:
            tallySheetVersion.add_invalid_vote_count(
                electionId=tallySheetVersion.submission.electionId,
                areaId=row.areaId,
                rejectedVoteCount=row.rejectedVoteCount
            )
        else:
            is_complete = False

    if is_complete:
        tallySheetVersion.set_complete()

    db.session.commit()

    return TallySheetVersionSchema().dump(tallySheetVersion).data
