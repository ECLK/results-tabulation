from flask import abort
from util import RequestBody

from schemas import StationaryItem_Schema as Schema
from domain import StationaryItemDomain


def get_all():
    result = StationaryItemDomain.get_all()

    return Schema(many=True).dump(result).data
