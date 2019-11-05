import connexion

from app import db
from auth import ADMIN_ROLE, authorize
from exception import NotFoundException
from exception.messages import MESSAGE_CODE_ELECTION_NOT_FOUND
from orm.entities.Election.election_helper import get_root_token, build_presidential_election
from orm.entities import Election, Area
from schemas import ElectionSchema as Schema, SimpleAreaSchema
from util import RequestBody, get_paginated_query


def get_all():
    result = Election.get_all()

    result = get_paginated_query(result).all()

    return Schema(many=True).dump(result).data


def get_by_id(electionId):
    result = Election.get_by_id(electionId=electionId)
    if result is None:
        raise NotFoundException(
            message="Election not found (electionId=%d)" % electionId,
            code=MESSAGE_CODE_ELECTION_NOT_FOUND
        )

    return Schema().dump(result).data


@authorize(required_roles=[ADMIN_ROLE])
def create(body):
    request_body = RequestBody(body)
    election_name = request_body.get("electionName")

    files = connexion.request.files
    polling_stations_dataset = files.get("pollingStationsDataset")
    postal_counting_centres_dataset = files.get("postalCountingCentresDataset")
    party_candidates_dataset = files.get("partyCandidatesDataset")
    invalid_vote_categories_dataset = files.get("invalidVoteCategoriesDataset")

    election = Election.create(electionName=election_name)
    election.set_polling_stations_dataset(fileSource=polling_stations_dataset)
    election.set_postal_counting_centres_dataset(fileSource=postal_counting_centres_dataset)
    election.set_party_candidates_dataset(fileSource=party_candidates_dataset)
    election.set_invalid_vote_categories_dataset(fileSource=invalid_vote_categories_dataset)

    build_presidential_election(root_election=election)

    db.session.commit()

    return Schema().dump(election).data


@authorize(required_roles=[ADMIN_ROLE])
def getRootToken(electionId):
    return get_root_token(electionId=electionId)


def get_all_areas(electionId):
    result = Area.get_all_areas_of_root_election(
        election_id=electionId
    )

    return SimpleAreaSchema(many=True).dump(result).data
