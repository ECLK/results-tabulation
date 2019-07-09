from flask import abort
from schemas import BallotBox_Schema as Schema
from domain import BallotBoxDomain
from util import RequestBody


def get_all():
    result = BallotBoxDomain.get_all()

    return Schema(many=True).dump(result).data


def create(body):
    request_body = RequestBody(body)
    result = BallotBoxDomain.create(
        ballotBoxId=request_body.get("ballotBoxId")
    )

    return Schema().dump(result).data, 201
