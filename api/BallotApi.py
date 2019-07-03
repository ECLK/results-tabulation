from flask import abort
from schemas import Ballot_Schema as Schema
from domain import BallotDomain


def get_all():
    result = BallotDomain.get_all()

    return Schema(many=True).dump(result).data


def create(body):
    result = BallotDomain.create(body)

    return Schema().dump(result).data, 201
