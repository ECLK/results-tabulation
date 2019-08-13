from util import RequestBody

from schemas import ElectionSchema as Schema
from orm.entities import Election
import connexion


def get_all():
    result = Election.get_all()

    return Schema(many=True).dump(result).data
