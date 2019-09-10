from app import db
from orm.entities import Submission, SubmissionVersion
from orm.entities.TallySheetVersionRow import TallySheetVersionRow_PRE_30_ED
from orm.enums import AreaTypeEnum
from schemas import TallySheetVersion_PRE_ALL_ISLAND_RESULT_Schema, TallySheetVersionSchema
from orm.entities.SubmissionVersion.TallySheetVersion import TallySheetVersion_PRE_ALL_ISLAND_RESULT, \
    TallySheetVersion_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS
from sqlalchemy import func


def get_by_id(tallySheetId, tallySheetVersionId):
    result = TallySheetVersion_PRE_ALL_ISLAND_RESULT_Schema.get_by_id(
        tallySheetId=tallySheetId,
        tallySheetVersionId=tallySheetVersionId
    )

    return TallySheetVersion_PRE_ALL_ISLAND_RESULT_Schema().dump(result).data


def create(tallySheetId):
    tallySheetVersion = TallySheetVersion_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS.create(
        tallySheetId=tallySheetId
    )

    electoralDistricts = tallySheetVersion.submission.area.get_associated_areas(AreaTypeEnum.ElectoralDistrict)

    query = db.session.query(
        TallySheetVersionRow_PRE_30_ED.Model.candidateId,
        Submission.Model.areaId.label("electoralDistrictId"),
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
        TallySheetVersionRow_PRE_30_ED.Model.candidateId,
        Submission.Model.areaId
    ).order_by(
        TallySheetVersionRow_PRE_30_ED.Model.candidateId,
        Submission.Model.areaId
    ).all()

    for row in query:
        tallySheetVersion.add_row(
            candidateId=row.candidateId,
            electoralDistrictId=row.electoralDistrictId,
            count=row.count
        )

    db.session.commit()

    return TallySheetVersionSchema().dump(tallySheetVersion).data
