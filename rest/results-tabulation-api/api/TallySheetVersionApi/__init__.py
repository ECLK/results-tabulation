from flask import Response
from app import db
from auth import authorize
from constants.AUTH_CONSTANTS import ALL_ROLES
from exception import NotFoundException
from exception.messages import MESSAGE_CODE_TALLY_SHEET_NOT_FOUND, MESSAGE_CODE_TALLY_SHEET_VERSION_NOT_FOUND
from ext.ExtendedTallySheet import ExtendedTallySheet
from orm.entities.Submission import TallySheet
from orm.entities.SubmissionVersion import TallySheetVersion
from schemas import TallySheetVersionSchema
from util import get_paginated_query, RequestBody


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

    tally_sheet, tally_sheet_version = TallySheet.create_latest_version(
        tallySheetId=tallySheetId,
        content=request_body.get("content")
    )

    db.session.commit()

    tally_sheet.create_tally_sheet_version_rows(tally_sheet_version=tally_sheet_version, post_save=True)

    db.session.commit()

    extended_tally_sheet: ExtendedTallySheet = tally_sheet.get_extended_tally_sheet()

    extended_tally_sheet.on_after_tally_sheet_post(tally_sheet=tally_sheet, tally_sheet_version=tally_sheet_version)

    db.session.commit()

    return TallySheetVersionSchema().dump(tally_sheet_version).data
