import os
import tempfile

import connexion

from app import db
from auth import ADMIN_ROLE, authorize
from build_database import get_root_token, build_database_from_api
from orm.entities import Election
from orm.entities.IO import File
from schemas import ElectionSchema as Schema
from util import RequestBody


def get_all():
    result = Election.get_all()

    return Schema(many=True).dump(result).data


# @authorize(required_roles=[ADMIN_ROLE])
# def createFromDataset(dataset):
#     election = build_database(dataset=dataset)
#
#     return Schema().dump(election).data


@authorize(required_roles=[ADMIN_ROLE])
def create(body):
    request_body = RequestBody(body)
    election_name = request_body.get("name")
    files = connexion.request.files
    election = Election.create(electionName=election_name, files=files)

    with tempfile.TemporaryDirectory() as temp_dir:
        File.copy_file(election.dataFileId, os.path.join(temp_dir, "data.csv"))
        File.copy_file(election.partyCandidateFileId, os.path.join(temp_dir, "party-candidate.csv"))
        File.copy_file(election.invalidVoteCategoriesFileId, os.path.join(temp_dir, "invalid-vote-categories.csv"))
        File.copy_file(election.postalDataFileId, os.path.join(temp_dir, "postal-data.csv"))

        build_database_from_api(root_election=election, csv_dir=temp_dir)

    db.session.commit()

    return Schema().dump(election).data


@authorize(required_roles=[ADMIN_ROLE])
def getRootToken(electionId):
    return get_root_token(electionId=electionId)
