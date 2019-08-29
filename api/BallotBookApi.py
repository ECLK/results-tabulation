from util import RequestBody

from schemas import BallotBookSchema as Schema
from orm.entities import BallotBook


def get_all():
    result = BallotBook.get_all(
    )

    return Schema(many=True).dump(result).data


def create(body):
    request_body = RequestBody(body)
    result = BallotBook.create(
        electionId=request_body.get("electionId"),
        fromBallotId=request_body.get("fromBallotId"),
        toBallotId=request_body.get("toBallotId")
    )

    return Schema().dump(result).data, 201
