from flask import Response

from api import FileApi
from api.TallySheetApi import refactor_tally_sheet_response
from app import db
from auth import authorize
from constants.AUTH_CONSTANTS import ALL_ROLES
from exception import NotFoundException, InvalidInputException
from exception.messages import MESSAGE_CODE_TALLY_SHEET_NOT_FOUND, MESSAGE_CODE_TALLY_SHEET_VERSION_NOT_FOUND, \
    MESSAGE_CODE_INVALID_INPUT
from ext.ExtendedTallySheet import ExtendedTallySheet
from orm.entities.Submission import TallySheet
from orm.entities.SubmissionVersion import TallySheetVersion
from schemas import TallySheetVersionSchema, TallySheetSchema_1
from util import get_paginated_query, RequestBody, input_is_valid


def get_all(tallySheetId):
    result = TallySheetVersion.get_all(tallySheetId=tallySheetId)

    result = get_paginated_query(result).all()

    return TallySheetVersionSchema(many=True).dump(result).data


@authorize(required_roles=ALL_ROLES)
def create_empty(tallySheetId):
    tallySheet, tallySheetVersion = TallySheet.create_empty_version(
        tallySheetId=tallySheetId
    )
    db.session.commit()

    return TallySheetVersionSchema().dump(tallySheetVersion).data


@authorize(required_roles=ALL_ROLES)
def create_empty_and_get_html(tallySheetId):
    tallySheet, tallySheetVersion = TallySheet.create_empty_version(
        tallySheetId=tallySheetId
    )
    db.session.commit()

    return Response(tallySheetVersion.html(), mimetype='text/html')


@authorize(required_roles=ALL_ROLES)
def letter_html(tallySheetId, tallySheetVersionId):
    tally_sheet = TallySheet.get_by_id(tallySheetId=tallySheetId)

    if tally_sheet is None:
        raise NotFoundException(
            message="Tally sheet not found (tallySheetId=%d)" % tallySheetId,
            code=MESSAGE_CODE_TALLY_SHEET_NOT_FOUND
        )

    tally_sheet_version = TallySheetVersion.get_by_id(tallySheetId=tallySheetId,
                                                      tallySheetVersionId=tallySheetVersionId)

    if tally_sheet_version is None:
        raise NotFoundException(
            message="Tally sheet version not found (tallySheetVersionId=%d)" % tallySheetVersionId,
            code=MESSAGE_CODE_TALLY_SHEET_VERSION_NOT_FOUND
        )

    return Response(tally_sheet.html_letter(tallySheetVersionId=tallySheetVersionId), mimetype='text/html')


@authorize(required_roles=ALL_ROLES)
def html(tallySheetId, tallySheetVersionId):
    tally_sheet = TallySheet.get_by_id(tallySheetId=tallySheetId)

    if tally_sheet is None:
        raise NotFoundException(
            message="Tally sheet not found (tallySheetId=%d)" % tallySheetId,
            code=MESSAGE_CODE_TALLY_SHEET_NOT_FOUND
        )

    tally_sheet_version = TallySheetVersion.get_by_id(tallySheetId=tallySheetId,
                                                      tallySheetVersionId=tallySheetVersionId)

    if tally_sheet_version is None:
        raise NotFoundException(
            message="Tally sheet version not found (tallySheetVersionId=%d)" % tallySheetVersionId,
            code=MESSAGE_CODE_TALLY_SHEET_VERSION_NOT_FOUND
        )

    return Response(tally_sheet.html(tallySheetVersionId=tallySheetVersionId), mimetype='text/html')


@authorize(required_roles=ALL_ROLES)
def pdf(tallySheetId, tallySheetVersionId):
    tally_sheet = TallySheet.get_by_id(tallySheetId=tallySheetId)

    if tally_sheet is None:
        raise NotFoundException(
            message="Tally sheet not found (tallySheetId=%d)" % tallySheetId,
            code=MESSAGE_CODE_TALLY_SHEET_NOT_FOUND
        )

    tally_sheet_version = TallySheetVersion.get_by_id(tallySheetId=tallySheetId,
                                                      tallySheetVersionId=tallySheetVersionId)

    if tally_sheet_version is None:
        raise NotFoundException(
            message="Tally sheet version not found (tallySheetVersionId=%d)" % tallySheetVersionId,
            code=MESSAGE_CODE_TALLY_SHEET_VERSION_NOT_FOUND
        )

    file_response = FileApi.get_download_file(fileId=tally_sheet_version.get_exported_pdf_file_id(
        tallySheetId=tallySheetId,
        tallySheetVersionId=tallySheetVersionId
    ))

    db.session.commit()

    return file_response


@authorize(required_roles=ALL_ROLES)
def letter_pdf(tallySheetId, tallySheetVersionId):
    tally_sheet = TallySheet.get_by_id(tallySheetId=tallySheetId)

    if tally_sheet is None:
        raise NotFoundException(
            message="Tally sheet not found (tallySheetId=%d)" % tallySheetId,
            code=MESSAGE_CODE_TALLY_SHEET_NOT_FOUND
        )

    tally_sheet_version = TallySheetVersion.get_by_id(tallySheetId=tallySheetId,
                                                      tallySheetVersionId=tallySheetVersionId)

    if tally_sheet_version is None:
        raise NotFoundException(
            message="Tally sheet version not found (tallySheetVersionId=%d)" % tallySheetVersionId,
            code=MESSAGE_CODE_TALLY_SHEET_VERSION_NOT_FOUND
        )

    file_response = FileApi.get_download_file(fileId=tally_sheet_version.get_exported_letter_pdf_file_id(
        tallySheetId=tallySheetId,
        tallySheetVersionId=tallySheetVersionId
    ))

    db.session.commit()

    return file_response


@authorize(required_roles=ALL_ROLES)
def get_by_id(tallySheetId, tallySheetVersionId):
    tallySheet = TallySheet.get_by_id(tallySheetId=tallySheetId)
    if tallySheet is None:
        raise NotFoundException(
            message="Tally sheet not found (tallySheetId=%d)" % tallySheetId,
            code=MESSAGE_CODE_TALLY_SHEET_NOT_FOUND
        )

    result = TallySheetVersion.get_by_id(
        tallySheetId=tallySheetId,
        tallySheetVersionId=tallySheetVersionId
    )

    return TallySheetVersionSchema().dump(result).data


@authorize(required_roles=ALL_ROLES)
def create(tallySheetId, body):
    request_body = RequestBody(body)
    tally_sheet = TallySheet.get_by_id(tallySheetId=tallySheetId)

    # validate user inputs to prevent XSS attacks
    if not input_is_valid(request_body.get("content")):
        raise InvalidInputException(
            message="Invalid input detected. Use of disallowed characters/invalid input length detected",
            code=MESSAGE_CODE_INVALID_INPUT
        )

    if tally_sheet is None:
        raise NotFoundException(
            message="Tally sheet not found (tallySheetId=%d)" % tallySheetId,
            code=MESSAGE_CODE_TALLY_SHEET_NOT_FOUND
        )

    extended_tally_sheet: ExtendedTallySheet = tally_sheet.get_extended_tally_sheet()
    extended_tally_sheet.execute_tally_sheet_post(content=request_body.get("content"))

    db.session.commit()

    return TallySheetSchema_1().dump(refactor_tally_sheet_response(tally_sheet)).data
