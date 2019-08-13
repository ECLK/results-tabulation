from app import db
from sqlalchemy.orm import relationship
from orm.entities import Election, Party, Candidate
from util import get_paginated_query


class ElectionPartyCandidateModel(db.Model):
    __tablename__ = 'election_party_candidate'
    electionId = db.Column(db.Integer, db.ForeignKey(Election.Model.__table__.c.electionId), primary_key=True)
    partyId = db.Column(db.Integer, db.ForeignKey(Party.Model.__table__.c.partyId), primary_key=True)
    candidateId = db.Column(db.Integer, db.ForeignKey(Candidate.Model.__table__.c.candidateId), primary_key=True)

    election = relationship(Election.Model, foreign_keys=[electionId])
    party = relationship(Party.Model, foreign_keys=[partyId])
    candidate = relationship(Candidate.Model, foreign_keys=[candidateId])

    __table_args__ = (
        # To avoid the same candidate being in multiple parties per election.
        db.UniqueConstraint('electionId', 'candidateId', name='CandidatePerElection'),
    )

Model = ElectionPartyCandidateModel


def get_all(electionId=None, partyId=None):
    query = Model.query

    if electionId is not None:
        query = query.filter(Model.electionId == electionId)

    if partyId is not None:
        query = query.filter(Model.partyId == partyId)

    result = get_paginated_query(query).all()

    return result


def get_by_id(electionId, partyId):
    result = Model.query.filter(
        Model.electionId == electionId,
        Model.partyId == partyId
    ).one_or_none()

    return result


def create(electionId, partyId, candidateId):
    result = Model(
        electionId=electionId,
        partyId=partyId,
        candidateId=candidateId
    )
    db.session.add(result)
    db.session.commit()

    return result
