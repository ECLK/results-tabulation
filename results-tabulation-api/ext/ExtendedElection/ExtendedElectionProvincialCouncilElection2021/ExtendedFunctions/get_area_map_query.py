from app import db
from sqlalchemy import bindparam
from sqlalchemy.orm import aliased
from constants.VOTE_TYPES import NonPostal


def get_area_map_query(election):
    from orm.entities import Election, Area
    from orm.entities.Area import AreaAreaModel
    from orm.enums import AreaTypeEnum

    country = db.session.query(Area.Model).filter(
        Area.Model.areaType == AreaTypeEnum.Country).subquery()
    administrative_district = db.session.query(Area.Model).filter(
        Area.Model.areaType == AreaTypeEnum.AdministrativeDistrict).subquery()
    province = db.session.query(Area.Model).filter(
        Area.Model.areaType == AreaTypeEnum.Province).subquery()
    polling_division = db.session.query(Area.Model).filter(
        Area.Model.areaType == AreaTypeEnum.PollingDivision).subquery()
    polling_district = db.session.query(Area.Model).filter(
        Area.Model.areaType == AreaTypeEnum.PollingDistrict).subquery()
    polling_station = db.session.query(Area.Model).filter(
        Area.Model.areaType == AreaTypeEnum.PollingStation).subquery()
    counting_centre = db.session.query(Area.Model).filter(
        Area.Model.areaType == AreaTypeEnum.CountingCentre).subquery()
    district_centre = db.session.query(Area.Model).filter(
        Area.Model.areaType == AreaTypeEnum.DistrictCentre).subquery()
    election_commission = db.session.query(Area.Model).filter(
        Area.Model.areaType == AreaTypeEnum.ElectionCommission).subquery()

    country__province = aliased(AreaAreaModel)
    province__administrative_district = aliased(AreaAreaModel)
    administrative_district__polling_division = aliased(AreaAreaModel)
    polling_division__polling_district = aliased(AreaAreaModel)
    polling_district__polling_station = aliased(AreaAreaModel)
    counting_centre__polling_station = aliased(AreaAreaModel)
    district_centre__counting_centre = aliased(AreaAreaModel)
    election_commission__district_centre = aliased(AreaAreaModel)

    # For postal vote counting centres.
    administrative_district__counting_centre = aliased(AreaAreaModel)

    query_args = [
        country.c.areaId.label("countryId"),
        country.c.areaName.label("countryName"),
        province.c.areaId.label("provinceId"),
        province.c.areaName.label("provinceName"),
        administrative_district.c.areaId.label("administrativeDistrictId"),
        administrative_district.c.areaName.label("administrativeDistrictName"),
        bindparam("electoralDistrictId", None),
        bindparam("electoralDistrictName", None),
        counting_centre.c.areaId.label("countingCentreId"),
        counting_centre.c.areaName.label("countingCentreName"),
        Election.Model.voteType,
        Election.Model.electionId
    ]

    query_filter = [
        country__province.parentAreaId == country.c.areaId,
        country__province.childAreaId == province.c.areaId,

        province__administrative_district.parentAreaId == province.c.areaId,
        province__administrative_district.childAreaId == administrative_district.c.areaId,

        district_centre__counting_centre.parentAreaId == district_centre.c.areaId,
        district_centre__counting_centre.childAreaId == counting_centre.c.areaId,

        election_commission__district_centre.parentAreaId == election_commission.c.areaId,
        election_commission__district_centre.childAreaId == district_centre.c.areaId,

        Election.Model.electionId == counting_centre.c.electionId
    ]

    if election.election.voteType != NonPostal:
        query_args += [
            bindparam("pollingDivisionId", None),
            bindparam("pollingDivisionName", None),
            bindparam("pollingDistrictId", None),
            bindparam("pollingDistrictName", None),
            bindparam("pollingStationId", None),
            bindparam("pollingStationName", None)
        ]
        query_filter += [
            administrative_district__counting_centre.parentAreaId == administrative_district.c.areaId,
            administrative_district__counting_centre.childAreaId == counting_centre.c.areaId
        ]
    else:
        query_args += [
            polling_division.c.areaId.label("pollingDivisionId"),
            polling_division.c.areaName.label("pollingDivisionName"),
            polling_district.c.areaId.label("pollingDistrictId"),
            polling_district.c.areaName.label("pollingDistrictName"),
            polling_station.c.areaId.label("pollingStationId"),
            polling_station.c.areaName.label("pollingStationName")
        ]
        query_filter += [
            administrative_district__polling_division.parentAreaId == administrative_district.c.areaId,
            administrative_district__polling_division.childAreaId == polling_division.c.areaId,

            polling_division__polling_district.parentAreaId == polling_division.c.areaId,
            polling_division__polling_district.childAreaId == polling_district.c.areaId,

            polling_district__polling_station.parentAreaId == polling_district.c.areaId,
            polling_district__polling_station.childAreaId == polling_station.c.areaId,

            counting_centre__polling_station.parentAreaId == counting_centre.c.areaId,
            counting_centre__polling_station.childAreaId == polling_station.c.areaId
        ]

    query = db.session.query(*query_args).filter(*query_filter)

    return query
