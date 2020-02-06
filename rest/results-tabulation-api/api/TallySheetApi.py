from app import db
from auth import authorize, DATA_EDITOR_ROLE, POLLING_DIVISION_REPORT_VERIFIER_ROLE, \
    ELECTORAL_DISTRICT_REPORT_VERIFIER_ROLE, NATIONAL_REPORT_VERIFIER_ROLE, EC_LEADERSHIP_ROLE
from constants.AUTH_CONSTANTS import ALL_ROLES, EC_LEADERSHIP_WRITE_ROLE
from exception import NotFoundException
from exception.messages import MESSAGE_CODE_TALLY_SHEET_NOT_FOUND, \
    MESSAGE_CODE_TALLY_SHEET_VERSION_NOT_FOUND, MESSAGE_CODE_TALLY_SHEET_INCOMPLETE_TALLY_SHEET_CANNOT_BE_LOCKED
from orm.entities.Submission import TallySheet
from orm.entities.Submission.TallySheet import TallySheetModel
from orm.entities.SubmissionVersion import TallySheetVersion
from schemas import TallySheetSchema
from util import RequestBody, get_paginated_query, result_push_service


@authorize(required_roles=ALL_ROLES)
def getAll(electionId=None, areaId=None, tallySheetCode=None):
    result = TallySheet.get_all(
        electionId=electionId,
        areaId=areaId,
        tallySheetCode=tallySheetCode
    )

    result = get_paginated_query(result).all()

    return TallySheetSchema(many=True).dump(result).data


@authorize(required_roles=ALL_ROLES)
def get_by_id(tallySheetId):
    tally_sheet = TallySheet.get_by_id(tallySheetId=tallySheetId)

    if tally_sheet is None:
        NotFoundException(
            message="Tally sheet not found (tallySheetId=%s)" % tallySheetId,
            code=MESSAGE_CODE_TALLY_SHEET_NOT_FOUND
        )

    return TallySheetSchema().dump(tally_sheet).data


@authorize(required_roles=ALL_ROLES)
def unlock(tallySheetId):
    tally_sheet = TallySheet.get_by_id(tallySheetId=tallySheetId)

    if tally_sheet is None:
        NotFoundException(
            message="Tally sheet not found (tallySheetId=%d)" % tallySheetId,
            code=MESSAGE_CODE_TALLY_SHEET_NOT_FOUND
        )

    # TODO refactor
    tally_sheet.submissionProof.open()

    tally_sheet.set_locked_version(None)

    # if tally_sheet.tallySheetCode in [TallySheetCodeEnum.CE_201, TallySheetCodeEnum.CE_201_PV]:
    #     election = tally_sheet.submission.election
    #     electionId = election.parentElectionId
    #     countingCentreId = tally_sheet.areaId
    #     results = StatusCE201.get_status_records(electionId, countingCentreId)
    #
    #     for item in results:
    #         item.status = "Submitted"
    #
    # if tally_sheet.tallySheetCode in [TallySheetCodeEnum.PRE_41]:
    #     election = tally_sheet.submission.election
    #     electionId = election.parentElectionId
    #     countingCentreId = tally_sheet.areaId
    #     results = StatusPRE41.get_status_records(electionId, countingCentreId)
    #
    #     for item in results:
    #         item.status = "Submitted"
    #
    # if tally_sheet.tallySheetCode in [TallySheetCodeEnum.PRE_34_CO]:
    #     election = tally_sheet.submission.election
    #     electionId = election.parentElectionId
    #     countingCentreId = tally_sheet.areaId
    #     results = StatusPRE34.get_status_records(electionId, countingCentreId)
    #
    #     for item in results:
    #         item.status = "Submitted"

    db.session.commit()

    return TallySheetSchema().dump(tally_sheet).data, 201


@authorize(required_roles=ALL_ROLES)
def lock(tallySheetId, body):
    request_body = RequestBody(body)
    tallySheetVersionId = request_body.get("lockedVersionId")

    tally_sheet = TallySheet.get_by_id(tallySheetId=tallySheetId)

    if tally_sheet is None:
        raise NotFoundException("Tally sheet not found (tallySheetId=%d)" % tallySheetId)

    tally_sheet_version = TallySheetVersion.get_by_id(tallySheetVersionId=tallySheetVersionId,
                                                      tallySheetId=tallySheetId)

    if tally_sheet_version is None:
        raise NotFoundException(
            message="Tally sheet version not found (tallySheetVersionId=%d)" % tallySheetVersionId,
            code=MESSAGE_CODE_TALLY_SHEET_VERSION_NOT_FOUND
        )

    if not tally_sheet_version.isComplete:
        raise NotFoundException(
            message="Incomplete tally sheet version (tallySheetVersionId=%d)" % tallySheetVersionId,
            code=MESSAGE_CODE_TALLY_SHEET_INCOMPLETE_TALLY_SHEET_CANNOT_BE_LOCKED
        )

    tally_sheet.set_locked_version(tally_sheet_version)

    # if tally_sheet.tallySheetCode in [TallySheetCodeEnum.CE_201, TallySheetCodeEnum.CE_201_PV]:
    #     election = tally_sheet.submission.election
    #     electionId = election.parentElectionId
    #     countingCentreId = tally_sheet.areaId
    #     results = StatusCE201.get_status_records(electionId, countingCentreId)
    #
    #     for item in results:
    #         item.status = "Verified"
    #
    # if tally_sheet.tallySheetCode in [TallySheetCodeEnum.PRE_41]:
    #     election = tally_sheet.submission.election
    #     electionId = election.parentElectionId
    #     countingCentreId = tally_sheet.areaId
    #     results = StatusPRE41.get_status_records(electionId, countingCentreId)
    #
    #     for item in results:
    #         item.status = "Verified"
    #
    # if tally_sheet.tallySheetCode in [TallySheetCodeEnum.PRE_34_CO]:
    #     election = tally_sheet.submission.election
    #     electionId = election.parentElectionId
    #     countingCentreId = tally_sheet.areaId
    #     results = StatusPRE34.get_status_records(electionId, countingCentreId)
    #
    #     for item in results:
    #         item.status = "Verified"

    db.session.commit()

    return TallySheetSchema().dump(tally_sheet).data, 201


# @authorize(required_roles=[EC_LEADERSHIP_ROLE])
# def certify(tallySheetId):
#     tally_sheet = TallySheet.get_by_id(tallySheetId=tallySheetId)
#
#     if tally_sheet is None:
#         raise NotFoundException("Tally sheet not found (tallySheetId=%d)" % tallySheetId)
#
#     tally_sheet.set_certified_version()
#
#     db.session.commit()
#
#     return TallySheetSchema().dump(tally_sheet).data, 201


@authorize(required_roles=ALL_ROLES)
def notify(tallySheetId):
    tally_sheet = TallySheet.get_by_id(tallySheetId=tallySheetId)

    if tally_sheet is None:
        raise NotFoundException("Tally sheet not found (tallySheetId=%d)" % tallySheetId)

    tally_sheet.set_notified_version()

    db.session.commit()

    try:
        result_push_service.notify_results(
            tally_sheet=tally_sheet,
            tally_sheet_version_id=tally_sheet.notifiedVersionId
        )
    except:  # rollback notification flag
        print("Result push service failed. Check the url configuration.")
        tally_sheet.notifiedVersionId = None
        tally_sheet.notifiedStampId = None
        db.session.commit()
        return "Push Service Failed. Please check configuration and try again.", 500

    return TallySheetSchema().dump(tally_sheet).data, 201


@authorize(required_roles=ALL_ROLES)
def release(tallySheetId):
    tally_sheet = TallySheet.get_by_id(tallySheetId=tallySheetId)

    if tally_sheet is None:
        raise NotFoundException("Tally sheet not found (tallySheetId=%d)" % tallySheetId)

    # TODO refactor
    tally_sheet.submissionProof.close()

    tally_sheet.set_released_version()

    db.session.commit()

    try:
        result_push_service.release_results(
            tally_sheet=tally_sheet,
            tally_sheet_version_id=tally_sheet.releasedVersionId
        )
    except:  # rollback release flag
        print("Result push service failed. Check the url configuration.")
        tally_sheet.releasedVersionId = None
        tally_sheet.releasedStampId = None
        db.session.commit()
        return "Push Service Failed. Please check configuration and try again.", 500

    return TallySheetSchema().dump(tally_sheet).data, 201


@authorize(required_roles=ALL_ROLES)
def request_edit(tallySheetId):
    tally_sheet = TallySheet.get_by_id(tallySheetId=tallySheetId)

    if tally_sheet is None:
        raise NotFoundException(
            message="Tally sheet not found (tallySheetId=%d)" % tallySheetId,
            code=MESSAGE_CODE_TALLY_SHEET_NOT_FOUND
        )

    # if tally_sheet.tallySheetCode not in [TallySheetCodeEnum.PRE_41, TallySheetCodeEnum.CE_201,
    #                                       TallySheetCodeEnum.CE_201_PV, TallySheetCodeEnum.PRE_34_CO]:
    #     raise ForbiddenException(
    #         message="Submit operation is not supported for this tally sheet type.",
    #         code=MESSAGE_CODE_TALLY_SHEET_SUBMIT_IS_NOT_SUPPORTED
    #     )

    tally_sheet.set_submitted_version(None)

    db.session.commit()

    return TallySheetSchema().dump(tally_sheet).data, 201


@authorize(required_roles=ALL_ROLES)
def submit(tallySheetId, body):
    request_body = RequestBody(body)
    tallySheetVersionId = request_body.get("submittedVersionId")

    tally_sheet: TallySheetModel = TallySheet.get_by_id(tallySheetId=tallySheetId)

    if tally_sheet is None:
        raise NotFoundException(
            message="Tally sheet not found (tallySheetId=%d)" % tallySheetId,
            code=MESSAGE_CODE_TALLY_SHEET_NOT_FOUND
        )

    # if tally_sheet.tallySheetCode not in [TallySheetCodeEnum.PRE_41, TallySheetCodeEnum.CE_201,
    #                                       TallySheetCodeEnum.CE_201_PV, TallySheetCodeEnum.PRE_34_CO]:
    #     raise ForbiddenException(
    #         message="Submit operation is not supported for this tally sheet type.",
    #         code=MESSAGE_CODE_TALLY_SHEET_SUBMIT_IS_NOT_SUPPORTED
    #     )

    tally_sheet_version = TallySheetVersion.get_by_id(tallySheetVersionId=tallySheetVersionId,
                                                      tallySheetId=tallySheetId)

    if tally_sheet_version is None:
        raise NotFoundException(
            message="Tally sheet version not found (tallySheetVersionId=%d)" % tallySheetVersionId,
            code=MESSAGE_CODE_TALLY_SHEET_VERSION_NOT_FOUND
        )

    tally_sheet.set_submitted_version(tally_sheet_version)

    # if tally_sheet.tallySheetCode in [TallySheetCodeEnum.CE_201, TallySheetCodeEnum.CE_201_PV]:
    #     election = tally_sheet.submission.election
    #     electionId = election.parentElectionId
    #     countingCentreId = tally_sheet.areaId
    #     results = StatusCE201.get_status_records(electionId, countingCentreId)
    #
    #     for item in results:
    #         item.status = "Submitted"
    #
    # if tally_sheet.tallySheetCode in [TallySheetCodeEnum.PRE_41]:
    #     election = tally_sheet.submission.election
    #     electionId = election.parentElectionId
    #     countingCentreId = tally_sheet.areaId
    #     results = StatusPRE41.get_status_records(electionId, countingCentreId)
    #
    #     for item in results:
    #         item.status = "Submitted"
    #
    # if tally_sheet.tallySheetCode in [TallySheetCodeEnum.PRE_34_CO]:
    #     election = tally_sheet.submission.election
    #     electionId = election.parentElectionId
    #     countingCentreId = tally_sheet.areaId
    #     results = StatusPRE34.get_status_records(electionId, countingCentreId)
    #
    #     for item in results:
    #         item.status = "Submitted"

    db.session.commit()

    return TallySheetSchema().dump(tally_sheet).data, 201
