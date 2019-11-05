from app import db
from sqlalchemy.orm import relationship, aliased, backref
from sqlalchemy import and_, func, or_

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
    # parentAreaId = db.Column(db.Integer, db.ForeignKey(areaId), nullable=True)

    _registeredVotersCount = db.Column(db.Integer(), nullable=True)

    election = relationship(Election.Model, foreign_keys=[electionId])
    # parentArea = relationship("AreaModel", remote_side=[areaId])
    # childAreas = relationship("AreaModel", foreign_keys=[parentAreaId])
    # pollingStations = relationship("PollingStationModel")

    # this relationship is used for persistence
    children = relationship("AreaAreaModel", lazy="joined",
                            primaryjoin="AreaModel.areaId==AreaAreaModel.parentAreaId")

    # children = relationship("AreaModel", secondary="area_area", lazy="subquery",
    #                         primaryjoin="AreaModel.areaId==AreaAreaModel.parentAreaId",
    #                         secondaryjoin="AreaModel.areaId==AreaAreaModel.childAreaId"
    #                         )
    # parents = relationship("AreaModel", secondary="area_area", lazy="joined",
    #                        primaryjoin="AreaModel.areaId==AreaAreaModel.childAreaId",
    #                        secondaryjoin="AreaModel.areaId==AreaAreaModel.parentAreaId"
    #                        )
    #
    # tallySheets = relationship("TallySheetModel", secondary="submission", lazy="joined",
    #                            primaryjoin="AreaModel.areaId==SubmissionModel.areaId",
    #                            secondaryjoin="SubmissionModel.submissionId==TallySheetModel.tallySheetId"
    #                            )
    #
    # tallySheets_PRE_41 = relationship(
    #     "TallySheetModel", secondary="submission",
    #     primaryjoin="AreaModel.areaId==SubmissionModel.areaId",
    #     secondaryjoin="and_(SubmissionModel.submissionId==TallySheetModel.tallySheetId, TallySheetModel.tallySheetCode=='PRE_41')"
    # )

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

    # def get_reports(self, reportCode):
    #     return [report for report in self.reports if report.reportCode is reportCode]

    @hybrid_property
    def pollingStations(self):
        return get_associated_areas(self, AreaTypeEnum.PollingStation)

    @hybrid_property
    def countingCentres(self):
        return get_associated_areas(self, AreaTypeEnum.CountingCentre)

    @hybrid_property
    def districtCentres(self):
        return get_associated_areas(self, AreaTypeEnum.DistrictCentre)

    @hybrid_property
    def electoralDistricts(self):
        return get_associated_areas(self, AreaTypeEnum.ElectoralDistrict)

    @hybrid_property
    def pollingDivisions(self):
        return get_associated_areas(self, AreaTypeEnum.PollingDivision)

    @hybrid_property
    def pollingDistricts(self):
        # TODO review
        # Sending the list of polling districts only for polling stations.
        if self.areaType is AreaTypeEnum.PollingStation:
            return get_associated_areas(self, AreaTypeEnum.PollingDistrict)
        else:
            return []

    @hybrid_property
    def registeredVotersCount(self):
        polling_stations_subquery = get_associated_areas_query(areas=[self],
                                                               areaType=AreaTypeEnum.PollingStation).subquery()

        total_registered_voters_count = db.session.query(
            func.sum(polling_stations_subquery.c._registeredVotersCount)
        ).scalar()

        return total_registered_voters_count

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
    election = Election.get_by_id(electionId=electionId)

    query = db.session.query(
        AreaModel
    ).join(
        Election.Model,
        Election.Model.electionId == AreaModel.electionId
    )

    if areaType is AreaTypeEnum.PollingStation:
        query = query.join(
            presidential_area_map_sub_query,
            presidential_area_map_sub_query.c.pollingStationId == AreaModel.areaId
        )
    elif areaType is AreaTypeEnum.CountingCentre:
        query = query.join(
            presidential_area_map_sub_query,
            presidential_area_map_sub_query.c.countingCentreId == AreaModel.areaId
        )
    elif areaType is AreaTypeEnum.DistrictCentre:
        query = query.join(
            presidential_area_map_sub_query,
            presidential_area_map_sub_query.c.districtCentreId == AreaModel.areaId
        )
    elif areaType is AreaTypeEnum.ElectionCommission:
        query = query.join(
            presidential_area_map_sub_query,
            presidential_area_map_sub_query.c.electionCommissionId == AreaModel.areaId
        )
    elif areaType is AreaTypeEnum.PollingDistrict:
        query = query.join(
            presidential_area_map_sub_query,
            presidential_area_map_sub_query.c.pollingDistrictId == AreaModel.areaId
        )
    elif areaType is AreaTypeEnum.PollingDivision:
        query = query.join(
            presidential_area_map_sub_query,
            presidential_area_map_sub_query.c.pollingDivisionId == AreaModel.areaId
        )
    elif areaType is AreaTypeEnum.ElectoralDistrict:
        query = query.join(
            presidential_area_map_sub_query,
            presidential_area_map_sub_query.c.electoralDistrictId == AreaModel.areaId
        )
    elif areaType is AreaTypeEnum.Country:
        query = query.join(
            presidential_area_map_sub_query,
            presidential_area_map_sub_query.c.countryId == AreaModel.areaId
        )
    elif areaType is AreaTypeEnum.PostalVoteCountingCentre:
        query = query.join(
            presidential_area_map_sub_query,
            presidential_area_map_sub_query.c.postalVoteCountingCentreId == AreaModel.areaId
        )

    query = query.group_by(AreaModel.areaId)

    filtered_polling_stations = [area.areaId for area in areas if area.areaType == AreaTypeEnum.PollingStation]
    filtered_counting_centres = [area.areaId for area in areas if area.areaType == AreaTypeEnum.CountingCentre]
    filtered_district_centres = [area.areaId for area in areas if area.areaType == AreaTypeEnum.DistrictCentre]
    filtered_election_commissions = [area.areaId for area in areas if area.areaType == AreaTypeEnum.ElectionCommission]
    filtered_polling_districts = [area.areaId for area in areas if area.areaType == AreaTypeEnum.PollingDistrict]
    filtered_polling_divisions = [area.areaId for area in areas if area.areaType == AreaTypeEnum.PollingDivision]
    filtered_electoral_districts = [area.areaId for area in areas if area.areaType == AreaTypeEnum.ElectoralDistrict]
    filtered_countries = [area.areaId for area in areas if area.areaType == AreaTypeEnum.Country]

    if len(filtered_polling_stations) > 0:
        query = query.filter(
            presidential_area_map_sub_query.c.pollingStationId.in_(filtered_polling_stations)
        )
    elif len(filtered_counting_centres) > 0:
        query = query.filter(
            presidential_area_map_sub_query.c.countingCentreId.in_(filtered_counting_centres)
        )
    elif len(filtered_district_centres) > 0:
        query = query.filter(
            presidential_area_map_sub_query.c.districtCentreId.in_(filtered_district_centres)
        )
    elif len(filtered_election_commissions) > 0:
        query = query.filter(
            presidential_area_map_sub_query.c.electionCommissionId.in_(filtered_election_commissions)
        )
    elif len(filtered_polling_districts) > 0:
        query = query.filter(
            presidential_area_map_sub_query.c.pollingDistrictId.in_(filtered_polling_districts)
        )
    elif len(filtered_polling_divisions) > 0:
        query = query.filter(
            presidential_area_map_sub_query.c.pollingDivisionId.in_(filtered_polling_divisions)
        )
    elif len(filtered_electoral_districts) > 0:
        query = query.filter(
            presidential_area_map_sub_query.c.electoralDistrictId.in_(filtered_electoral_districts)
        )
    elif len(filtered_countries) > 0:
        query = query.filter(
            presidential_area_map_sub_query.c.countryId.in_(filtered_countries)
        )

    if electionId is not None:
        query = query.filter(
            or_(
                Model.electionId.in_(election.mappedElectionIds),
                Model.electionId.in_(election.subElectionIds)
            )
        )

    query = query.filter(
        AreaModel.areaType == areaType
    )

    return query


def get_associated_areas(area, areaType, electionId=None):
    result = get_associated_areas_query(areas=[area], areaType=areaType, electionId=electionId).all()

    return result


def create(areaName, electionId):
    area = Model(
        areaName=areaName,
        electionId=electionId
    )

    return area


def get_all_areas_of_root_election(election_id):
    election = Election.get_by_id(electionId=election_id)

    if election.parentElectionId is not None:
        return get_all_areas_of_root_election(election.parentElectionI)
    else:
        return get_all(election_id=election_id)


def get_all(election_id=None, area_name=None, associated_area_id=None, area_type=None):
    election = Election.get_by_id(electionId=election_id)

    if associated_area_id is not None and area_type is not None:
        associated_area = get_by_id(areaId=associated_area_id)
        query = get_associated_areas_query(areas=[associated_area], areaType=area_type, electionId=election_id)
    else:
        query = Model.query

    if area_name is not None:
        query = query.filter(Model.areaName.like(area_name))

    if election is not None:
        query = query.filter(
            or_(
                Model.electionId.in_(election.mappedElectionIds),
                Model.electionId.in_(election.subElectionIds)
            )
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
