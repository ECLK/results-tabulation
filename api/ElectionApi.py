import connexion

from app import db
from auth import ADMIN_ROLE, authorize
from orm.entities.Election.election_helper import get_root_token, build_presidential_election
from orm.entities import Election
from schemas import ElectionSchema as Schema
from util import RequestBody, get_paginated_query


def get_all():
    result = Election.get_all()

    result = get_paginated_query(result).all()

    return Schema(many=True).dump(result).data


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
