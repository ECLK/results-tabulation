from sqlalchemy.ext.associationproxy import association_proxy

from app import db
from sqlalchemy.orm import relationship
from orm.entities import Election, Party
from orm.entities.Election import ElectionPartyCandidate
from util import get_paginated_query


class ElectionPartyModel(db.Model):
    __tablename__ = 'election_party'
    electionId = db.Column(db.Integer, db.ForeignKey(Election.Model.__table__.c.electionId), primary_key=True)
    partyId = db.Column(db.Integer, db.ForeignKey(Party.Model.__table__.c.partyId), primary_key=True)

    election = relationship(Election.Model, foreign_keys=[electionId])
    party = relationship(Party.Model, foreign_keys=[partyId])
    candidates = relationship(
        "CandidateModel",
        secondary="election_party_candidate",
        primaryjoin="and_(ElectionPartyModel.electionId==ElectionPartyCandidateModel.electionId, ElectionPartyModel.partyId==ElectionPartyCandidateModel.partyId)",
        secondaryjoin="ElectionPartyCandidateModel.candidateId==CandidateModel.candidateId"
    )

    partyName = association_proxy("party", "partyName")
    partySymbolFileId = association_proxy("party", "partySymbolFileId")
    partySymbol = association_proxy("party", "partySymbol")

    def add_candidate(self, candidateId):
        ElectionPartyCandidate.create(
            electionId=self.electionId,
            partyId=self.partyId,
            candidateId=candidateId
        )


Model = ElectionPartyModel


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


def create(electionId, partyId):
    result = Model(
        electionId=electionId,
        partyId=partyId
    )
    db.session.add(result)
    db.session.commit()

    return result
