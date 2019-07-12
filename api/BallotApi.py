from flask import abort
from schemas import Ballot_Schema as Schema
from domain import BallotDomain
from util import RequestBody


def get_all():
    result = BallotDomain.get_all()

    return Schema(many=True).dump(result).data


def create(body):
    request_body = RequestBody(body)
    result = BallotDomain.create(
        electionId=request_body.get("electionId"),
        ballotId=request_body.get("ballotId")
    )

    return Schema().dump(result).data, 201
