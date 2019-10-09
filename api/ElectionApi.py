from auth import ADMIN_ROLE, authorize
from build_database import build_database, get_root_token
from util import RequestBody

from schemas import ElectionSchema as Schema
from orm.entities import Election
import connexion


def get_all():
    result = Election.get_all()

    return Schema(many=True).dump(result).data


@authorize(required_roles=[ADMIN_ROLE])
def createFromDataset(dataset):
    election = build_database(dataset=dataset)

    return Schema().dump(election).data


@authorize(required_roles=[ADMIN_ROLE])
def getRootToken(electionId):
    return get_root_token(electionId=electionId)
