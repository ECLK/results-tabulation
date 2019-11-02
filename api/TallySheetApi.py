from typing import Set

from app import db
from auth import authorize, DATA_EDITOR_ROLE, POLLING_DIVISION_REPORT_VERIFIER_ROLE, \
    ELECTORAL_DISTRICT_REPORT_VERIFIER_ROLE, NATIONAL_REPORT_VERIFIER_ROLE, has_role_based_access, ACCESS_TYPE_READ
from auth.AuthConstants import ALL_ROLES
from exception import NotFoundException, ForbiddenException
from exception.messages import MESSAGE_CODE_TALLY_SHEET_CANNOT_LOCK_BEFORE_SUBMIT, \
    MESSAGE_CODE_TALLY_SHEET_SUBMIT_IS_NOT_SUPPORTED, MESSAGE_CODE_TALLY_SHEET_NOT_FOUND, \
    MESSAGE_CODE_TALLY_SHEET_VERSION_NOT_FOUND, MESSAGE_CODE_TALLY_SHEET_INCOMPLETE_TALLY_SHEET_CANNOT_BE_LOCKED
from orm.entities.Submission import TallySheet
from orm.entities.Submission.TallySheet import TallySheetModel
from orm.entities.SubmissionVersion import TallySheetVersion
from orm.enums import TallySheetCodeEnum
from schemas import TallySheetSchema
from util import RequestBody, get_paginated_query


@authorize(required_roles=ALL_ROLES)
def getAll(electionId=None, areaId=None, tallySheetCode=None):
    result = TallySheet.get_all(
        electionId=electionId,
        areaId=areaId,
        tallySheetCode=tallySheetCode
    )

    result = get_paginated_query(result).all()

    # filter based on roles
    # filtered_results = [tally_sheet for tally_sheet in result if has_role_based_access(tally_sheet, ACCESS_TYPE_READ)]

    return TallySheetSchema(many=True).dump(result).data


@authorize(required_roles=ALL_ROLES)
def get_by_id(tallySheetId):
    tally_sheet = TallySheet.get_by_id(tallySheetId=tallySheetId)

    if tally_sheet is None:
        NotFoundException(
            message="Tally sheet not found (tallySheetId=%d)" % tallySheetId,
            code=MESSAGE_CODE_TALLY_SHEET_NOT_FOUND
        )

    return TallySheetSchema().dump(tally_sheet).data


@authorize(
    required_roles=[DATA_EDITOR_ROLE, POLLING_DIVISION_REPORT_VERIFIER_ROLE, ELECTORAL_DISTRICT_REPORT_VERIFIER_ROLE,
                    NATIONAL_REPORT_VERIFIER_ROLE])
def unlock(tallySheetId):
    tally_sheet = TallySheet.get_by_id(tallySheetId=tallySheetId)

    if tally_sheet is None:
        NotFoundException(
            message="Tally sheet not found (tallySheetId=%d)" % tallySheetId,
            code=MESSAGE_CODE_TALLY_SHEET_NOT_FOUND
        )

    tally_sheet.set_locked_version(None)

    db.session.commit()

    return TallySheetSchema().dump(tally_sheet).data, 201


@authorize(
    required_roles=[DATA_EDITOR_ROLE, POLLING_DIVISION_REPORT_VERIFIER_ROLE, ELECTORAL_DISTRICT_REPORT_VERIFIER_ROLE,
                    NATIONAL_REPORT_VERIFIER_ROLE])
def lock(tallySheetId, body):
    request_body = RequestBody(body)
    tallySheetVersionId = request_body.get("lockedVersionId")

    tally_sheet = TallySheet.get_by_id(tallySheetId=tallySheetId)

    if tally_sheet is None:
        raise NotFoundException("Tally sheet not found (tallySheetId=%d)" % tallySheetId)

    if tally_sheet.tallySheetCode in [TallySheetCodeEnum.PRE_41, TallySheetCodeEnum.CE_201,
                                      TallySheetCodeEnum.CE_201_PV,
                                      TallySheetCodeEnum.PRE_34_CO] and not tally_sheet.submitted:
        raise ForbiddenException(
            message="Tally sheet is not yet submitted, cannot lock.",
            code=MESSAGE_CODE_TALLY_SHEET_CANNOT_LOCK_BEFORE_SUBMIT
        )

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

    db.session.commit()

    return TallySheetSchema().dump(tally_sheet).data, 201


@authorize(required_roles=[DATA_EDITOR_ROLE])
def request_edit(tallySheetId):
    tally_sheet = TallySheet.get_by_id(tallySheetId=tallySheetId)

    if tally_sheet is None:
        raise NotFoundException(
            message="Tally sheet not found (tallySheetId=%d)" % tallySheetId,
            code=MESSAGE_CODE_TALLY_SHEET_NOT_FOUND
        )

    if tally_sheet.tallySheetCode not in [TallySheetCodeEnum.PRE_41, TallySheetCodeEnum.CE_201,
                                          TallySheetCodeEnum.CE_201_PV, TallySheetCodeEnum.PRE_34_CO]:
        raise ForbiddenException(
            message="Submit operation is not supported for this tally sheet type.",
            code=MESSAGE_CODE_TALLY_SHEET_SUBMIT_IS_NOT_SUPPORTED
        )

    tally_sheet.set_submitted_version(None)

    db.session.commit()

    return TallySheetSchema().dump(tally_sheet).data, 201


@authorize(required_roles=[DATA_EDITOR_ROLE])
def submit(tallySheetId, body):
    request_body = RequestBody(body)
    tallySheetVersionId = request_body.get("submittedVersionId")

    tally_sheet: TallySheetModel = TallySheet.get_by_id(tallySheetId=tallySheetId)

    if tally_sheet is None:
        raise NotFoundException(
            message="Tally sheet not found (tallySheetId=%d)" % tallySheetId,
            code=MESSAGE_CODE_TALLY_SHEET_NOT_FOUND
        )

    if tally_sheet.tallySheetCode not in [TallySheetCodeEnum.PRE_41, TallySheetCodeEnum.CE_201,
                                          TallySheetCodeEnum.CE_201_PV, TallySheetCodeEnum.PRE_34_CO]:
        raise ForbiddenException(
            message="Submit operation is not supported for this tally sheet type.",
            code=MESSAGE_CODE_TALLY_SHEET_SUBMIT_IS_NOT_SUPPORTED
        )

    tally_sheet_version = TallySheetVersion.get_by_id(tallySheetVersionId=tallySheetVersionId,
                                                      tallySheetId=tallySheetId)

    if tally_sheet_version is None:
        raise NotFoundException(
            message="Tally sheet version not found (tallySheetVersionId=%d)" % tallySheetVersionId,
            code=MESSAGE_CODE_TALLY_SHEET_VERSION_NOT_FOUND
        )

    tally_sheet.set_submitted_version(tally_sheet_version)

    db.session.commit()

    return TallySheetSchema().dump(tally_sheet).data, 201
