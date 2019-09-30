from app import db
from orm.entities import Submission, SubmissionVersion
from orm.entities.Submission import TallySheet
from orm.entities.TallySheetVersionRow import TallySheetVersionRow_PRE_30_PD, TallySheetVersionRow_RejectedVoteCount
from orm.enums import AreaTypeEnum, TallySheetCodeEnum
from schemas import TallySheetVersion_PRE_30_ED_Schema, TallySheetVersionSchema
from orm.entities.SubmissionVersion.TallySheetVersion import TallySheetVersion_PRE_30_ED
from sqlalchemy import func


def get_by_id(tallySheetId, tallySheetVersionId):
    result = TallySheetVersion_PRE_30_ED.get_by_id(
        tallySheetId=tallySheetId,
        tallySheetVersionId=tallySheetVersionId
    )

    return TallySheetVersion_PRE_30_ED_Schema().dump(result).data


def create(tallySheetId):
    tallySheetVersion = TallySheetVersion_PRE_30_ED.create(
        tallySheetId=tallySheetId
    )

    pollingDivisions = tallySheetVersion.submission.area.get_associated_areas(AreaTypeEnum.PollingDivision)

    query = db.session.query(
        TallySheetVersionRow_PRE_30_PD.Model.candidateId,
        Submission.Model.electionId,
        Submission.Model.areaId,
        func.sum(TallySheetVersionRow_PRE_30_PD.Model.count).label("count"),
    ).join(
        SubmissionVersion.Model,
        SubmissionVersion.Model.submissionVersionId == TallySheetVersionRow_PRE_30_PD.Model.tallySheetVersionId
    ).join(
        Submission.Model,
        Submission.Model.submissionId == SubmissionVersion.Model.submissionId
    ).filter(
        TallySheetVersionRow_PRE_30_PD.Model.tallySheetVersionId == Submission.Model.latestVersionId,
        Submission.Model.areaId.in_([area.areaId for area in pollingDivisions])
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
            pollingDivisionId=row.areaId,
            count=row.count,
            electionId=row.electionId
        )

    rejected_vote_count_query = db.session.query(
        Submission.Model.electionId,
        Submission.Model.areaId,
        func.sum(TallySheetVersionRow_RejectedVoteCount.Model.rejectedVoteCount).label("rejectedVoteCount"),
    ).join(
        TallySheet.Model,
        TallySheet.Model.tallySheetId == Submission.Model.submissionId
    ).join(
        TallySheetVersionRow_RejectedVoteCount.Model,
        TallySheetVersionRow_RejectedVoteCount.Model.tallySheetVersionId == Submission.Model.latestVersionId
    ).filter(
        Submission.Model.areaId.in_([area.areaId for area in pollingDivisions]),
        TallySheet.Model.tallySheetCode == TallySheetCodeEnum.PRE_30_PD
    ).group_by(
        Submission.Model.areaId,
        Submission.Model.electionId
    ).order_by(
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
