from util import RequestBody, get_paginated_query

from schemas import OfficeSchema as Schema
from orm.entities import Office
import connexion


def get_all(electionId=None, officeName=None, parentOfficeId=None, officeType=None):
    result = Office.get_all(
        electionId=electionId,
        officeName=officeName,
        parentOfficeId=parentOfficeId,
        officeType=officeType
    )

    result = get_paginated_query(result).all()

    return Schema(many=True).dump(result).data
