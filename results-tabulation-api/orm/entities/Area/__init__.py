from app import db
from sqlalchemy.orm import relationship
from sqlalchemy import func
from sqlalchemy.sql.functions import coalesce

from constants.VOTE_TYPES import NonPostal, Postal, Quarantine
from orm.entities.Area import AreaMap
from orm.enums import AreaTypeEnum
from orm.entities import Election
from sqlalchemy.ext.hybrid import hybrid_property


class AreaModel(db.Model):
    __tablename__ = 'area'
    areaId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    areaName = db.Column(db.String(800), nullable=False)
    areaType = db.Column(db.Enum(AreaTypeEnum), nullable=False)
    electionId = db.Column(db.Integer, db.ForeignKey(Election.Model.__table__.c.electionId), nullable=False)

    _registeredVotersCount = db.Column(db.Integer(), nullable=True)
    _registeredPostalVotersCount = db.Column(db.Integer(), nullable=True)
    _registeredQuarantineVotersCount = db.Column(db.Integer(), nullable=True)
    _registeredDisplacedVotersCount = db.Column(db.Integer(), nullable=True)

    election = relationship(Election.Model, foreign_keys=[electionId])

    # this relationship is used for persistence
    children = relationship("AreaAreaModel", lazy="joined",
                            primaryjoin="AreaModel.areaId==AreaAreaModel.parentAreaId")
    parents = relationship("AreaAreaModel", lazy="joined",
                           primaryjoin="AreaModel.areaId==AreaAreaModel.childAreaId")

    def __init__(self, areaName, electionId):
        super(AreaModel, self).__init__(
            areaName=areaName,
            electionId=electionId
        )
        db.session.add(self)
        db.session.flush()

    def add_parent(self, parentId):
        parentArea = get_by_id(areaId=parentId)
        parentArea.add_child(self.areaId)

        return self

    def add_child(self, childId):
        existing_mapping = AreaAreaModel.query.filter(
            AreaAreaModel.parentAreaId == self.areaId,
            AreaAreaModel.childAreaId == childId
        ).one_or_none()

        if existing_mapping is None:
            areaParent = AreaAreaModel(parentAreaId=self.areaId, childAreaId=childId)
            db.session.add(areaParent)
            db.session.flush()

        return self

    def get_associated_areas_query(self, areaType, electionId=None):
        return get_associated_areas_query(areas=[self], areaType=areaType, electionId=electionId)

    def get_associated_areas(self, areaType, electionId=None):
        return self.get_associated_areas_query(areaType, electionId).all()

    def get_submissions(self, submissionType):
        return [submission for submission in self.submissions if submission.submissionType is submissionType]

    @hybrid_property
    def areaMapList(self):
        extended_election = self.election.get_extended_election()

        return extended_election.get_area_map(area=self)

    def get_registered_voters_count(self, vote_type=None):
        polling_stations_subquery = get_associated_areas_query(areas=[self],
                                                               areaType=AreaTypeEnum.PollingStation).subquery()

        _registeredVotersCount = db.Column(db.Integer(), nullable=True)
        _registeredPostalVotersCount = db.Column(db.Integer(), nullable=True)
        _registeredQuarantineVotersCount = db.Column(db.Integer(), nullable=True)
        _registeredDisplacedVotersCount = db.Column(db.Integer(), nullable=True)

        if vote_type == NonPostal:
            registered_voters_column = coalesce(polling_stations_subquery.c._registeredVotersCount, 0)
        elif vote_type == Postal:
            registered_voters_column = coalesce(polling_stations_subquery.c._registeredPostalVotersCount, 0)
        elif vote_type == Quarantine:
            registered_voters_column = coalesce(polling_stations_subquery.c._registeredQuarantineVotersCount, 0)
        elif vote_type == Quarantine:
            registered_voters_column = coalesce(polling_stations_subquery.c._registeredDisplacedVotersCount, 0)
        else:
            registered_voters_column = coalesce(polling_stations_subquery.c._registeredVotersCount, 0) \
                                       + coalesce(polling_stations_subquery.c._registeredPostalVotersCount, 0) \
                                       + coalesce(polling_stations_subquery.c._registeredQuarantineVotersCount, 0) \
                                       + coalesce(polling_stations_subquery.c._registeredDisplacedVotersCount, 0)

        total_registered_voters_count = db.session.query(func.sum(registered_voters_column)).scalar()

        return float(total_registered_voters_count)

    @hybrid_property
    def registeredVotersCount(self):
        polling_stations_subquery = get_associated_areas_query(areas=[self],
                                                               areaType=AreaTypeEnum.PollingStation).subquery()

        total_registered_voters_count = db.session.query(
            func.sum(polling_stations_subquery.c._registeredVotersCount)
        ).scalar()

        return total_registered_voters_count

    @hybrid_property
    def registeredPostalVotersCount(self):
        polling_stations_subquery = get_associated_areas_query(areas=[self],
                                                               areaType=AreaTypeEnum.PollingStation).subquery()

        total_registered_postal_voters_count = db.session.query(
            func.sum(polling_stations_subquery.c._registeredPostalVotersCount)
        ).scalar()

        return total_registered_postal_voters_count

    __mapper_args__ = {
        'polymorphic_on': areaType
    }


class AreaAreaModel(db.Model):
    __tablename__ = 'area_area'
    parentAreaId = db.Column(db.Integer, db.ForeignKey("area.areaId"), primary_key=True)
    childAreaId = db.Column(db.Integer, db.ForeignKey("area.areaId"), primary_key=True)


Model = AreaModel


def get_presidential_area_map_query():
    return db.session.query(
        AreaMap.Model
    )


def get_associated_areas_query(areas, areaType, electionId=None):
    presidential_area_map_sub_query = get_presidential_area_map_query().subquery()

    area_types = [AreaTypeEnum.Country, AreaTypeEnum.ElectoralDistrict, AreaTypeEnum.PollingDivision,
                  AreaTypeEnum.PollingDistrict, AreaTypeEnum.PollingStation, AreaTypeEnum.CountingCentre,
                  AreaTypeEnum.DistrictCentre, AreaTypeEnum.ElectionCommission]

    area_type_to_column_map = {
        AreaTypeEnum.Country: presidential_area_map_sub_query.c.countryId,
        AreaTypeEnum.ElectoralDistrict: presidential_area_map_sub_query.c.electoralDistrictId,
        AreaTypeEnum.PollingDivision: presidential_area_map_sub_query.c.pollingDivisionId,
        AreaTypeEnum.PollingDistrict: presidential_area_map_sub_query.c.pollingDistrictId,
        AreaTypeEnum.PollingStation: presidential_area_map_sub_query.c.pollingStationId,
        AreaTypeEnum.CountingCentre: presidential_area_map_sub_query.c.countingCentreId,
        AreaTypeEnum.DistrictCentre: presidential_area_map_sub_query.c.districtCentreId,
        AreaTypeEnum.ElectionCommission: presidential_area_map_sub_query.c.electionCommissionId
    }

    area_type_to_query_area_ids = {}

    for area in areas:
        if area.areaType not in area_type_to_query_area_ids:
            area_type_to_query_area_ids[area.areaType] = []

        area_type_to_query_area_ids[area.areaType].append(area.areaId)

    query_args = [AreaModel]
    query_filters = [
        area_type_to_column_map[areaType] == AreaModel.areaId
    ]
    query_group_by = [AreaModel.areaId]

    if electionId is not None:
        election = db.session.query(Election.Model).filter(Election.Model.electionId == electionId).one_or_none()
        election_ids = election.get_this_and_above_election_ids() + election.get_this_and_below_election_ids()
        query_filters.append(AreaModel.electionId.in_(election_ids))

    for area_type in area_types:
        if area_type in area_type_to_query_area_ids:
            query_filters.append(area_type_to_column_map[area_type].in_(area_type_to_query_area_ids[area_type]))

    return db.session.query(*query_args).filter(*query_filters).group_by(*query_group_by)


def get_associated_areas(area, areaType, electionId=None):
    result = get_associated_areas_query(areas=[area], areaType=areaType, electionId=electionId).all()

    return result


def create(areaName, electionId):
    area = Model(
        areaName=areaName,
        electionId=electionId
    )

    return area


def get_all(election_id=None, area_name=None, associated_area_id=None, area_type=None):
    election = Election.Model.query.filter(Election.Model.electionId == election_id).one_or_none()

    if associated_area_id is not None and area_type is not None:
        associated_area = get_by_id(areaId=associated_area_id)
        query = get_associated_areas_query(areas=[associated_area], areaType=area_type, electionId=election_id)
    else:
        query = Model.query

    if area_name is not None:
        query = query.filter(Model.areaName.like(area_name))

    if election is not None:
        query = query.filter(
            Model.electionId == election_id
        )

    if area_type is not None:
        query = query.filter(Model.areaType == area_type)

    query = query.order_by(Model.areaId)

    return query


def get_by_id(areaId):
    result = Model.query.filter(
        Model.areaId == areaId
    ).one_or_none()

    return result
