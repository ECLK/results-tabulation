from flask import Response

from app import db
from auth import authorize
from auth.AuthConstants import ALL_ROLES
from orm.entities.SubmissionVersion import TallySheetVersion
from schemas import Ballot_Schema as Schema
from util import RequestBody


def get_all(tallySheetId):
    result = TallySheetVersion.get_all(tallySheetId=tallySheetId)

    return Schema(many=True).dump(result).data


def create(body):
    request_body = RequestBody(body)
    result = TallySheetVersion.create(
        tallySheetId=request_body.get("tallySheetId")
    )

    db.session.commit()

    return Schema().dump(result).data, 201


@authorize(required_roles=ALL_ROLES)
def html(tallySheetId, tallySheetVersionId):
    tallySheetVersion = TallySheetVersion.get_by_id(tallySheetVersionId=tallySheetVersionId)

    db.session.commit()

    return Response(tallySheetVersion.html(), mimetype='text/html')
