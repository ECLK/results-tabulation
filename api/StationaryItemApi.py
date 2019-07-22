from schemas import StationaryItem_Schema as Schema
from orm.entities import StationaryItem


def get_all():
    result = StationaryItem.get_all()

    return Schema(many=True).dump(result).data
