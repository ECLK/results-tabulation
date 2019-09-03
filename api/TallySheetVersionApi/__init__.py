from app import db
from util import RequestBody
from schemas import Ballot_Schema as Schema
from orm.entities.SubmissionVersion import TallySheetVersion


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
