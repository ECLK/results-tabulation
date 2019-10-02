from flask import Response

from app import db
from auth import authorize
from auth.AuthConstants import ALL_ROLES
from exception import NotFoundException
from orm.entities.Submission import TallySheet
from orm.entities.SubmissionVersion import TallySheetVersion
from schemas import TallySheetVersionSchema
from util import RequestBody


def get_all(tallySheetId):
    result = TallySheetVersion.get_all(tallySheetId=tallySheetId)

    return TallySheetVersionSchema(many=True).dump(result).data


def create(body):
    request_body = RequestBody(body)
    result = TallySheetVersion.create(
        tallySheetId=request_body.get("tallySheetId")
    )

    db.session.commit()

    return TallySheetVersionSchema().dump(result).data, 201


@authorize(required_roles=ALL_ROLES)
def html(tallySheetId, tallySheetVersionId):
    tally_sheet = TallySheet.get_by_id(tallySheetId=tallySheetId)

    if tally_sheet is None:
        raise NotFoundException("Tally sheet not found (tallySheetId=%d)" % tallySheetId)

    tally_sheet_version = TallySheetVersion.get_by_id(tallySheetVersionId=tallySheetVersionId)

    if tally_sheet_version is None:
        NotFoundException("Tally sheet version not found (tallySheetVersionId=%d)" % tallySheetVersionId)

    db.session.commit()

    return Response(tally_sheet_version.html(), mimetype='text/html')
