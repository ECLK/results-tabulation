from app import db
from util import RequestBody, get_ballot_type

from schemas import Ballot_Schema as Schema
from orm.entities import Ballot
import connexion


def get_all(ballotId=None, ballotType=None, electionId=None):
    result = Ballot.get_all(
        ballotId=ballotId,
        ballotType=ballotType,
        electionId=electionId
    )

    return Schema(many=True).dump(result).data


def create(body):
    request_body = RequestBody(body)
    result = Ballot.create(
        electionId=request_body.get("electionId"),
        ballotId=request_body.get("ballotId"),
        ballotType=get_ballot_type(request_body.get("ballotType"))
    )

    db.session.commit()

    return Schema().dump(result).data, 201
