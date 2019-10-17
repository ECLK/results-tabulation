from util import RequestBody, get_paginated_query

from schemas import ElectorateSchema as Schema
from orm.entities import Electorate
import connexion


def get_all(electionId=None, electorateName=None, parentElectorateId=None, electorateType=None):
    result = Electorate.get_all(
        electionId=electionId,
        electorateName=electorateName,
        parentElectorateId=parentElectorateId,
        electorateType=electorateType
    )

    result = get_paginated_query(result).all()

    return Schema(many=True).dump(result).data
