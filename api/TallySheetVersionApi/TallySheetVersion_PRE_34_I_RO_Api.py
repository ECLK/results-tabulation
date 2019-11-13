from app import db
from auth import authorize
from auth.AuthConstants import POLLING_DIVISION_REPORT_VIEWER_ROLE, EC_LEADERSHIP_ROLE, \
    ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE
from orm.entities import Submission, Area, Election
from orm.entities.Election import ElectionCandidate
from orm.entities.Submission import TallySheet
from orm.entities.SubmissionVersion import TallySheetVersion
from orm.entities.TallySheetVersionRow import TallySheetVersionRow_PRE_34_preference, \
    TallySheetVersionRow_PRE_34_summary
from orm.enums import AreaTypeEnum, TallySheetCodeEnum
from schemas import TallySheetVersionSchema
from sqlalchemy import func, and_


@authorize(
    required_roles=[ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE, POLLING_DIVISION_REPORT_VIEWER_ROLE, EC_LEADERSHIP_ROLE])
def get_by_id(tallySheetId, tallySheetVersionId):
    result = TallySheetVersion.get_by_id(
        tallySheetId=tallySheetId,
        tallySheetVersionId=tallySheetVersionId
    )

    return TallySheetVersionSchema().dump(result).data


@authorize(
    required_roles=[ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE, POLLING_DIVISION_REPORT_VIEWER_ROLE, EC_LEADERSHIP_ROLE])
def create(tallySheetId):
    tallySheet, tallySheetVersion = TallySheet.create_latest_version(
        tallySheetId=tallySheetId,
        tallySheetCode=TallySheetCodeEnum.PRE_34_I_RO
    )

    countingCentres = tallySheetVersion.submission.area.get_associated_areas(
        areaType=AreaTypeEnum.CountingCentre, electionId=tallySheetVersion.submission.electionId
    )

    query = db.session.query(
        func.count(Area.Model.areaId).label("areaCount"),
        Election.Model.electionId,
        ElectionCandidate.Model.candidateId,
        TallySheetVersionRow_PRE_34_preference.Model.preferenceNumber,
        func.sum(TallySheetVersionRow_PRE_34_preference.Model.preferenceCount).label("preferenceCount"),
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
            TallySheet.Model.tallySheetCode == TallySheetCodeEnum.PRE_34_CO
        )
    ).join(
        TallySheetVersionRow_PRE_34_preference.Model,
        and_(
            TallySheetVersionRow_PRE_34_preference.Model.tallySheetVersionId == Submission.Model.lockedVersionId,
            TallySheetVersionRow_PRE_34_preference.Model.candidateId == ElectionCandidate.Model.candidateId,
            TallySheetVersionRow_PRE_34_preference.Model.electionId == Submission.Model.electionId
        ),
        isouter=True
    ).filter(
        Area.Model.areaId.in_([area.areaId for area in countingCentres]),
        ElectionCandidate.Model.qualifiedForPreferences == True
    ).group_by(
        ElectionCandidate.Model.candidateId,
        TallySheetVersionRow_PRE_34_preference.Model.preferenceNumber,
    ).order_by(
        Area.Model.areaId,
        ElectionCandidate.Model.candidateId
    ).all()

    summary = db.session.query(
        func.count(Area.Model.areaId).label("areaCount"),
        func.sum(TallySheetVersionRow_PRE_34_summary.Model.ballotPapersNotCounted).label("ballotPapersNotCounted"),
        func.sum(TallySheetVersionRow_PRE_34_summary.Model.remainingBallotPapers).label("remainingBallotPapers"),
    ).join(
        Submission.Model,
        Submission.Model.areaId == Area.Model.areaId
    ).join(
        TallySheet.Model,
        and_(
            TallySheet.Model.tallySheetId == Submission.Model.submissionId,
            TallySheet.Model.tallySheetCode == TallySheetCodeEnum.PRE_34_CO
        )
    ).join(
        TallySheetVersionRow_PRE_34_summary.Model,
        and_(
            TallySheetVersionRow_PRE_34_summary.Model.tallySheetVersionId == Submission.Model.lockedVersionId,
            TallySheetVersionRow_PRE_34_summary.Model.electionId == Submission.Model.electionId
        ),
        isouter=True
    ).filter(
        Area.Model.areaId.in_([area.areaId for area in countingCentres])
    ).one_or_none()

    is_complete = True
    for row in query:
        if row.candidateId is not None and row.preferenceNumber is not None and row.preferenceNumber is not None:
            tallySheetVersion.add_row(
                electionId=row.electionId,
                candidateId=row.candidateId,
                preferenceNumber=row.preferenceNumber,
                preferenceCount=row.preferenceCount
            )
        else:
            is_complete = False

    if summary is not None and summary.ballotPapersNotCounted is not None and summary.remainingBallotPapers is not None:
        TallySheetVersionRow_PRE_34_summary.create(
            electionId=tallySheet.submission.electionId,
            tallySheetVersionId=tallySheetVersion.tallySheetVersionId,
            ballotPapersNotCounted=summary.ballotPapersNotCounted,
            remainingBallotPapers=summary.remainingBallotPapers
        )
    else:
        is_complete = False

    if is_complete:
        tallySheetVersion.set_complete()

    db.session.commit()

    return TallySheetVersionSchema().dump(tallySheetVersion).data
