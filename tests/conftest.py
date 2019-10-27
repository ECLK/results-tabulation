import os

import pytest

import auth
from app import create_app, db
from orm.entities import Election


@pytest.fixture(scope="session")
def test_client():
    connex_app = create_app()
    flask_app = connex_app.app
    tc = flask_app.test_client()

    def create_test_election():
        from orm.entities.Election.election_helper import build_presidential_election
        election = Election.create(electionName="Test Election")

        basedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "sample-data", "test")
        party_candidate_dataset_file = os.path.join(basedir, "party-candidate.csv")
        polling_station_dataset_file = os.path.join(basedir, "data.csv")
        postal_counting_centers_dataset_file = os.path.join(basedir, "postal-data.csv")
        invalid_vote_categories_dataset_file = os.path.join(basedir, "invalid-vote-categories.csv")

        build_presidential_election(root_election=election,
                                    party_candidate_dataset_file=party_candidate_dataset_file,
                                    polling_station_dataset_file=polling_station_dataset_file,
                                    postal_counting_centers_dataset_file=postal_counting_centers_dataset_file,
                                    invalid_vote_categories_dataset_file=invalid_vote_categories_dataset_file)
        return election

    with connex_app.app.app_context():
        db.create_all()
        db.session.commit()

        with connex_app.app.test_request_context(environ_base={'REMOTE_ADDR': '1.2.3.4'}) as test_request_ctx:
            test_request_ctx.connexion_context = {auth.USER_NAME: 'Test User'}
            election = create_test_election()

        from orm.entities.Election.election_helper import get_root_token
        jwt = get_root_token(election.electionId)

        tc.http_headers = {
            auth.JWT_TOKEN_HEADER_KEY: jwt
        }

        yield tc
