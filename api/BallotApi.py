from util import RequestBody

from schemas import Ballot_Schema as Schema
from orm.entities import Ballot


def get_all():
    result = Ballot.get_all()

    return Schema(many=True).dump(result).data


def create(body):
    request_body = RequestBody(body)
    result = Ballot.create(
        electionId=request_body.get("electionId"),
        ballotId=request_body.get("ballotId")
    )

    return Schema().dump(result).data, 201
