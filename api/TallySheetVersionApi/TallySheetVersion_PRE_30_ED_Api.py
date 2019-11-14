from api import TallySheetVersionApi
from app import db
from auth import authorize, ELECTORAL_DISTRICT_REPORT_VERIFIER_ROLE, NATIONAL_REPORT_VERIFIER_ROLE
from auth.AuthConstants import ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE, EC_LEADERSHIP_ROLE
from orm.entities import Submission, Election, Area
from orm.entities.Election import ElectionCandidate
from orm.entities.Submission import TallySheet
from orm.entities.SubmissionVersion import TallySheetVersion
from orm.entities.TallySheetVersionRow import TallySheetVersionRow_PRE_30_PD, TallySheetVersionRow_RejectedVoteCount
from orm.enums import TallySheetCodeEnum
from schemas import TallySheetVersion_PRE_30_ED_Schema, TallySheetVersionSchema
from sqlalchemy import func, and_


@authorize(required_roles=[ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE, ELECTORAL_DISTRICT_REPORT_VERIFIER_ROLE,
                           NATIONAL_REPORT_VERIFIER_ROLE, EC_LEADERSHIP_ROLE])
def get_by_id(tallySheetId, tallySheetVersionId):
    result = TallySheetVersion.get_by_id(
        tallySheetId=tallySheetId,
        tallySheetVersionId=tallySheetVersionId
    )

    return TallySheetVersion_PRE_30_ED_Schema().dump(result).data


@authorize(
    required_roles=[ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE, ELECTORAL_DISTRICT_REPORT_VERIFIER_ROLE,
                    NATIONAL_REPORT_VERIFIER_ROLE, EC_LEADERSHIP_ROLE])
def create(tallySheetId):
    tallySheet, tallySheetVersion = TallySheet.create_latest_version(
        tallySheetId=tallySheetId,
        tallySheetCode=TallySheetCodeEnum.PRE_30_ED
    )

    polling_division_and_electoral_district_subquery = tallySheetVersion.polling_division_and_electoral_district_query().subquery()

    query = db.session.query(
        polling_division_and_electoral_district_subquery.c.areaId,
        ElectionCandidate.Model.candidateId,
        Submission.Model.electionId,
        func.sum(TallySheetVersionRow_PRE_30_PD.Model.count).label("count"),
    ).join(
        Election.Model,
        Election.Model.electionId == polling_division_and_electoral_district_subquery.c.electionId
    ).join(
        ElectionCandidate.Model,
        ElectionCandidate.Model.electionId == Election.Model.electionId
    ).join(
        Submission.Model,
        Submission.Model.areaId == polling_division_and_electoral_district_subquery.c.areaId
    ).join(
        TallySheet.Model,
        and_(
            TallySheet.Model.tallySheetId == Submission.Model.submissionId,
            TallySheet.Model.tallySheetCode == TallySheetCodeEnum.PRE_30_PD
        )
    ).join(
        TallySheetVersionRow_PRE_30_PD.Model,
        and_(
            TallySheetVersionRow_PRE_30_PD.Model.tallySheetVersionId == Submission.Model.lockedVersionId,
            TallySheetVersionRow_PRE_30_PD.Model.candidateId == ElectionCandidate.Model.candidateId
        ),
        isouter=True
    ).group_by(
        ElectionCandidate.Model.candidateId,
        Submission.Model.electionId,
        Submission.Model.areaId
    ).order_by(
        ElectionCandidate.Model.candidateId,
        Submission.Model.electionId,
        Submission.Model.areaId
    ).all()

    is_complete = True
    for row in query:
        print("###### row [1] ##### ", row)
        if (row.candidateId and row.areaId and row.count and row.electionId) is not None:
            tallySheetVersion.add_row(
                candidateId=row.candidateId,
                areaId=row.areaId,
                count=row.count,
                electionId=row.electionId
            )
        else:
            is_complete = False

    rejected_vote_count_query = db.session.query(
        polling_division_and_electoral_district_subquery.c.areaId,
        Submission.Model.electionId,
        func.sum(TallySheetVersionRow_RejectedVoteCount.Model.rejectedVoteCount).label("rejectedVoteCount"),
    ).join(
        Submission.Model,
        Submission.Model.areaId == polling_division_and_electoral_district_subquery.c.areaId
    ).join(
        TallySheet.Model,
        and_(
            TallySheet.Model.tallySheetId == Submission.Model.submissionId,
            TallySheet.Model.tallySheetCode == TallySheetCodeEnum.PRE_30_PD
        )
    ).join(
        TallySheetVersionRow_RejectedVoteCount.Model,
        TallySheetVersionRow_RejectedVoteCount.Model.tallySheetVersionId == Submission.Model.lockedVersionId,
        isouter=True
    ).group_by(
        Submission.Model.electionId,
        Submission.Model.areaId
    ).order_by(
        Submission.Model.electionId,
        Submission.Model.areaId
    ).all()

    for row in rejected_vote_count_query:
        print("###### row [2] ##### ", row)
        if (row.electionId and row.areaId and row.rejectedVoteCount) is not None:
            tallySheetVersion.add_invalid_vote_count(
                electionId=row.electionId,
                areaId=row.areaId,
                rejectedVoteCount=row.rejectedVoteCount
            )
        else:
            is_complete = False

    if is_complete:
        tallySheetVersion.set_complete()

    db.session.commit()

    return TallySheetVersionSchema().dump(tallySheetVersion).data
