from app import db
from auth import authorize, POLLING_DIVISION_REPORT_VERIFIER_ROLE, ELECTORAL_DISTRICT_REPORT_VERIFIER_ROLE, \
    NATIONAL_REPORT_VERIFIER_ROLE, NATIONAL_REPORT_VIEWER_ROLE
from auth.AuthConstants import POLLING_DIVISION_REPORT_VIEWER_ROLE, EC_LEADERSHIP_ROLE, \
    ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE
from orm.entities import Submission, Area, Election
from orm.entities.Area import AreaMap
from orm.entities.Election import ElectionCandidate
from orm.entities.Submission import TallySheet
from orm.entities.SubmissionVersion import TallySheetVersion
from orm.entities.TallySheetVersionRow import TallySheetVersionRow_PRE_34_preference, TallySheetVersionRow_PRE_30_PD
from orm.enums import AreaTypeEnum, TallySheetCodeEnum
from schemas import TallySheetVersionSchema
from sqlalchemy import func, and_, or_


@authorize(required_roles=[NATIONAL_REPORT_VIEWER_ROLE, NATIONAL_REPORT_VERIFIER_ROLE, EC_LEADERSHIP_ROLE])
def get_by_id(tallySheetId, tallySheetVersionId):
    result = TallySheetVersion.get_by_id(
        tallySheetId=tallySheetId,
        tallySheetVersionId=tallySheetVersionId
    )

    return TallySheetVersionSchema().dump(result).data


@authorize(required_roles=[NATIONAL_REPORT_VIEWER_ROLE, NATIONAL_REPORT_VERIFIER_ROLE, EC_LEADERSHIP_ROLE])
def create(tallySheetId):
    tallySheet, tallySheetVersion = TallySheet.create_latest_version(
        tallySheetId=tallySheetId,
        tallySheetCode=TallySheetCodeEnum.PRE_34_AI
    )

    electoral_districts = db.session.query(
        AreaMap.Model.electoralDistrictId
    ).filter(
        AreaMap.Model.countryId == tallySheet.submission.areaId
    ).group_by(
        AreaMap.Model.electoralDistrictId
    ).all()

    electoral_district_ids = []
    for electoral_district in electoral_districts:
        electoral_district_ids.append(electoral_district.electoralDistrictId)

    query = db.session.query(
        func.count(Area.Model.areaId).label("areaCount"),
        ElectionCandidate.Model.candidateId,
        TallySheetVersionRow_PRE_34_preference.Model.preferenceNumber,
        func.sum(TallySheetVersionRow_PRE_34_preference.Model.preferenceCount).label("preferenceCount"),
        Submission.Model.electionId
    ).join(
        Submission.Model,
        Submission.Model.areaId == Area.Model.areaId
    ).join(
        Election.Model,
        Election.Model.electionId == Area.Model.electionId
    ).join(
        ElectionCandidate.Model,
        or_(
            ElectionCandidate.Model.electionId == Election.Model.electionId,
            ElectionCandidate.Model.electionId == Election.Model.parentElectionId
        )
    ).join(
        TallySheet.Model,
        and_(
            TallySheet.Model.tallySheetId == Submission.Model.submissionId,
            TallySheet.Model.tallySheetCode == TallySheetCodeEnum.PRE_34_ED
        )
    ).join(
        TallySheetVersionRow_PRE_34_preference.Model,
        and_(
            TallySheetVersionRow_PRE_34_preference.Model.tallySheetVersionId == Submission.Model.lockedVersionId,
            TallySheetVersionRow_PRE_34_preference.Model.candidateId == ElectionCandidate.Model.candidateId
        ),
    ).filter(
        Submission.Model.areaId.in_(electoral_district_ids)
    ).group_by(
        ElectionCandidate.Model.candidateId,
        TallySheetVersionRow_PRE_34_preference.Model.preferenceNumber
    ).order_by(
        TallySheetVersionRow_PRE_34_preference.Model.candidateId,
        TallySheetVersionRow_PRE_34_preference.Model.preferenceNumber
    ).all()

    is_complete = True  # TODO:Change other reports to validate like this
    for row in query:
        if row.candidateId is not None and row.preferenceNumber is not None and row.preferenceCount:
            print("========== row ======== ", row)
            tallySheetVersion.add_row(
                electionId=row.electionId,
                candidateId=row.candidateId,
                preferenceNumber=row.preferenceNumber,
                preferenceCount=row.preferenceCount
            )
        else:
            is_complete = False

    if is_complete:
        tallySheetVersion.set_complete()

    db.session.commit()

    return TallySheetVersionSchema().dump(tallySheetVersion).data
