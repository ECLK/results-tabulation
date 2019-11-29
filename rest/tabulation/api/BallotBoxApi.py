from app import db
from util import RequestBody, get_paginated_query

from schemas import BallotBox_Schema as Schema
from orm.entities import BallotBox


def get_all(ballotBoxId=None, electionId=None):
    result = BallotBox.get_all(
        ballotBoxId=ballotBoxId,
        electionId=electionId
    )

    result = get_paginated_query(result).all()

    return Schema(many=True).dump(result).data


def create(body):
    request_body = RequestBody(body)
    result = BallotBox.create(
        electionId=request_body.get("electionId"),
        ballotBoxId=request_body.get("ballotBoxId")
    )

    db.session.commit()

    return Schema().dump(result).data, 201
