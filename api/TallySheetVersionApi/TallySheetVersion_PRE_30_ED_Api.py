from api import TallySheetVersionApi
from app import db
from auth import authorize
from auth.AuthConstants import ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE, EC_LEADERSHIP_ROLE
from orm.entities import Submission
from orm.entities.Submission import TallySheet
from orm.entities.SubmissionVersion import TallySheetVersion
from orm.entities.TallySheetVersionRow import TallySheetVersionRow_PRE_30_PD, TallySheetVersionRow_RejectedVoteCount
from orm.enums import TallySheetCodeEnum
from schemas import TallySheetVersion_PRE_30_ED_Schema, TallySheetVersionSchema
from sqlalchemy import func


@authorize(required_roles=[ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE, EC_LEADERSHIP_ROLE])
def get_by_id(tallySheetId, tallySheetVersionId):
    result = TallySheetVersion.get_by_id(
        tallySheetId=tallySheetId,
        tallySheetVersionId=tallySheetVersionId
    )

    return TallySheetVersion_PRE_30_ED_Schema().dump(result).data


@authorize(required_roles=[ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE, EC_LEADERSHIP_ROLE])
def create(tallySheetId):
    tallySheet, tallySheetVersion = TallySheet.create_latest_version(
        tallySheetId=tallySheetId,
        tallySheetCode=TallySheetCodeEnum.PRE_30_ED
    )
    tallySheetVersion.set_complete()  # TODO: valid before setting complete. Refer to PRE_30_PD
    polling_division_and_electoral_district_subquery = tallySheetVersion.polling_division_and_electoral_district_query().subquery()

    query = db.session.query(
        polling_division_and_electoral_district_subquery.c.areaId,
        TallySheetVersionRow_PRE_30_PD.Model.candidateId,
        Submission.Model.electionId,
        func.sum(TallySheetVersionRow_PRE_30_PD.Model.count).label("count"),
    ).join(
        Submission.Model,
        Submission.Model.areaId == polling_division_and_electoral_district_subquery.c.areaId
    ).join(
        TallySheet.Model,
        TallySheet.Model.tallySheetId == Submission.Model.submissionId,
    ).join(
        TallySheetVersionRow_PRE_30_PD.Model,
        TallySheetVersionRow_PRE_30_PD.Model.tallySheetVersionId == Submission.Model.lockedVersionId
    ).filter(
        TallySheet.Model.tallySheetCode == TallySheetCodeEnum.PRE_30_PD
    ).group_by(
        TallySheetVersionRow_PRE_30_PD.Model.candidateId,
        Submission.Model.electionId,
        Submission.Model.areaId
    ).order_by(
        TallySheetVersionRow_PRE_30_PD.Model.candidateId,
        Submission.Model.electionId,
        Submission.Model.areaId
    ).all()

    for row in query:
        tallySheetVersion.add_row(
            candidateId=row.candidateId,
            areaId=row.areaId,
            count=row.count,
            electionId=row.electionId
        )

    rejected_vote_count_query = db.session.query(
        polling_division_and_electoral_district_subquery.c.areaId,
        Submission.Model.electionId,
        func.sum(TallySheetVersionRow_RejectedVoteCount.Model.rejectedVoteCount).label("rejectedVoteCount"),
    ).join(
        Submission.Model,
        Submission.Model.areaId == polling_division_and_electoral_district_subquery.c.areaId
    ).join(
        TallySheet.Model,
        TallySheet.Model.tallySheetId == Submission.Model.submissionId,
    ).join(
        TallySheetVersionRow_RejectedVoteCount.Model,
        TallySheetVersionRow_RejectedVoteCount.Model.tallySheetVersionId == Submission.Model.lockedVersionId
    ).filter(
        TallySheet.Model.tallySheetCode == TallySheetCodeEnum.PRE_30_PD
    ).group_by(
        Submission.Model.electionId,
        Submission.Model.areaId
    ).order_by(
        Submission.Model.electionId,
        Submission.Model.areaId
    ).all()

    for row in rejected_vote_count_query:
        tallySheetVersion.add_invalid_vote_count(
            electionId=row.electionId,
            areaId=row.areaId,
            rejectedVoteCount=row.rejectedVoteCount
        )

    db.session.commit()

    return TallySheetVersionSchema().dump(tallySheetVersion).data
