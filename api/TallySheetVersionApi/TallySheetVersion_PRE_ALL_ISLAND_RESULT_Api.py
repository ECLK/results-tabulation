from app import db
from orm.entities import Submission, SubmissionVersion
from orm.entities.TallySheetVersionRow import TallySheetVersionRow_PRE_30_ED
from orm.enums import AreaTypeEnum
from schemas import TallySheetVersion_PRE_ALL_ISLAND_RESULT_Schema
from orm.entities.SubmissionVersion.TallySheetVersion import TallySheetVersion_PRE_ALL_ISLAND_RESULT
from sqlalchemy import func


def create(tallySheetId):
    tallySheetVersion = TallySheetVersion_PRE_ALL_ISLAND_RESULT.create(
        tallySheetId=tallySheetId
    )

    electoralDistricts = tallySheetVersion.submission.area.get_associated_areas(AreaTypeEnum.ElectoralDistrict)

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
        TallySheetVersionRow_PRE_30_ED.Model.tallySheetVersionId == Submission.Model.latestVersionId,
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

    db.session.commit()

    return TallySheetVersion_PRE_ALL_ISLAND_RESULT_Schema().dump(tallySheetVersion).data
