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
    rootElectionId = db.Column(db.Integer, db.ForeignKey("election.electionId", name="fk_election_root_election_id"),
                               nullable=True)
    parentElectionId = db.Column(db.Integer, db.ForeignKey("election.electionId"), nullable=True)
    voteType = db.Column(db.Enum(VoteTypeEnum), nullable=False)
    isListed = db.Column(db.String(100), nullable=False)

    _parties = relationship("ElectionPartyModel")
    _invalidVoteCategories = relationship("InvalidVoteCategoryModel")
    subElections = relationship("ElectionModel", foreign_keys=[parentElectionId])
    rootElection = relationship("ElectionModel", remote_side=[electionId], foreign_keys=[rootElectionId])
    parentElection = relationship("ElectionModel", remote_side=[electionId], foreign_keys=[parentElectionId])

    pollingStationsDatasetId = db.Column(db.Integer, db.ForeignKey(File.Model.__table__.c.fileId))
    postalCountingCentresDatasetId = db.Column(db.Integer, db.ForeignKey(File.Model.__table__.c.fileId))
    partyCandidateDatasetId = db.Column(db.Integer, db.ForeignKey(File.Model.__table__.c.fileId))
    invalidVoteCategoriesDatasetId = db.Column(db.Integer, db.ForeignKey(File.Model.__table__.c.fileId))

    pollingStationsDataset = relationship(File.Model, foreign_keys=[pollingStationsDatasetId])
    postalCountingCentresDataset = relationship(File.Model, foreign_keys=[postalCountingCentresDatasetId])
    partyCandidateDataset = relationship(File.Model, foreign_keys=[partyCandidateDatasetId])
    invalidVoteCategoriesDataset = relationship(File.Model, foreign_keys=[invalidVoteCategoriesDatasetId])

    def __init__(self, electionName, parentElectionId, voteType, isListed):
        super(ElectionModel, self).__init__(
            electionName=electionName,
            parentElectionId=parentElectionId,
            voteType=voteType,
            isListed=isListed
        )

        if parentElectionId is not None:
            parentElection = get_by_id(parentElectionId)
            self.rootElectionId = parentElection.rootElectionId
        else:
            self.rootElectionId = self.electionId

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

    def add_sub_election(self, electionName, voteType, isListed=False):
        return create(
            electionName=electionName,
            parentElectionId=self.electionId,
            voteType=voteType,
            isListed=isListed
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
        return self.rootElection

    def get_official_name(self):
        if self.parentElectionId is None:
            return self.electionName
        else:
            return self.parentElection.get_official_name()


Model = ElectionModel


def create(electionName, parentElectionId=None,
           voteType=VoteTypeEnum.PostalAndNonPostal, isListed=False):
    election = Model(
        electionName=electionName,
        parentElectionId=parentElectionId,
        voteType=voteType,
        isListed=isListed
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
        Model.isListed == True
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
