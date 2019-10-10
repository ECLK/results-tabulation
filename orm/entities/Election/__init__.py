from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from app import db
from orm.entities.Election import ElectionParty, ElectionCandidate, InvalidVoteCategory
from orm.entities.IO import File
from orm.enums import VoteTypeEnum
from util import get_paginated_query


class ElectionModel(db.Model):
    __tablename__ = 'election'
    electionId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    electionName = db.Column(db.String(100), nullable=False)
    parentElectionId = db.Column(db.Integer, db.ForeignKey("election.electionId"), nullable=True)
    voteType = db.Column(db.Enum(VoteTypeEnum), nullable=False)
    _parties = relationship("ElectionPartyModel")
    _invalidVoteCategories = relationship("InvalidVoteCategoryModel")

    subElections = relationship("ElectionModel")
    parentElection = relationship("ElectionModel", remote_side=[electionId])

    dataFileId = db.Column(db.Integer, db.ForeignKey(File.Model.__table__.c.fileId))
    partyCandidateFileId = db.Column(db.Integer, db.ForeignKey(File.Model.__table__.c.fileId))
    invalidVoteCategoriesFileId = db.Column(db.Integer, db.ForeignKey(File.Model.__table__.c.fileId))
    postalDataFileId = db.Column(db.Integer, db.ForeignKey(File.Model.__table__.c.fileId))

    def __init__(self, electionName, parentElectionId, voteType):
        super(ElectionModel, self).__init__(
            electionName=electionName,
            parentElectionId=parentElectionId,
            voteType=voteType
        )

        db.session.add(self)
        db.session.flush()

    @hybrid_property
    def mappedElectionIds(self):

        # TODO

        if self.parentElectionId is None:
            return [self.electionId]
        else:
            return [self.electionId, self.parentElectionId]

    @hybrid_property
    def subElectionIds(self):

        # TODO

        return [subElection.electionId for subElection in self.subElections]

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

    def add_sub_election(self, electionName, voteType):
        return create(
            electionName=electionName,
            parentElectionId=self.electionId,
            voteType=voteType
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


def create(electionName, parentElectionId=None, voteType=VoteTypeEnum.PostalAndNonPostal, files=None):
    result = Model(
        electionName=electionName,
        parentElectionId=parentElectionId,
        voteType=voteType
    )

    if files:
        data_file = File.createFromFileSource(
            fileSource=files.get("data")
        )

        party_candidate_file = File.createFromFileSource(
            fileSource=files.get("partyCandidate")
        )

        invalid_vote_categories_file = File.createFromFileSource(
            fileSource=files.get("invalidVoteCategories")
        )

        postal_data_file = File.createFromFileSource(
            fileSource=files.get("postalData")
        )

        result.dataFileId = data_file.fileId
        result.partyCandidateFileId = party_candidate_file.fileId
        result.invalidVoteCategoriesFileId = invalid_vote_categories_file.fileId
        result.postalDataFileId = postal_data_file.fileId

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
