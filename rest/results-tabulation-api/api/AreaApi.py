from schemas import AreaSchema
from util import get_area_type, get_paginated_query
from orm.entities import Area


def get_all(electionId=None, areaName=None, associatedAreaId=None, areaType=None):
    query = Area.get_all(
        election_id=electionId,
        area_name=areaName,
        associated_area_id=associatedAreaId,
        area_type=get_area_type(area_type=areaType)
    )
    query = get_paginated_query(query)
    result = query.all()

    return AreaSchema(many=True).dump(result).data


def get_by_id(areaId):
    result = Area.get_by_id(areaId=areaId)

    return AreaSchema().dump(result).data
