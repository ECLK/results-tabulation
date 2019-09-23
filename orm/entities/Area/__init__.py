from sqlalchemy.ext.associationproxy import association_proxy

from app import db
from sqlalchemy.orm import relationship, aliased
from sqlalchemy import and_, func, or_

from orm.enums import AreaTypeEnum, AreaCategoryEnum
from orm.entities import Election
from sqlalchemy.ext.hybrid import hybrid_property
from util import get_paginated_query, get_array, get_area_type


class AreaModel(db.Model):
    __tablename__ = 'area'
    areaId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    areaName = db.Column(db.String(100), nullable=False)
    areaType = db.Column(db.Enum(AreaTypeEnum), nullable=False)
    electionId = db.Column(db.Integer, db.ForeignKey(Election.Model.__table__.c.electionId), nullable=False)
    # parentAreaId = db.Column(db.Integer, db.ForeignKey(areaId), nullable=True)

    _registeredVotersCount = db.Column(db.Integer(), nullable=True)

    election = relationship(Election.Model, foreign_keys=[electionId])
    # parentArea = relationship("AreaModel", remote_side=[areaId])
    # childAreas = relationship("AreaModel", foreign_keys=[parentAreaId])
    # pollingStations = relationship("PollingStationModel")

    # this relationship is used for persistence
    children = relationship("AreaModel", secondary="area_area",
                            primaryjoin="AreaModel.areaId==AreaAreaModel.parentAreaId",
                            secondaryjoin="AreaModel.areaId==AreaAreaModel.childAreaId"
                            )
    parents = relationship("AreaModel", secondary="area_area",
                           primaryjoin="AreaModel.areaId==AreaAreaModel.childAreaId",
                           secondaryjoin="AreaModel.areaId==AreaAreaModel.parentAreaId"
                           )

    tallySheets = relationship("TallySheetModel", secondary="submission",
                               primaryjoin="AreaModel.areaId==SubmissionModel.areaId",
                               secondaryjoin="SubmissionModel.submissionId==TallySheetModel.tallySheetId"
                               )

    tallySheets_PRE_41 = relationship(
        "TallySheetModel", secondary="submission",
        primaryjoin="AreaModel.areaId==SubmissionModel.areaId",
        secondaryjoin="and_(SubmissionModel.submissionId==TallySheetModel.tallySheetId, TallySheetModel.tallySheetCode=='PRE_41')"
    )

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

    def get_associated_areas(self, areaType, electionId=None):
        return get_associated_areas(self, areaType, electionId)

    def get_submissions(self, submissionType):
        return [submission for submission in self.submissions if submission.submissionType is submissionType]

    # def get_reports(self, reportCode):
    #     return [report for report in self.reports if report.reportCode is reportCode]

    @hybrid_property
    def pollingStations(self):
        return get_associated_areas(self, AreaTypeEnum.PollingStation)

    @hybrid_property
    def countingCentres(self):
        # return []
        return get_associated_areas(self, AreaTypeEnum.CountingCentre)

    @hybrid_property
    def districtCentres(self):
        # return []
        return get_associated_areas(self, AreaTypeEnum.DistrictCentre)

    @hybrid_property
    def registeredVotersCount(self):
        polling_stations_subquery = get_associated_areas_query(self, areaType=AreaTypeEnum.PollingStation).subquery()

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
    election_commission_mapping = aliased(AreaAreaModel)
    district_centre_mapping = aliased(AreaAreaModel)
    counting_centre_mapping = aliased(AreaAreaModel)
    postal_vote_counting_centre_mapping = aliased(AreaAreaModel)
    polling_station_mapping = aliased(AreaAreaModel)
    polling_district_mapping = aliased(AreaAreaModel)
    polling_division_mapping = aliased(AreaAreaModel)
    electoral_district_mapping = aliased(AreaAreaModel)
    country_mapping = aliased(AreaAreaModel)

    election_commission = aliased(AreaModel)
    district_centre = aliased(AreaModel)
    counting_centre = aliased(AreaModel)
    polling_station = aliased(AreaModel)
    polling_district = aliased(AreaModel)
    polling_division = aliased(AreaModel)
    electoral_district = aliased(AreaModel)
    country = aliased(AreaModel)

    presidential_area_map_query = db.session.query(
        counting_centre.areaId.label("countingCentreId"),
        polling_station.areaId.label("pollingStationId"),
        district_centre.areaId.label("districtCentreId"),
        election_commission.areaId.label("electionCommissionId"),
        polling_district.areaId.label("pollingDistrictId"),
        polling_division.areaId.label("pollingDivisionId"),
        electoral_district.areaId.label("electoralDistrictId"),
        country.areaId.label("countryId")
    ).join(
        polling_station_mapping,
        polling_station_mapping.parentAreaId == counting_centre.areaId,
        isouter=True
    ).join(
        polling_station,
        and_(
            polling_station.areaId == polling_station_mapping.childAreaId,
            polling_station.areaType == AreaTypeEnum.PollingStation
        ),
        isouter=True
    ).join(
        district_centre_mapping,
        district_centre_mapping.childAreaId == counting_centre.areaId,
        isouter=True
    ).join(
        district_centre,
        and_(
            district_centre.areaId == district_centre_mapping.parentAreaId,
            district_centre.areaType == AreaTypeEnum.DistrictCentre
        ),
        isouter=True
    ).join(
        election_commission_mapping,
        election_commission_mapping.childAreaId == district_centre.areaId,
        isouter=True
    ).join(
        election_commission,
        and_(
            election_commission.areaId == election_commission_mapping.parentAreaId,
            election_commission.areaType == AreaTypeEnum.ElectionCommission
        ),
        isouter=True
    ).join(
        polling_district_mapping,
        polling_district_mapping.childAreaId == polling_station.areaId,
        isouter=True
    ).join(
        polling_district,
        and_(
            polling_district.areaId == polling_district_mapping.parentAreaId,
            polling_district.areaType == AreaTypeEnum.PollingDistrict
        ),
        isouter=True
    ).join(
        postal_vote_counting_centre_mapping,
        postal_vote_counting_centre_mapping.childAreaId == counting_centre.areaId,
        isouter=True
    ).join(
        polling_division_mapping,
        polling_division_mapping.childAreaId == polling_district.areaId,
        isouter=True
    ).join(
        polling_division,
        or_(
            and_(
                polling_division.areaId == polling_division_mapping.parentAreaId,
                polling_division.areaType == AreaTypeEnum.PollingDivision
            ),
            and_(
                polling_division.areaId == postal_vote_counting_centre_mapping.parentAreaId,
                polling_division.areaType == AreaTypeEnum.PollingDivision
            ),
        ),
        isouter=True
    ).join(
        electoral_district_mapping,
        electoral_district_mapping.childAreaId == polling_division.areaId,
        isouter=True
    ).join(
        electoral_district,
        and_(
            electoral_district.areaId == electoral_district_mapping.parentAreaId,
            electoral_district.areaType == AreaTypeEnum.ElectoralDistrict
        ),
        isouter=True
    ).join(
        country_mapping,
        country_mapping.childAreaId == electoral_district.areaId,
        isouter=True
    ).join(
        country,
        and_(
            country.areaId == country_mapping.parentAreaId,
            country.areaType == AreaTypeEnum.Country
        ),
        isouter=True
    )

    return presidential_area_map_query


def get_associated_areas_query(area, areaType, electionId=None):
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

    if area.areaType is AreaTypeEnum.PollingStation:
        query = query.filter(
            presidential_area_map_sub_query.c.pollingStationId == area.areaId
        )
    elif area.areaType is AreaTypeEnum.CountingCentre:
        query = query.filter(
            presidential_area_map_sub_query.c.countingCentreId == area.areaId
        )
    elif area.areaType is AreaTypeEnum.DistrictCentre:
        query = query.filter(
            presidential_area_map_sub_query.c.districtCentreId == area.areaId
        )
    elif area.areaType is AreaTypeEnum.ElectionCommission:
        query = query.filter(
            presidential_area_map_sub_query.c.electionCommissionId == area.areaId
        )
    elif area.areaType is AreaTypeEnum.PollingDistrict:
        query = query.filter(
            presidential_area_map_sub_query.c.pollingDistrictId == area.areaId
        )
    elif area.areaType is AreaTypeEnum.PollingDivision:
        query = query.filter(
            presidential_area_map_sub_query.c.pollingDivisionId == area.areaId
        )
    elif area.areaType is AreaTypeEnum.ElectoralDistrict:
        query = query.filter(
            presidential_area_map_sub_query.c.electoralDistrictId == area.areaId
        )
    elif area.areaType is AreaTypeEnum.Country:
        query = query.filter(
            presidential_area_map_sub_query.c.countryId == area.areaId
        )
    elif area.areaType is AreaTypeEnum.PostalVoteCountingCentre:
        query = query.filter(
            presidential_area_map_sub_query.c.postalVoteCountingCentreId == area.areaId
        )

    if electionId is not None:
        query = query.filter(
            AreaModel.electionId.in_(election.mappedElectionIds)
        )

    return query


def get_associated_areas(area, areaType, electionId=None):
    result = get_associated_areas_query(area=area, areaType=areaType, electionId=electionId).all()

    return result


def create(areaName, electionId):
    area = Model(
        areaName=areaName,
        electionId=electionId
    )

    return area


def get_all(election_id=None, area_name=None, associated_area_id=None, area_type=None):
    if associated_area_id is not None and area_type is not None:
        associated_area = get_by_id(areaId=associated_area_id)
        query = get_associated_areas_query(area=associated_area, areaType=area_type, electionId=election_id)
    else:
        query = Model.query

    if area_name is not None:
        query = query.filter(Model.areaName.like(area_name))

    # if election_id is not None:
    #     query = query.filter(
    #         or_(
    #             Election.Model.electionId == election_id,
    #             Election.Model.parentElectionId == election_id
    #         )
    #     )

    if area_type is not None:
        query = query.filter(Model.areaType == area_type)

    query = query.order_by(Model.areaId)

    result = get_paginated_query(query).all()

    return result


def get_by_id(areaId):
    result = Model.query.filter(
        Model.areaId == areaId
    ).one_or_none()

    return result
