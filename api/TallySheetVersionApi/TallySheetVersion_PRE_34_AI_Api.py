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
        ElectionCandidate.Model.qualifiedForPreferences,
        Submission.Model.electionId,
        func.sum(
            func.IF(
                and_(
                    TallySheetVersionRow_PRE_34_preference.Model.preferenceNumber == 1
                ),
                TallySheetVersionRow_PRE_34_preference.Model.preferenceCount,
                None
            )
        ).label("firstPreferenceCount"),
        func.sum(
            func.IF(
                and_(
                    TallySheetVersionRow_PRE_34_preference.Model.preferenceNumber == 2
                ),
                TallySheetVersionRow_PRE_34_preference.Model.preferenceCount,
                None
            )
        ).label("secondPreferenceCount"),
        func.sum(
            func.IF(
                and_(
                    TallySheetVersionRow_PRE_34_preference.Model.preferenceNumber == 3
                ),
                TallySheetVersionRow_PRE_34_preference.Model.preferenceCount,
                None
            )
        ).label("thirdPreferenceCount"),
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
        isouter=True
    ).filter(
        Submission.Model.areaId.in_(electoral_district_ids)
    ).group_by(
        ElectionCandidate.Model.candidateId
    ).order_by(
        ElectionCandidate.Model.candidateId
    ).all()

    is_complete = True
    for row in query:
        if (row.candidateId and row.firstPreferenceCount) is not None:
            tallySheetVersion.add_row(
                electionId=row.electionId,
                candidateId=row.candidateId,
                preferenceNumber=1,
                preferenceCount=row.firstPreferenceCount
            )

            if row.qualifiedForPreferences is True:
                if (row.secondPreferenceCount and row.thirdPreferenceCount) is not None:
                    tallySheetVersion.add_row(
                        electionId=row.electionId,
                        candidateId=row.candidateId,
                        preferenceNumber=2,
                        preferenceCount=row.secondPreferenceCount
                    )
                    tallySheetVersion.add_row(
                        electionId=row.electionId,
                        candidateId=row.candidateId,
                        preferenceNumber=3,
                        preferenceCount=row.thirdPreferenceCount
                    )
                else:
                    is_complete = False
        else:
            is_complete = False

    if is_complete:
        tallySheetVersion.set_complete()

    db.session.commit()

    return TallySheetVersionSchema().dump(tallySheetVersion).data
