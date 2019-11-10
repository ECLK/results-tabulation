from flask import Response
from app import db
from auth import authorize
from auth.AuthConstants import ALL_ROLES
from exception import NotFoundException
from exception.messages import MESSAGE_CODE_TALLY_SHEET_NOT_FOUND, MESSAGE_CODE_TALLY_SHEET_VERSION_NOT_FOUND
from orm.entities.Submission import TallySheet
from orm.entities.SubmissionVersion import TallySheetVersion
from schemas import TallySheetVersionSchema
from util import get_paginated_query


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

    return Response(tally_sheet_version.html(), mimetype='text/html')


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

    return Response(tally_sheet_version.html(), mimetype='text/html')
