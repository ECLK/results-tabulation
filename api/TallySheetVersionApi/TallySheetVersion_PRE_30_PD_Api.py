from app import db
from auth import authorize
from auth.AuthConstants import POLLING_DIVISION_REPORT_VIEWER_ROLE, EC_LEADERSHIP_ROLE, \
    ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE
from orm.entities import Submission, SubmissionVersion
from orm.entities.Submission import TallySheet
from orm.entities.SubmissionVersion import TallySheetVersion
from orm.entities.TallySheetVersionRow import TallySheetVersionRow_PRE_41, TallySheetVersionRow_RejectedVoteCount
from orm.enums import AreaTypeEnum, TallySheetCodeEnum
from schemas import TallySheetVersion_PRE_30_PD_Schema, TallySheetVersionSchema
from sqlalchemy import func


@authorize(
    required_roles=[ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE, POLLING_DIVISION_REPORT_VIEWER_ROLE, EC_LEADERSHIP_ROLE])
def get_by_id(tallySheetId, tallySheetVersionId):
    result = TallySheetVersion.get_by_id(
        tallySheetId=tallySheetId,
        tallySheetVersionId=tallySheetVersionId
    )

    return TallySheetVersion_PRE_30_PD_Schema().dump(result).data


@authorize(
    required_roles=[ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE, POLLING_DIVISION_REPORT_VIEWER_ROLE, EC_LEADERSHIP_ROLE])
def create(tallySheetId):
    tallySheet, tallySheetVersion = TallySheet.create_latest_version(
        tallySheetId=tallySheetId,
        tallySheetCode=TallySheetCodeEnum.PRE_30_PD
    )

    countingCentres = tallySheetVersion.submission.area.get_associated_areas(
        areaType=AreaTypeEnum.CountingCentre, electionId=tallySheetVersion.submission.electionId
    )

    query = db.session.query(
        TallySheetVersionRow_PRE_41.Model.candidateId,
        Submission.Model.areaId,
        func.sum(TallySheetVersionRow_PRE_41.Model.count).label("count"),
    ).join(
        SubmissionVersion.Model,
        SubmissionVersion.Model.submissionVersionId == TallySheetVersionRow_PRE_41.Model.tallySheetVersionId
    ).join(
        Submission.Model,
        Submission.Model.submissionId == SubmissionVersion.Model.submissionId
    ).filter(
        TallySheetVersionRow_PRE_41.Model.tallySheetVersionId == Submission.Model.lockedVersionId,
        Submission.Model.areaId.in_([area.areaId for area in countingCentres])
    ).group_by(
        TallySheetVersionRow_PRE_41.Model.candidateId,
        Submission.Model.areaId
    ).order_by(
        TallySheetVersionRow_PRE_41.Model.candidateId,
        Submission.Model.areaId
    ).all()

    for row in query:
        tallySheetVersion.add_row(
            candidateId=row.candidateId,
            countingCentreId=row.areaId,
            count=row.count
        )

    rejected_vote_count_query = db.session.query(
        Submission.Model.areaId,
        func.sum(TallySheetVersionRow_RejectedVoteCount.Model.rejectedVoteCount).label("rejectedVoteCount"),
    ).join(
        TallySheet.Model,
        TallySheet.Model.tallySheetId == Submission.Model.submissionId
    ).join(
        TallySheetVersionRow_RejectedVoteCount.Model,
        TallySheetVersionRow_RejectedVoteCount.Model.tallySheetVersionId == Submission.Model.lockedVersionId
    ).filter(
        Submission.Model.areaId.in_([area.areaId for area in countingCentres]),
        TallySheet.Model.tallySheetCode == TallySheetCodeEnum.PRE_41
    ).group_by(
        Submission.Model.areaId
    ).order_by(
        Submission.Model.areaId
    ).all()

    for row in rejected_vote_count_query:
        tallySheetVersion.add_invalid_vote_count(
            electionId=tallySheetVersion.submission.electionId,
            areaId=row.areaId,
            rejectedVoteCount=row.rejectedVoteCount
        )

    db.session.commit()

    return TallySheetVersionSchema().dump(tallySheetVersion).data
