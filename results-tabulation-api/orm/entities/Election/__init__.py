from typing import Set

from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from app import db
from auth import get_user_access_area_ids
from ext.ExtendedElection import get_extended_election
from orm.entities import Meta
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
    metaId = db.Column(db.Integer, db.ForeignKey(Meta.Model.__table__.c.metaId), nullable=True)

    parties = relationship("ElectionPartyModel", order_by="ElectionPartyModel.electionPartyId", lazy='subquery')
    _invalidVoteCategories = relationship("InvalidVoteCategoryModel", lazy='subquery')
    subElections = relationship("ElectionModel", foreign_keys=[parentElectionId], lazy='subquery')
    rootElection = relationship("ElectionModel", remote_side=[electionId], foreign_keys=[rootElectionId],
                                lazy='subquery')
    parentElection = relationship("ElectionModel", remote_side=[electionId], foreign_keys=[parentElectionId],
                                  lazy='subquery')
    meta = relationship(Meta.Model, foreign_keys=[metaId], lazy='subquery')

    pollingStationsDatasetId = db.Column(db.Integer, db.ForeignKey(File.Model.__table__.c.fileId))
    postalCountingCentresDatasetId = db.Column(db.Integer, db.ForeignKey(File.Model.__table__.c.fileId))
    partyCandidateDatasetId = db.Column(db.Integer, db.ForeignKey(File.Model.__table__.c.fileId))
    invalidVoteCategoriesDatasetId = db.Column(db.Integer, db.ForeignKey(File.Model.__table__.c.fileId))
    numberOfSeatsDatasetId = db.Column(db.Integer, db.ForeignKey(File.Model.__table__.c.fileId))

    pollingStationsDataset = relationship(File.Model, foreign_keys=[pollingStationsDatasetId])
    postalCountingCentresDataset = relationship(File.Model, foreign_keys=[postalCountingCentresDatasetId])
    partyCandidateDataset = relationship(File.Model, foreign_keys=[partyCandidateDatasetId])
    invalidVoteCategoriesDataset = relationship(File.Model, foreign_keys=[invalidVoteCategoriesDatasetId])
    numberOfSeatsDataset = relationship(File.Model, foreign_keys=[numberOfSeatsDatasetId])

    metaDataList = association_proxy("meta", "metaDataList")

    def __init__(self, electionTemplateName, electionName, parentElection, voteType, isListed,
                 party_candidate_dataset_file=None,
                 polling_station_dataset_file=None, postal_counting_centers_dataset_file=None,
                 invalid_vote_categories_dataset_file=None,
                 number_of_seats_dataset_file=None):
        super(ElectionModel, self).__init__(
            electionTemplateName=electionTemplateName,
            electionName=electionName,
            voteType=voteType,
            isListed=isListed,
            metaId=Meta.create().metaId
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
            self.set_number_of_seats_dataset(fileSource=number_of_seats_dataset_file)

            extended_election = self.get_extended_election()

            if extended_election is not None:
                extended_election.build_election()

    def get_extended_election(self):
        extended_election = get_extended_election(election=self)
        return extended_election

    def get_this_and_above_election_ids(self):
        if self.parentElectionId is None:
            return [self.electionId]
        else:
            return [self.electionId] + self.parentElection.get_this_and_above_election_ids()

    def get_this_and_below_election_ids(self):
        _this_and_below_election_ids = [self.electionId]
        for subElection in self.subElections:
            _this_and_below_election_ids += subElection.get_this_and_below_election_ids()

        return _this_and_below_election_ids

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

    def add_invalid_vote_category(self, categoryDescription, invalidVoteCategoryType=None):
        invalid_vote_category = db.session.query(InvalidVoteCategory.Model).filter(
            InvalidVoteCategory.Model.electionId == self.electionId,
            InvalidVoteCategory.Model.categoryDescription == categoryDescription
        ).one_or_none()

        if invalid_vote_category is None:
            invalid_vote_category = InvalidVoteCategory.create(
                electionId=self.electionId,
                categoryDescription=categoryDescription,
                invalidVoteCategoryType=invalidVoteCategoryType
            )

        return invalid_vote_category

    def add_party(self, partyId):
        election_party = db.session.query(ElectionParty.Model).filter(
            ElectionParty.Model.partyId == partyId,
            ElectionParty.Model.electionId == self.electionId
        ).one_or_none()

        if election_party is None:
            election_party = ElectionParty.create(
                electionId=self.electionId,
                partyId=partyId
            )

        return election_party

    def add_candidate(self, partyId, candidateId):

        election_candidate = db.session.query(ElectionCandidate.Model).filter(
            ElectionCandidate.Model.partyId == partyId,
            ElectionCandidate.Model.candidateId == candidateId,
            ElectionCandidate.Model.electionId == self.electionId
        ).one_or_none()

        if election_candidate is None:
            election_candidate = ElectionCandidate.create(
                electionId=self.electionId,
                partyId=partyId,
                candidateId=candidateId
            )

        return election_candidate

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

    def set_number_of_seats_dataset(self, fileSource):
        dataset = File.createFromFileSource(fileSource=fileSource)
        self.numberOfSeatsDatasetId = dataset.fileId

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
           invalid_vote_categories_dataset_file=None,
           number_of_seats_dataset_file=None):
    election = Model(
        electionTemplateName=electionTemplateName,
        electionName=electionName,
        parentElection=parentElection,
        voteType=voteType,
        isListed=isListed,
        party_candidate_dataset_file=party_candidate_dataset_file,
        polling_station_dataset_file=polling_station_dataset_file,
        postal_counting_centers_dataset_file=postal_counting_centers_dataset_file,
        invalid_vote_categories_dataset_file=invalid_vote_categories_dataset_file,
        number_of_seats_dataset_file=number_of_seats_dataset_file
    )

    return election


def get_authorized_election_ids():
    from orm.entities import Area

    user_access_area_ids: Set[int] = get_user_access_area_ids()

    authorized_elections = db.session.query(
        ElectionModel
    ).filter(
        ElectionModel.electionId == Area.Model.electionId,
        Area.Model.areaId.in_(user_access_area_ids)
    ).group_by(
        ElectionModel.electionId
    ).all()

    authorized_election_ids = []
    for authorized_election in authorized_elections:
        authorized_election_ids.extend(authorized_election.get_this_and_above_election_ids())
        authorized_election_ids.extend(authorized_election.get_this_and_below_election_ids())

    return authorized_election_ids


def get_all(parentElectionId=None, rootElectionId=None, isListed=True):
    authorized_election_ids = get_authorized_election_ids()

    query_args = [ElectionModel]
    query_filters = [Model.electionId.in_(authorized_election_ids)]

    query_filters.append(ElectionModel.parentElectionId == parentElectionId)

    if rootElectionId is not None:
        query_filters.append(ElectionModel.rootElectionId == rootElectionId)

    if isListed is not None:
        query_filters.append(ElectionModel.isListed == isListed)

    return db.session.query(*query_args).filter(*query_filters)


def get_by_id(electionId):
    authorized_election_ids = get_authorized_election_ids()

    result = Model.query.filter(
        Model.electionId == electionId,
        Model.electionId.in_(authorized_election_ids)
    ).one_or_none()

    return result
