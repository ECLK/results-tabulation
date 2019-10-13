import os
from datetime import datetime
from unittest.mock import patch

import pytest

from app import create_app, db
from orm.entities import Election
from orm.entities.Audit.Stamp import Stamp


@pytest.fixture(scope="session")
def test_client():
    connex_app = create_app()
    flask_app = connex_app.app
    tc = flask_app.test_client()

    @patch("orm.entities.Audit.Stamp.create")
    def create_test_election(mock_stamp_create):
        mock_stamp = Stamp()
        mock_stamp.ip = "0.0.0.0"
        mock_stamp.createdBy = "TestAdmin"
        mock_stamp.createdAt = datetime.now()
        db.session.add(mock_stamp)
        db.session.flush()
        mock_stamp_create.return_value = mock_stamp

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

        election = create_test_election()

        from orm.entities.Election.election_helper import get_root_token
        jwt_token = get_root_token(election.electionId)

        tc.environ_base['HTTP_AUTHORIZATION'] = 'Bearer ' + jwt_token

        yield tc
