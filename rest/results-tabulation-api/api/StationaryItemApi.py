from schemas import StationaryItem_Schema as Schema
from orm.entities import StationaryItem
from util import get_paginated_query


def get_all():
    result = StationaryItem.get_all()

    result = get_paginated_query(result).all()

    return Schema(many=True).dump(result).data
