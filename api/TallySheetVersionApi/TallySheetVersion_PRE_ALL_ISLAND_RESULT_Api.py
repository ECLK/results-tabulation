from api import TallySheetVersionApi
from app import db
from auth import authorize, NATIONAL_REPORT_VIEWER_ROLE, EC_LEADERSHIP_ROLE, NATIONAL_REPORT_VERIFIER_ROLE
from orm.entities import Submission, SubmissionVersion, Area
from orm.entities.Submission import TallySheet
from orm.entities.SubmissionVersion import TallySheetVersion
from orm.entities.TallySheetVersionRow import TallySheetVersionRow_PRE_30_ED, TallySheetVersionRow_RejectedVoteCount
from orm.enums import AreaTypeEnum, TallySheetCodeEnum
from schemas import TallySheetVersion_PRE_ALL_ISLAND_RESULT_Schema, TallySheetVersionSchema
from sqlalchemy import func


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
    tallySheetVersion.set_complete()  # TODO: valid before setting complete. Refer to PRE_30_PD

    electoralDistricts = db.session.query(
        Area.Model.areaId
    ).filter(
        Area.Model.areaType == AreaTypeEnum.ElectoralDistrict,
        Area.Model.electionId == tallySheetVersion.submission.electionId
    ).all()

    query = db.session.query(
        TallySheetVersionRow_PRE_30_ED.Model.candidateId,
        func.sum(TallySheetVersionRow_PRE_30_ED.Model.count).label("count"),
    ).join(
        SubmissionVersion.Model,
        SubmissionVersion.Model.submissionVersionId == TallySheetVersionRow_PRE_30_ED.Model.tallySheetVersionId
    ).join(
        Submission.Model,
        Submission.Model.submissionId == SubmissionVersion.Model.submissionId
    ).filter(
        TallySheetVersionRow_PRE_30_ED.Model.tallySheetVersionId == Submission.Model.lockedVersionId,
        Submission.Model.areaId.in_([area.areaId for area in electoralDistricts])
    ).group_by(
        TallySheetVersionRow_PRE_30_ED.Model.candidateId
    ).order_by(
        TallySheetVersionRow_PRE_30_ED.Model.candidateId
    ).all()

    for row in query:
        tallySheetVersion.add_row(
            candidateId=row.candidateId,
            count=row.count
        )

    rejected_vote_count_query = db.session.query(
        func.count(Submission.Model.areaId).label("areaCount"),
        func.sum(TallySheetVersionRow_RejectedVoteCount.Model.rejectedVoteCount).label("rejectedVoteCount"),
    ).join(
        TallySheet.Model,
        TallySheet.Model.tallySheetId == Submission.Model.submissionId
    ).join(
        TallySheetVersionRow_RejectedVoteCount.Model,
        TallySheetVersionRow_RejectedVoteCount.Model.tallySheetVersionId == Submission.Model.lockedVersionId
    ).filter(
        Submission.Model.areaId.in_([area.areaId for area in electoralDistricts]),
        TallySheet.Model.tallySheetCode == TallySheetCodeEnum.PRE_30_ED
    ).order_by(
        Submission.Model.areaId
    ).all()

    for row in rejected_vote_count_query:
        if row.areaCount > 0:
            tallySheetVersion.add_invalid_vote_count(
                electionId=tallySheetVersion.submission.electionId,
                rejectedVoteCount=row.rejectedVoteCount
            )

    db.session.commit()

    return TallySheetVersionSchema().dump(tallySheetVersion).data
