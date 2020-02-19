"""empty message

Revision ID: 7bdab37d8bbf
Revises: eb0d667f2b5e
Create Date: 2020-02-18 09:29:35.407457

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import Session, relationship
from sqlalchemy.ext.declarative import declarative_base
from tqdm import tqdm

# revision identifiers, used by Alembic.
revision = '7bdab37d8bbf'
down_revision = 'eb0d667f2b5e'
branch_labels = None
depends_on = None

Base = declarative_base()
bind = op.get_bind()
session = Session(bind=bind)
db = sa


class _ElectionParty(Base):
    __tablename__ = 'election_party'
    electionPartyId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    electionId = db.Column(db.Integer)
    partyId = db.Column(db.Integer)

    @classmethod
    def create(cls, electionId, partyId):
        party = _ElectionParty(
            electionId=electionId,
            partyId=partyId
        )

        session.add(party)
        session.flush()

        return party


class _ElectionCandidate(Base):
    __tablename__ = 'election_candidate'
    electionCandidateId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    electionId = db.Column(db.Integer)
    partyId = db.Column(db.Integer)
    candidateId = db.Column(db.Integer)
    qualifiedForPreferences = db.Column(db.Boolean, default=False, nullable=False)

    @classmethod
    def create(cls, electionId, candidateId, partyId):
        candidate = _ElectionCandidate(
            electionId=electionId,
            candidateId=candidateId,
            partyId=partyId
        )

        session.add(candidate)
        session.flush()

        return candidate


class _InvalidVoteCategory(Base):
    __tablename__ = 'election_invalidVoteCategory'
    invalidVoteCategoryId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    electionId = db.Column(db.Integer)
    categoryDescription = db.Column(db.String(300))

    @classmethod
    def create(cls, electionId, categoryDescription):
        invalid_vote_category = _InvalidVoteCategory(
            electionId=electionId,
            categoryDescription=categoryDescription
        )

        session.add(invalid_vote_category)
        session.flush()

        return invalid_vote_category


class _Election(Base):
    __tablename__ = 'election'
    electionId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    electionName = db.Column(db.String(100))
    rootElectionId = db.Column(db.Integer)
    parentElectionId = db.Column(db.Integer)
    voteType = db.Column(db.String(100))
    electionTemplateName = db.Column(db.String(100))
    isListed = db.Column(db.Boolean)

    def add_invalid_vote_category(self, categoryDescription):
        invalid_vote_category = session.query(_InvalidVoteCategory).filter(
            _InvalidVoteCategory.electionId == self.electionId,
            _InvalidVoteCategory.categoryDescription == categoryDescription
        ).one_or_none()

        if invalid_vote_category is None:
            invalid_vote_category = _InvalidVoteCategory.create(
                electionId=self.electionId,
                categoryDescription=categoryDescription
            )

        return invalid_vote_category

    def add_party(self, partyId):
        election_party = session.query(_ElectionParty).filter(
            _ElectionParty.partyId == partyId,
            _ElectionParty.electionId == self.electionId
        ).one_or_none()

        if election_party is None:
            election_party = _ElectionParty.create(
                electionId=self.electionId,
                partyId=partyId
            )

        return election_party

    def add_candidate(self, partyId, candidateId):
        election_candidate = session.query(_ElectionCandidate).filter(
            _ElectionCandidate.partyId == partyId,
            _ElectionCandidate.candidateId == candidateId,
            _ElectionCandidate.electionId == self.electionId
        ).one_or_none()

        if election_candidate is None:
            election_candidate = _ElectionCandidate.create(
                electionId=self.electionId,
                partyId=partyId,
                candidateId=candidateId
            )

        return election_candidate


def upgrade():
    existing_elections = session.query(_Election).all()

    print(" -- Adding mappings to parties, candidates and invalid vote categories of each election.")
    for existing_election in tqdm(existing_elections):
        root_election_election_candidates = session.query(_ElectionCandidate).filter(
            _ElectionCandidate.electionId == existing_election.rootElectionId
        )
        for root_election_election_candidate in root_election_election_candidates:
            existing_election.add_party(
                partyId=root_election_election_candidate.partyId
            )
            existing_election.add_candidate(
                partyId=root_election_election_candidate.partyId,
                candidateId=root_election_election_candidate.candidateId
            )

        invalid_vote_categories = session.query(_InvalidVoteCategory).filter(
            _InvalidVoteCategory.electionId == existing_election.rootElectionId
        )
        for invalid_vote_category in invalid_vote_categories:
            existing_election.add_invalid_vote_category(
                categoryDescription=invalid_vote_category.categoryDescription
            )

        session.commit()


def downgrade():
    pass
