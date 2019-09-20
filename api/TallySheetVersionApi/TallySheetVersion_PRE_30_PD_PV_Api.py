from app import db
from orm.entities import Submission, SubmissionVersion
from orm.entities.TallySheetVersionRow import TallySheetVersionRow_PRE_41
from orm.enums import AreaTypeEnum
from schemas import TallySheetVersion_PRE_30_PD_Schema, TallySheetVersionSchema
from orm.entities.SubmissionVersion.TallySheetVersion import TallySheetVersion_PRE_30_PD_PV
from sqlalchemy import func


def get_by_id(tallySheetId, tallySheetVersionId):
    result = TallySheetVersion_PRE_30_PD_PV.get_by_id(
        tallySheetId=tallySheetId,
        tallySheetVersionId=tallySheetVersionId
    )

    return TallySheetVersion_PRE_30_PD_Schema().dump(result).data


def create(tallySheetId):
    tallySheetVersion = TallySheetVersion_PRE_30_PD_PV.create(
        tallySheetId=tallySheetId
    )

    countingCentres = tallySheetVersion.submission.area.get_associated_areas(
        areaType=AreaTypeEnum.PostalVoteCountingCentre, electionId=tallySheetVersion.submission.electionId
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
        TallySheetVersionRow_PRE_41.Model.tallySheetVersionId == Submission.Model.latestVersionId,
        Submission.Model.areaId.in_([area.areaId for area in countingCentres])
    ).group_by(
        TallySheetVersionRow_PRE_41.Model.candidateId,
        Submission.Model.areaId
    ).order_by(
        TallySheetVersionRow_PRE_41.Model.candidateId,
        Submission.Model.areaId
    ).all()

    print("################ query ", query)

    for row in query:
        print("################ row ", row)
        tallySheetVersion.add_row(
            candidateId=row.candidateId,
            countingCentreId=row.areaId,
            count=row.count
        )

    db.session.commit()

    return TallySheetVersionSchema().dump(tallySheetVersion).data
