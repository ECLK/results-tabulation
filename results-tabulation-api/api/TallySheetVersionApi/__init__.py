from flask import Response

from api import FileApi, TallySheetApi
from app import db, cache
from auth import authorize, get_user_access_area_ids
from constants.AUTH_CONSTANTS import ALL_ROLES
from exception import NotFoundException
from exception.messages import MESSAGE_CODE_TALLY_SHEET_NOT_FOUND, MESSAGE_CODE_TALLY_SHEET_VERSION_NOT_FOUND
from ext.ExtendedTallySheet import ExtendedTallySheet
from orm.entities.Submission import TallySheet
from orm.entities.SubmissionVersion import TallySheetVersion
from schemas import TallySheetVersionSchema
from util import get_paginated_query, RequestBody, validate_tally_sheet_version_request_content_special_characters


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
def letter_html(tallySheetId, tallySheetVersionId, body):
    request_body = RequestBody(body)
    signatures = request_body.get("signatures")

    user_access_area_ids = get_user_access_area_ids()

    return _cache_letter_html(user_access_area_ids=user_access_area_ids, tally_sheet_id=tallySheetId,
                              tally_sheet_version_id=tallySheetVersionId, signatures=signatures)


@cache.memoize()
def _cache_letter_html(user_access_area_ids, tally_sheet_id, tally_sheet_version_id, signatures):
    tally_sheet = TallySheet.get_by_id(tallySheetId=tally_sheet_id)

    if tally_sheet is None:
        raise NotFoundException(
            message="Tally sheet not found (tallySheetId=%d)" % tally_sheet_id,
            code=MESSAGE_CODE_TALLY_SHEET_NOT_FOUND
        )

    tally_sheet_version = TallySheetVersion.get_by_id(tallySheetId=tally_sheet_id,
                                                      tallySheetVersionId=tally_sheet_version_id)

    if tally_sheet_version is None:
        raise NotFoundException(
            message="Tally sheet version not found (tallySheetVersionId=%d)" % tally_sheet_version_id,
            code=MESSAGE_CODE_TALLY_SHEET_VERSION_NOT_FOUND
        )

    return Response(tally_sheet.html_letter(tallySheetVersionId=tally_sheet_version_id, signatures=signatures),
                    mimetype='text/html')


@authorize(required_roles=ALL_ROLES)
def html(tallySheetId, tallySheetVersionId):
    user_access_area_ids = get_user_access_area_ids()

    return _cache_html(user_access_area_ids=user_access_area_ids, tally_sheet_id=tallySheetId,
                       tally_sheet_version_id=tallySheetVersionId)


@cache.memoize()
def _cache_html(user_access_area_ids, tally_sheet_id, tally_sheet_version_id):
    tally_sheet = TallySheet.get_by_id(tallySheetId=tally_sheet_id)

    if tally_sheet is None:
        raise NotFoundException(
            message="Tally sheet not found (tallySheetId=%d)" % tally_sheet_id,
            code=MESSAGE_CODE_TALLY_SHEET_NOT_FOUND
        )

    tally_sheet_version = TallySheetVersion.get_by_id(tallySheetId=tally_sheet_id,
                                                      tallySheetVersionId=tally_sheet_version_id)

    if tally_sheet_version is None:
        raise NotFoundException(
            message="Tally sheet version not found (tallySheetVersionId=%d)" % tally_sheet_version_id,
            code=MESSAGE_CODE_TALLY_SHEET_VERSION_NOT_FOUND
        )

    return Response(tally_sheet.html(tallySheetVersionId=tally_sheet_version_id), mimetype='text/html')


@authorize(required_roles=ALL_ROLES)
def pdf(tallySheetId, tallySheetVersionId):
    user_access_area_ids = get_user_access_area_ids()

    return _cache_pdf(user_access_area_ids=user_access_area_ids, tally_sheet_id=tallySheetId,
                      tally_sheet_version_id=tallySheetVersionId)


@cache.memoize()
def _cache_pdf(user_access_area_ids, tally_sheet_id, tally_sheet_version_id):
    tally_sheet = TallySheet.get_by_id(tallySheetId=tally_sheet_id)

    if tally_sheet is None:
        raise NotFoundException(
            message="Tally sheet not found (tallySheetId=%d)" % tally_sheet_id,
            code=MESSAGE_CODE_TALLY_SHEET_NOT_FOUND
        )

    tally_sheet_version = TallySheetVersion.get_by_id(tallySheetId=tally_sheet_id,
                                                      tallySheetVersionId=tally_sheet_version_id)

    if tally_sheet_version is None:
        raise NotFoundException(
            message="Tally sheet version not found (tallySheetVersionId=%d)" % tally_sheet_version_id,
            code=MESSAGE_CODE_TALLY_SHEET_VERSION_NOT_FOUND
        )

    file_response = FileApi.get_download_file(fileId=tally_sheet_version.get_exported_pdf_file_id(
        tallySheetId=tally_sheet_id,
        tallySheetVersionId=tally_sheet_version_id
    ))

    db.session.commit()

    return file_response


@authorize(required_roles=ALL_ROLES)
def letter_pdf(tallySheetId, tallySheetVersionId, body):
    request_body = RequestBody(body)
    signatures = request_body.get("signatures")
    
    user_access_area_ids = get_user_access_area_ids()

    return _cache_letter_pdf(user_access_area_ids=user_access_area_ids, tally_sheet_id=tallySheetId,
                             tally_sheet_version_id=tallySheetVersionId, signatures=signatures)


@cache.memoize()
def _cache_letter_pdf(user_access_area_ids, tally_sheet_id, tally_sheet_version_id, signatures):
    tally_sheet = TallySheet.get_by_id(tallySheetId=tally_sheet_id)

    if tally_sheet is None:
        raise NotFoundException(
            message="Tally sheet not found (tallySheetId=%d)" % tally_sheet_id,
            code=MESSAGE_CODE_TALLY_SHEET_NOT_FOUND
        )

    tally_sheet_version = TallySheetVersion.get_by_id(tallySheetId=tally_sheet_id,
                                                      tallySheetVersionId=tally_sheet_version_id)

    if tally_sheet_version is None:
        raise NotFoundException(
            message="Tally sheet version not found (tallySheetVersionId=%d)" % tally_sheet_version_id,
            code=MESSAGE_CODE_TALLY_SHEET_VERSION_NOT_FOUND
        )

    file_response = FileApi.get_download_file(fileId=tally_sheet_version.get_exported_letter_pdf_file_id(
        tallySheetId=tally_sheet_id,
        tallySheetVersionId=tally_sheet_version_id,
        signatures=signatures
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
    validate_tally_sheet_version_request_content_special_characters(request_body.get("content"))

    if tally_sheet is None:
        raise NotFoundException(
            message="Tally sheet not found (tallySheetId=%d)" % tallySheetId,
            code=MESSAGE_CODE_TALLY_SHEET_NOT_FOUND
        )

    extended_tally_sheet: ExtendedTallySheet = tally_sheet.get_extended_tally_sheet()
    extended_tally_sheet.execute_tally_sheet_post(content=request_body.get("content"))

    db.session.commit()

    return TallySheetApi.get_by_id(tallySheetId=tallySheetId)
