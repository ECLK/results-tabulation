from util import get_area_type

from schemas import SimpleAreaSchema
from orm.entities import Area


def get_all(electionId=None, areaName=None, associatedAreaId=None, areaType=None):
    result = Area.get_all(
        election_id=electionId,
        area_name=areaName,
        associated_area_id=associatedAreaId,
        area_type=get_area_type(area_type=areaType)
    )

    # result = get_paginated_query(result).all()
    result = result.all()

    return SimpleAreaSchema(many=True).dump(result).data


def get_by_id(areaId):
    result = Area.get_by_id(areaId=areaId)

    return SimpleAreaSchema().dump(result).data
