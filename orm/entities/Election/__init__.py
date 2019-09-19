from sqlalchemy.ext.hybrid import hybrid_property

from app import db
from sqlalchemy.orm import relationship

from orm.entities.Election import ElectionParty, ElectionCandidate, InvalidVoteCategory
from util import get_paginated_query


class ElectionModel(db.Model):
    __tablename__ = 'election'
    electionId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    electionName = db.Column(db.String(100), nullable=False)
    parentElectionId = db.Column(db.Integer, db.ForeignKey("election.electionId"), nullable=True)
    _parties = relationship("ElectionPartyModel")
    _invalidVoteCategories = relationship("InvalidVoteCategoryModel")

    subElections = relationship("ElectionModel")
    parentElection = relationship("ElectionModel", remote_side=[electionId])

    def __init__(self, electionName, parentElectionId):
        super(ElectionModel, self).__init__(
            electionName=electionName,
            parentElectionId=parentElectionId
        )

        db.session.add(self)
        db.session.flush()

    @hybrid_property
    def parties(self):
        if self.parentElectionId is None:
            return self._parties
        else:
            return self.parentElection.parties

    @hybrid_property
    def invalidVoteCategories(self):
        if self.parentElectionId is None:
            return self._invalidVoteCategories
        else:
            return self.parentElection.invalidVoteCategories

    def add_sub_election(self, electionName):
        return create(
            electionName=electionName,
            parentElectionId=self.electionId
        )

    def add_invalid_vote_category(self, categoryDescription):
        return InvalidVoteCategory.create(
            electionId=self.electionId,
            categoryDescription=categoryDescription
        )

    def add_party(self, partyId):
        return ElectionParty.create(
            electionId=self.electionId,
            partyId=partyId
        )

    def add_candidate(self, partyId, candidateId):
        return ElectionCandidate.create(
            electionId=self.electionId,
            partyId=partyId,
            candidateId=candidateId
        )


Model = ElectionModel


def create(electionName, parentElectionId=None):
    result = Model(
        electionName=electionName,
        parentElectionId=parentElectionId
    )

    return result


def get_all():
    query = Model.query.filter(
        Model.parentElectionId == None
    )

    result = get_paginated_query(query).all()

    return result


def get_by_id(electionId):
    result = Model.query.filter(
        Model.electionId == electionId
    ).one_or_none()

    return result


def create_tally_sheets(electionId, electionType):
    election = get_by_id(electionId=electionId)

    # if electionType == "Precidential":
