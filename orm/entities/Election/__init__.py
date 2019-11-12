from typing import Set

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, aliased

from app import db
from auth import get_user_access_area_ids
from orm.entities.Election import ElectionParty, ElectionCandidate, InvalidVoteCategory
from orm.entities.IO import File
from orm.enums import VoteTypeEnum
from sqlalchemy import and_, func, or_


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

    pollingStationsDatasetId = db.Column(db.Integer, db.ForeignKey(File.Model.__table__.c.fileId))
    postalCountingCentresDatasetId = db.Column(db.Integer, db.ForeignKey(File.Model.__table__.c.fileId))
    partyCandidateDatasetId = db.Column(db.Integer, db.ForeignKey(File.Model.__table__.c.fileId))
    invalidVoteCategoriesDatasetId = db.Column(db.Integer, db.ForeignKey(File.Model.__table__.c.fileId))

    pollingStationsDataset = relationship(File.Model, foreign_keys=[pollingStationsDatasetId])
    postalCountingCentresDataset = relationship(File.Model, foreign_keys=[postalCountingCentresDatasetId])
    partyCandidateDataset = relationship(File.Model, foreign_keys=[partyCandidateDatasetId])
    invalidVoteCategoriesDataset = relationship(File.Model, foreign_keys=[invalidVoteCategoriesDatasetId])

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

    def set_polling_stations_dataset(self, fileSource):
        dataset = File.createFromFileSource(fileSource=fileSource)
        self.pollingStationsDatasetId = dataset.fileId

    def set_postal_counting_centres_dataset(self, fileSource):
        dataset = File.createFromFileSource(fileSource=fileSource)
        self.postalCountingCentresDatasetId = dataset.fileId

    def set_party_candidates_dataset(self, fileSource):
        dataset = File.createFromFileSource(fileSource=fileSource)
        self.partyCandidateDatasetId = dataset.fileId

    def set_invalid_vote_categories_dataset(self, fileSource):
        dataset = File.createFromFileSource(fileSource=fileSource)
        self.invalidVoteCategoriesDatasetId = dataset.fileId

    def get_root_election(self):
        if self.parentElectionId is None:
            return self
        else:
            return self.parentElection

    def get_official_name(self):
        if self.parentElectionId is None:
            return self.electionName
        else:
            return self.parentElection.get_official_name()


Model = ElectionModel


def create(electionName, parentElectionId=None,
           voteType=VoteTypeEnum.PostalAndNonPostal):
    election = Model(
        electionName=electionName,
        parentElectionId=parentElectionId,
        voteType=voteType
    )

    return election


def get_authorized_election_ids():
    from orm.entities import Area

    user_access_area_ids: Set[int] = get_user_access_area_ids()

    authorized_elections = db.session.query(
        Model
    ).join(
        Area.Model,
        Area.Model.electionId == Model.electionId
    ).filter(
        Area.Model.areaId.in_(user_access_area_ids)
    ).group_by(
        Area.Model.electionId
    ).all()

    authorized_election_ids = []
    for authorized_election in authorized_elections:
        authorized_election_ids.extend(authorized_election.mappedElectionIds)

    return authorized_election_ids


def get_all():
    authorized_election_ids = get_authorized_election_ids()

    query = Model.query.filter(
        Model.electionId.in_(authorized_election_ids),
        Model.parentElectionId == None
    )

    return query


def get_by_id(electionId):
    authorized_election_ids = get_authorized_election_ids()

    result = Model.query.filter(
        Model.electionId == electionId,
        Model.electionId.in_(authorized_election_ids)
    ).one_or_none()

    return result


def create_tally_sheets(electionId, electionType):
    election = get_by_id(electionId=electionId)

    # if electionType == "Precidential":
