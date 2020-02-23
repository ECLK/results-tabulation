from sqlalchemy import bindparam
from sqlalchemy.orm import aliased
from app import db
from ext.ExtendedTallySheetVersion import ExtendedTallySheetVersion
from sqlalchemy import and_, func, or_


def get_extended_election(election):
    from constants.ELECTION_TEMPLATES import PRESIDENTIAL_ELECTION_2019, PARLIAMENT_ELECTION_2020
    from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020 import ExtendedElectionParliamentaryElection2020
    from ext.ExtendedElection.ExtendedElectionPresidentialElection2019 import ExtendedElectionPresidentialElection2019

    EXTENDED_ELECTION_MAP = {
        PRESIDENTIAL_ELECTION_2019: ExtendedElectionPresidentialElection2019,
        PARLIAMENT_ELECTION_2020: ExtendedElectionParliamentaryElection2020
    }

    if election.electionTemplateName in EXTENDED_ELECTION_MAP:
        return EXTENDED_ELECTION_MAP[election.electionTemplateName](election=election)
    else:
        return None


class ExtendedElection:
    from orm.entities import Election

    role_based_access_config = None

    def __init__(self, election: Election, role_based_access_config=None):
        self.election = election
        self.role_based_access_config = role_based_access_config

    def get_extended_tally_sheet_version_class(self, templateName):

        EXTENDED_TEMPLATE_MAP = {
            # TODO
        }

        if templateName in EXTENDED_TEMPLATE_MAP:
            return EXTENDED_TEMPLATE_MAP[templateName]
        else:
            return ExtendedTallySheetVersion

    def build_election(self, party_candidate_dataset_file=None,
                       polling_station_dataset_file=None, postal_counting_centers_dataset_file=None,
                       invalid_vote_categories_dataset_file=None):
        pass

    def get_area_map_for_tally_sheet(self, tally_sheet):
        area = tally_sheet.area
        return self.get_area_map(area=area)

    def get_area_map(self, area):

        from orm.enums import AreaTypeEnum

        area_map_subquery = self.get_area_map_query().subquery()
        area_map = []
        if area.areaType == AreaTypeEnum.CountingCentre:
            area_map = db.session.query(
                bindparam("pollingStationId", None),
                bindparam("pollingStationName", None),
                area_map_subquery.c.countingCentreId,
                area_map_subquery.c.countingCentreName,
                area_map_subquery.c.pollingDivisionId,
                area_map_subquery.c.pollingDivisionName,
                area_map_subquery.c.electoralDistrictId,
                area_map_subquery.c.electoralDistrictName,
            ).filter(
                area_map_subquery.c.countingCentreId == area.areaId
            ).group_by(
                area_map_subquery.c.countingCentreId,
                area_map_subquery.c.pollingDivisionId,
                area_map_subquery.c.electoralDistrictId
            ).all()

        return area_map

    def get_area_map_query(self):

        from orm.entities import Election, Area
        from orm.entities.Area import AreaAreaModel
        from orm.enums import AreaTypeEnum

        country = db.session.query(Area.Model).filter(
            Area.Model.areaType == AreaTypeEnum.Country).subquery()
        electoral_district = db.session.query(Area.Model).filter(
            Area.Model.areaType == AreaTypeEnum.ElectoralDistrict).subquery()
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

        country__electoral_district = aliased(AreaAreaModel)
        electoral_district__polling_division = aliased(AreaAreaModel)
        polling_division__polling_district = aliased(AreaAreaModel)
        polling_district__polling_station = aliased(AreaAreaModel)
        counting_centre__polling_station = aliased(AreaAreaModel)
        counting_centre__polling_station = aliased(AreaAreaModel)
        district_centre__counting_centre = aliased(AreaAreaModel)
        election_commission__district_centre = aliased(AreaAreaModel)

        electoral_district__counting_centre = aliased(AreaAreaModel)

        query = db.session.query(
            country.c.areaId.label("countryId"),
            country.c.areaName.label("countryName"),
            electoral_district.c.areaId.label("electoralDistrictId"),
            electoral_district.c.areaName.label("electoralDistrictName"),
            polling_division.c.areaId.label("pollingDivisionId"),
            polling_division.c.areaName.label("pollingDivisionName"),
            polling_district.c.areaId.label("pollingDistrictId"),
            polling_district.c.areaName.label("pollingDistrictName"),
            polling_station.c.areaId.label("pollingStationId"),
            polling_station.c.areaName.label("pollingStationName"),
            counting_centre.c.areaId.label("countingCentreId"),
            counting_centre.c.areaName.label("countingCentreName"),
            Election.Model.voteType
        ).filter(
            country__electoral_district.parentAreaId == country.c.areaId,
            country__electoral_district.childAreaId == electoral_district.c.areaId,

            electoral_district__polling_division.parentAreaId == electoral_district.c.areaId,
            electoral_district__polling_division.childAreaId == polling_division.c.areaId,

            polling_division__polling_district.parentAreaId == polling_division.c.areaId,
            polling_division__polling_district.childAreaId == polling_district.c.areaId,

            polling_district__polling_station.parentAreaId == polling_district.c.areaId,
            polling_district__polling_station.childAreaId == polling_station.c.areaId,

            counting_centre__polling_station.parentAreaId == counting_centre.c.areaId,
            counting_centre__polling_station.childAreaId == polling_station.c.areaId,

            district_centre__counting_centre.parentAreaId == district_centre.c.areaId,
            district_centre__counting_centre.childAreaId == counting_centre.c.areaId,

            election_commission__district_centre.parentAreaId == election_commission.c.areaId,
            election_commission__district_centre.childAreaId == district_centre.c.areaId,

            Election.Model.electionId == counting_centre.c.electionId
        )

        return query

    def get_area_map_query_postal(self):

        from orm.entities import Election, Area
        from orm.entities.Area import AreaAreaModel
        from orm.enums import AreaTypeEnum

        country = db.session.query(Area.Model).filter(
            Area.Model.areaType == AreaTypeEnum.Country).subquery()
        electoral_district = db.session.query(Area.Model).filter(
            Area.Model.areaType == AreaTypeEnum.ElectoralDistrict).subquery()
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

        country__electoral_district = aliased(AreaAreaModel)
        electoral_district__polling_division = aliased(AreaAreaModel)
        polling_division__polling_district = aliased(AreaAreaModel)
        polling_district__polling_station = aliased(AreaAreaModel)
        counting_centre__polling_station = aliased(AreaAreaModel)
        counting_centre__polling_station = aliased(AreaAreaModel)
        district_centre__counting_centre = aliased(AreaAreaModel)
        election_commission__district_centre = aliased(AreaAreaModel)

        electoral_district__counting_centre = aliased(AreaAreaModel)

        query = db.session.query(
            country.c.areaId.label("countryId"),
            country.c.areaName.label("countryName"),
            electoral_district.c.areaId.label("electoralDistrictId"),
            electoral_district.c.areaName.label("electoralDistrictName"),
            polling_division.c.areaId.label("pollingDivisionId"),
            polling_division.c.areaName.label("pollingDivisionName"),
            polling_district.c.areaId.label("pollingDistrictId"),
            polling_district.c.areaName.label("pollingDistrictName"),
            polling_station.c.areaId.label("pollingStationId"),
            polling_station.c.areaName.label("pollingStationName"),
            counting_centre.c.areaId.label("countingCentreId"),
            counting_centre.c.areaName.label("countingCentreName"),
            Election.Model.voteType
        ).filter(
            country__electoral_district.parentAreaId == country.c.areaId,
            country__electoral_district.childAreaId == electoral_district.c.areaId,

            electoral_district__counting_centre.parentAreaId == electoral_district.c.areaId,
            electoral_district__counting_centre.childAreaId == counting_centre.c.areaId,

            district_centre__counting_centre.parentAreaId == district_centre.c.areaId,
            district_centre__counting_centre.childAreaId == counting_centre.c.areaId,

            election_commission__district_centre.parentAreaId == election_commission.c.areaId,
            election_commission__district_centre.childAreaId == district_centre.c.areaId,

            Election.Model.electionId == counting_centre.c.electionId
        )

        return query
