from util import RequestBody

from schemas import BallotBox_Schema as Schema
from orm.entities import BallotBox


def get_all(ballotBoxId=None):
    result = BallotBox.get_all(
        ballotBoxId=ballotBoxId
    )

    return Schema(many=True).dump(result).data


def create(body):
    request_body = RequestBody(body)
    result = BallotBox.create(
        electionId=request_body.get("electionId"),
        ballotBoxId=request_body.get("ballotBoxId")
    )

    return Schema().dump(result).data, 201
