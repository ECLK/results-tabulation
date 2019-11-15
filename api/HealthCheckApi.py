from util import RequestBody, get_area_type, get_paginated_query

from schemas import AreaSchema as Schema
from orm.entities import Area
import connexion


def get():
    return "Health Check Success!", 200
