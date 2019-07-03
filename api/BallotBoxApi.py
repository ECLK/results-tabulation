from flask import abort
from schemas import BallotBox_Schema as Schema
from domain import BallotBoxDomain


def get_all():
    result = BallotBoxDomain.get_all()

    return Schema(many=True).dump(result).data


def create(body):
    result = BallotBoxDomain.create(body)

    return Schema().dump(result).data, 201
