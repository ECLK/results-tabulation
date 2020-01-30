from typing import Set

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, aliased

from app import db
from auth import get_user_access_area_ids
from ext.Election import get_extended_election_class
from orm.entities.Election import ElectionParty, ElectionCandidate, InvalidVoteCategory
from orm.entities.IO import File


class ElectionModel(db.Model):
    __tablename__ = 'election'
    electionId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    electionName = db.Column(db.String(100), nullable=False)
    rootElectionId = db.Column(db.Integer, db.ForeignKey("election.electionId", name="fk_election_root_election_id"),
                               nullable=True)
    parentElectionId = db.Column(db.Integer, db.ForeignKey("election.electionId"), nullable=True)
    voteType = db.Column(db.String(100), nullable=False)
    electionTemplateName = db.Column(db.String(100), nullable=False)
    isListed = db.Column(db.Boolean, nullable=False, default=False)

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

    def __init__(self, electionTemplateName, electionName, parentElection, voteType, isListed,
                 party_candidate_dataset_file=None,
                 polling_station_dataset_file=None, postal_counting_centers_dataset_file=None,
                 invalid_vote_categories_dataset_file=None):
        super(ElectionModel, self).__init__(
            electionTemplateName=electionTemplateName,
            electionName=electionName,
            voteType=voteType,
            isListed=isListed
        )

        db.session.add(self)
        db.session.flush()

        if parentElection is not None:
            self.parentElectionId = parentElection.electionId
            self.rootElectionId = parentElection.rootElectionId
        else:
            self.parentElectionId = None
            self.rootElectionId = self.electionId

        db.session.flush()

        if self.electionId == self.rootElectionId:
            self.set_polling_stations_dataset(fileSource=polling_station_dataset_file)
            self.set_postal_counting_centres_dataset(fileSource=postal_counting_centers_dataset_file)
            self.set_party_candidates_dataset(fileSource=party_candidate_dataset_file)
            self.set_invalid_vote_categories_dataset(fileSource=invalid_vote_categories_dataset_file)

            extended_election_class = get_extended_election_class(electionTemplateName=self.electionTemplateName)

            if extended_election_class is not None:
                extended_election_class.build_election(root_election=self)

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
            electionTemplateName=self.electionTemplateName,
            electionName=electionName,
            parentElection=self,
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

PostalAndNonPostal = "PostalAndNonPostal"


def create(electionTemplateName, electionName, parentElection=None, voteType=PostalAndNonPostal, isListed=False,
           party_candidate_dataset_file=None,
           polling_station_dataset_file=None, postal_counting_centers_dataset_file=None,
           invalid_vote_categories_dataset_file=None):
    election = Model(
        electionTemplateName=electionTemplateName,
        electionName=electionName,
        parentElection=parentElection,
        voteType=voteType,
        isListed=isListed,
        party_candidate_dataset_file=party_candidate_dataset_file,
        polling_station_dataset_file=polling_station_dataset_file,
        postal_counting_centers_dataset_file=postal_counting_centers_dataset_file,
        invalid_vote_categories_dataset_file=invalid_vote_categories_dataset_file
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
