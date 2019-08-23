from util import RequestBody

from schemas import ElectorateSchema as Schema
from orm.entities import Electorate
import connexion


def get_all(electionId=None, electorateName=None, electorateType=None):
    result = Electorate.get_all(
        electionId=electionId,
        electorateName=electorateName,
        electorateType=electorateType
    )

    return Schema(many=True).dump(result).data
