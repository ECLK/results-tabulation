from sqlalchemy import bindparam
from sqlalchemy.orm import aliased

from app import db
from constants.TALLY_SHEET_COLUMN_SOURCE import TALLY_SHEET_COLUMN_SOURCE_META, TALLY_SHEET_COLUMN_SOURCE_CONTENT, \
    TALLY_SHEET_COLUMN_SOURCE_QUERY
from ext.ExtendedElection.ExtendedElectionPresidentialElection2019.ExtendedTallySheet.ExtendedTallySheet_PRE_30_ED import \
    ExtendedTallySheet_PRE_30_ED
from ext.ExtendedElection.ExtendedElectionPresidentialElection2019.ExtendedTallySheet.ExtendedTallySheet_PRE_30_PD import \
    ExtendedTallySheet_PRE_30_PD
from ext.ExtendedElection.ExtendedElectionPresidentialElection2019.ExtendedTallySheet.ExtendedTallySheet_PRE_41 import \
    ExtendedTallySheet_PRE_41
from ext.ExtendedElection.ExtendedElectionPresidentialElection2019.ExtendedTallySheet.ExtendedTallySheet_PRE_AI import \
    ExtendedTallySheet_PRE_AI
from ext.ExtendedElection.ExtendedElectionPresidentialElection2019.ExtendedTallySheet.ExtendedTallySheet_PRE_AI_ED import \
    ExtendedTallySheet_PRE_AI_ED
from ext.ExtendedElection.ExtendedElectionPresidentialElection2019.TALLY_SHEET_CODES import CE_201, CE_201_PV, PRE_41, \
    PRE_30_PD, PRE_30_ED, \
    PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS, PRE_ALL_ISLAND_RESULTS, PRE_34_CO, PRE_34_I_RO, PRE_34_II_RO, PRE_34, \
    PRE_34_PD, PRE_34_ED, PRE_34_AI
from ext.ExtendedElection.ExtendedElectionPresidentialElection2019.WORKFLOW_ACTION_TYPE import \
    WORKFLOW_ACTION_TYPE_VIEW, \
    WORKFLOW_ACTION_TYPE_SAVE, WORKFLOW_ACTION_TYPE_SUBMIT, WORKFLOW_ACTION_TYPE_REQUEST_CHANGES, \
    WORKFLOW_ACTION_TYPE_VERIFY, WORKFLOW_ACTION_TYPE_EDIT, \
    WORKFLOW_ACTION_TYPE_MOVE_TO_CERTIFY, WORKFLOW_ACTION_TYPE_CERTIFY, WORKFLOW_ACTION_TYPE_RELEASE, \
    WORKFLOW_ACTION_TYPE_PRINT
from ext.ExtendedElection.ExtendedElectionPresidentialElection2019.WORKFLOW_STATUS_TYPE import \
    WORKFLOW_STATUS_TYPE_EMPTY, \
    WORKFLOW_STATUS_TYPE_SAVED, WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED, WORKFLOW_STATUS_TYPE_SUBMITTED, \
    WORKFLOW_STATUS_TYPE_VERIFIED, WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY, \
    WORKFLOW_STATUS_TYPE_CERTIFIED, WORKFLOW_STATUS_TYPE_RELEASED
from constants.VOTE_TYPES import Postal, NonPostal
from ext import TallySheetMap
from ext.ExtendedElection import ExtendedElection
from ext.ExtendedElection.ExtendedElectionPresidentialElection2019 import RoleBasedAccess
from ext.ExtendedElection.util import get_rows_from_csv, update_dashboard_tables
from orm.entities import Election, Candidate, Template, Party, Meta, Workflow
from orm.entities.Area import AreaMap
from orm.entities.Area.Electorate import Country, ElectoralDistrict, PollingDivision, PollingDistrict
from orm.entities.Area.Office import PollingStation, CountingCentre, DistrictCentre, ElectionCommission
from orm.entities.Submission import TallySheet
from orm.enums import AreaTypeEnum

role_based_access_config = RoleBasedAccess.role_based_access_config


class ExtendedElectionPresidentialElection2019(ExtendedElection):
    def __init__(self, election):
        super(ExtendedElectionPresidentialElection2019, self).__init__(
            election=election,
            role_based_access_config=role_based_access_config
        )

    def get_extended_tally_sheet_class(self, templateName):
        EXTENDED_TEMPLATE_MAP = {
            PRE_41: ExtendedTallySheet_PRE_41,
            PRE_30_PD: ExtendedTallySheet_PRE_30_PD,
            PRE_30_ED: ExtendedTallySheet_PRE_30_ED,
            PRE_ALL_ISLAND_RESULTS: ExtendedTallySheet_PRE_AI,
            PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS: ExtendedTallySheet_PRE_AI_ED
        }

        if templateName in EXTENDED_TEMPLATE_MAP:
            return EXTENDED_TEMPLATE_MAP[templateName]
        else:
            return super(ExtendedElectionPresidentialElection2019, self).get_extended_tally_sheet_class(
                templateName=templateName
            )

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
        district_centre__counting_centre = aliased(AreaAreaModel)
        election_commission__district_centre = aliased(AreaAreaModel)

        # For postal vote counting centres.
        electoral_district__counting_centre = aliased(AreaAreaModel)

        query_args = [
            country.c.areaId.label("countryId"),
            country.c.areaName.label("countryName"),
            electoral_district.c.areaId.label("electoralDistrictId"),
            electoral_district.c.areaName.label("electoralDistrictName"),
            counting_centre.c.areaId.label("countingCentreId"),
            counting_centre.c.areaName.label("countingCentreName"),
            Election.Model.voteType
        ]

        query_filter = [
            country__electoral_district.parentAreaId == country.c.areaId,
            country__electoral_district.childAreaId == electoral_district.c.areaId,

            district_centre__counting_centre.parentAreaId == district_centre.c.areaId,
            district_centre__counting_centre.childAreaId == counting_centre.c.areaId,

            election_commission__district_centre.parentAreaId == election_commission.c.areaId,
            election_commission__district_centre.childAreaId == district_centre.c.areaId,

            Election.Model.electionId == counting_centre.c.electionId
        ]

        if self.election.voteType == Postal:
            query_args += [
                bindparam("pollingDivisionId", None),
                bindparam("pollingDivisionName", None),
                bindparam("pollingDistrictId", None),
                bindparam("pollingDistrictName", None),
                bindparam("pollingStationId", None),
                bindparam("pollingStationName", None)
            ]
            query_filter += [
                electoral_district__counting_centre.parentAreaId == electoral_district.c.areaId,
                electoral_district__counting_centre.childAreaId == counting_centre.c.areaId
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
                electoral_district__polling_division.parentAreaId == electoral_district.c.areaId,
                electoral_district__polling_division.childAreaId == polling_division.c.areaId,

                polling_division__polling_district.parentAreaId == polling_division.c.areaId,
                polling_division__polling_district.childAreaId == polling_district.c.areaId,

                polling_district__polling_station.parentAreaId == polling_district.c.areaId,
                polling_district__polling_station.childAreaId == polling_station.c.areaId,

                counting_centre__polling_station.parentAreaId == counting_centre.c.areaId,
                counting_centre__polling_station.childAreaId == polling_station.c.areaId
            ]

        query = db.session.query(*query_args).filter(*query_filter)

        return query

    def build_election(self, party_candidate_dataset_file=None,
                       polling_station_dataset_file=None, postal_counting_centers_dataset_file=None,
                       invalid_vote_categories_dataset_file=None):
        root_election = self.election
        postal_election = root_election.add_sub_election(electionName="Postal", voteType=Postal)
        ordinary_election = root_election.add_sub_election(electionName="Ordinary", voteType=NonPostal)

        if not party_candidate_dataset_file:
            party_candidate_dataset_file = root_election.partyCandidateDataset.fileContent

        if not polling_station_dataset_file:
            polling_station_dataset_file = root_election.pollingStationsDataset.fileContent

        if not postal_counting_centers_dataset_file:
            postal_counting_centers_dataset_file = root_election.postalCountingCentresDataset.fileContent

        if not invalid_vote_categories_dataset_file:
            invalid_vote_categories_dataset_file = root_election.invalidVoteCategoriesDataset.fileContent

        workflow_data_entry: Workflow = Workflow.create(
            workflowName="Data Entry",
            firstStatus=WORKFLOW_STATUS_TYPE_EMPTY,
            lastStatus=WORKFLOW_STATUS_TYPE_VERIFIED,
            statuses=[
                WORKFLOW_STATUS_TYPE_EMPTY,
                WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED,
                WORKFLOW_STATUS_TYPE_SAVED,
                WORKFLOW_STATUS_TYPE_SUBMITTED,
                WORKFLOW_STATUS_TYPE_VERIFIED
            ],
            actions=[
                {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW,
                 "fromStatus": WORKFLOW_STATUS_TYPE_EMPTY, "toStatus": WORKFLOW_STATUS_TYPE_EMPTY},
                {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW,
                 "fromStatus": WORKFLOW_STATUS_TYPE_SAVED, "toStatus": WORKFLOW_STATUS_TYPE_SAVED},
                {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW,
                 "fromStatus": WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED,
                 "toStatus": WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED},
                {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW,
                 "fromStatus": WORKFLOW_STATUS_TYPE_SUBMITTED, "toStatus": WORKFLOW_STATUS_TYPE_SUBMITTED},
                {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW,
                 "fromStatus": WORKFLOW_STATUS_TYPE_VERIFIED, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},

                {"name": "Print", "type": WORKFLOW_ACTION_TYPE_PRINT,
                 "fromStatus": WORKFLOW_STATUS_TYPE_SUBMITTED, "toStatus": WORKFLOW_STATUS_TYPE_SUBMITTED},
                {"name": "Print", "type": WORKFLOW_ACTION_TYPE_PRINT,
                 "fromStatus": WORKFLOW_STATUS_TYPE_VERIFIED, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},

                {"name": "Enter", "type": WORKFLOW_ACTION_TYPE_SAVE,
                 "fromStatus": WORKFLOW_STATUS_TYPE_EMPTY, "toStatus": WORKFLOW_STATUS_TYPE_SAVED},
                {"name": "EDIT", "type": WORKFLOW_ACTION_TYPE_SAVE,
                 "fromStatus": WORKFLOW_STATUS_TYPE_SAVED, "toStatus": WORKFLOW_STATUS_TYPE_SAVED},

                {"name": "Submit", "type": WORKFLOW_ACTION_TYPE_SUBMIT,
                 "fromStatus": WORKFLOW_STATUS_TYPE_SAVED, "toStatus": WORKFLOW_STATUS_TYPE_SUBMITTED},

                {"name": "Verify", "type": WORKFLOW_ACTION_TYPE_VERIFY,
                 "fromStatus": WORKFLOW_STATUS_TYPE_SUBMITTED, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},

                {"name": "Edit", "type": WORKFLOW_ACTION_TYPE_EDIT,
                 "fromStatus": WORKFLOW_STATUS_TYPE_SUBMITTED, "toStatus": WORKFLOW_STATUS_TYPE_SAVED},

                {"name": "Edit", "type": WORKFLOW_ACTION_TYPE_EDIT,
                 "fromStatus": WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED, "toStatus": WORKFLOW_STATUS_TYPE_SAVED},

                {"name": "Request Changes", "type": WORKFLOW_ACTION_TYPE_REQUEST_CHANGES,
                 "fromStatus": WORKFLOW_STATUS_TYPE_SUBMITTED, "toStatus": WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED},

                {"name": "Request Changes", "type": WORKFLOW_ACTION_TYPE_REQUEST_CHANGES,
                 "fromStatus": WORKFLOW_STATUS_TYPE_VERIFIED, "toStatus": WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED}
            ]
        )

        workflow_report: Workflow = Workflow.create(
            workflowName="Data Entry",
            firstStatus=WORKFLOW_STATUS_TYPE_EMPTY,
            lastStatus=WORKFLOW_STATUS_TYPE_VERIFIED,
            statuses=[
                WORKFLOW_STATUS_TYPE_EMPTY,
                WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED,
                WORKFLOW_STATUS_TYPE_SAVED,
                WORKFLOW_STATUS_TYPE_VERIFIED
            ],
            actions=[
                {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW,
                 "fromStatus": WORKFLOW_STATUS_TYPE_EMPTY, "toStatus": WORKFLOW_STATUS_TYPE_SAVED},
                {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW,
                 "fromStatus": WORKFLOW_STATUS_TYPE_SAVED, "toStatus": WORKFLOW_STATUS_TYPE_SAVED},
                {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW,
                 "fromStatus": WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED,
                 "toStatus": WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED},
                {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW,
                 "fromStatus": WORKFLOW_STATUS_TYPE_VERIFIED, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},

                {"name": "Print", "type": WORKFLOW_ACTION_TYPE_PRINT,
                 "fromStatus": WORKFLOW_STATUS_TYPE_VERIFIED, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},

                {"name": "Verify", "type": WORKFLOW_ACTION_TYPE_VERIFY,
                 "fromStatus": WORKFLOW_STATUS_TYPE_EMPTY, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
                {"name": "Verify", "type": WORKFLOW_ACTION_TYPE_VERIFY,
                 "fromStatus": WORKFLOW_STATUS_TYPE_SAVED, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
                {"name": "Verify", "type": WORKFLOW_ACTION_TYPE_VERIFY,
                 "fromStatus": WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},

                {"name": "Request Changes", "type": WORKFLOW_ACTION_TYPE_REQUEST_CHANGES,
                 "fromStatus": WORKFLOW_STATUS_TYPE_VERIFIED, "toStatus": WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED}
            ]
        )

        workflow_released_report: Workflow = Workflow.create(
            workflowName="Data Entry",
            firstStatus=WORKFLOW_STATUS_TYPE_EMPTY,
            lastStatus=WORKFLOW_STATUS_TYPE_RELEASED,
            statuses=[
                WORKFLOW_STATUS_TYPE_EMPTY,
                WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED,
                WORKFLOW_STATUS_TYPE_SAVED,
                WORKFLOW_STATUS_TYPE_VERIFIED,
                WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY,
                WORKFLOW_STATUS_TYPE_CERTIFIED,
                WORKFLOW_STATUS_TYPE_RELEASED
            ],
            actions=[
                {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW,
                 "fromStatus": WORKFLOW_STATUS_TYPE_EMPTY, "toStatus": WORKFLOW_STATUS_TYPE_SAVED},
                {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW,
                 "fromStatus": WORKFLOW_STATUS_TYPE_SAVED, "toStatus": WORKFLOW_STATUS_TYPE_SAVED},
                {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW,
                 "fromStatus": WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED,
                 "toStatus": WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED},
                {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW,
                 "fromStatus": WORKFLOW_STATUS_TYPE_VERIFIED, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
                {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW,
                 "fromStatus": WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY,
                 "toStatus": WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY},
                {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW,
                 "fromStatus": WORKFLOW_STATUS_TYPE_CERTIFIED, "toStatus": WORKFLOW_STATUS_TYPE_CERTIFIED},
                {"name": "View", "type": WORKFLOW_ACTION_TYPE_VIEW,
                 "fromStatus": WORKFLOW_STATUS_TYPE_RELEASED, "toStatus": WORKFLOW_STATUS_TYPE_RELEASED},

                {"name": "Print", "type": WORKFLOW_ACTION_TYPE_PRINT,
                 "fromStatus": WORKFLOW_STATUS_TYPE_VERIFIED, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
                {"name": "Print", "type": WORKFLOW_ACTION_TYPE_PRINT,
                 "fromStatus": WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY,
                 "toStatus": WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY},
                {"name": "Print", "type": WORKFLOW_ACTION_TYPE_PRINT,
                 "fromStatus": WORKFLOW_STATUS_TYPE_CERTIFIED, "toStatus": WORKFLOW_STATUS_TYPE_CERTIFIED},
                {"name": "Print", "type": WORKFLOW_ACTION_TYPE_PRINT,
                 "fromStatus": WORKFLOW_STATUS_TYPE_RELEASED, "toStatus": WORKFLOW_STATUS_TYPE_RELEASED},

                {"name": "Verify", "type": WORKFLOW_ACTION_TYPE_VERIFY,
                 "fromStatus": WORKFLOW_STATUS_TYPE_EMPTY, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
                {"name": "Verify", "type": WORKFLOW_ACTION_TYPE_VERIFY,
                 "fromStatus": WORKFLOW_STATUS_TYPE_SAVED, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},
                {"name": "Verify", "type": WORKFLOW_ACTION_TYPE_VERIFY,
                 "fromStatus": WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED, "toStatus": WORKFLOW_STATUS_TYPE_VERIFIED},

                {"name": "Print and Certify", "type": WORKFLOW_ACTION_TYPE_MOVE_TO_CERTIFY,
                 "fromStatus": WORKFLOW_STATUS_TYPE_VERIFIED, "toStatus": WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY},

                {"name": "Upload and Certify", "type": WORKFLOW_ACTION_TYPE_CERTIFY,
                 "fromStatus": WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY, "toStatus": WORKFLOW_STATUS_TYPE_CERTIFIED},

                {"name": "Release", "type": WORKFLOW_ACTION_TYPE_RELEASE,
                 "fromStatus": WORKFLOW_STATUS_TYPE_CERTIFIED, "toStatus": WORKFLOW_STATUS_TYPE_RELEASED},

                {"name": "Request Changes", "type": WORKFLOW_ACTION_TYPE_REQUEST_CHANGES,
                 "fromStatus": WORKFLOW_STATUS_TYPE_VERIFIED, "toStatus": WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED},
                {"name": "Request Changes", "type": WORKFLOW_ACTION_TYPE_REQUEST_CHANGES,
                 "fromStatus": WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY,
                 "toStatus": WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED},
                {"name": "Request Changes", "type": WORKFLOW_ACTION_TYPE_REQUEST_CHANGES,
                 "fromStatus": WORKFLOW_STATUS_TYPE_CERTIFIED, "toStatus": WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED},
                {"name": "Request Changes", "type": WORKFLOW_ACTION_TYPE_REQUEST_CHANGES,
                 "fromStatus": WORKFLOW_STATUS_TYPE_RELEASED, "toStatus": WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED}
            ]
        )

        tally_sheet_template_ce_201 = Template.create(
            templateName=CE_201
        )
        tally_sheet_template_ce_201_ballot_box_row = tally_sheet_template_ce_201.add_row(
            templateRowType="BALLOT_BOX",
            hasMany=True,
            isDerived=False,
            columns=[
                {"columnName": "electionId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "areaId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT},
                {"columnName": "ballotBoxId", "grouped": False, "func": None,
                 "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT}
            ]
        )
        tally_sheet_template_ce_201_number_of_ballots_received = tally_sheet_template_ce_201.add_row(
            templateRowType="NUMBER_OF_BALLOTS_RECEIVED",
            hasMany=True,
            isDerived=False,
            columns=[
                {"columnName": "electionId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "areaId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT},
                {"columnName": "numValue", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT}
            ]
        )
        tally_sheet_template_ce_201_number_of_ballots_spoilt = tally_sheet_template_ce_201.add_row(
            templateRowType="NUMBER_OF_BALLOTS_SPOILT",
            hasMany=True,
            isDerived=False,
            columns=[
                {"columnName": "electionId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "areaId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT},
                {"columnName": "numValue", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT}
            ]
        )
        tally_sheet_template_ce_201_number_of_ballots_issued = tally_sheet_template_ce_201.add_row(
            templateRowType="NUMBER_OF_BALLOTS_ISSUED",
            hasMany=True,
            isDerived=False,
            columns=[
                {"columnName": "electionId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "areaId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT},
                {"columnName": "numValue", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT}
            ]
        )
        tally_sheet_template_ce_201_number_of_ballots_unused = tally_sheet_template_ce_201.add_row(
            templateRowType="NUMBER_OF_BALLOTS_UNUSED",
            hasMany=True,
            isDerived=False,
            columns=[
                {"columnName": "electionId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "areaId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT},
                {"columnName": "numValue", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT}
            ]
        )
        tally_sheet_template_ce_201_number_of_ordinary_ballots_in_ballot_paper_account = tally_sheet_template_ce_201.add_row(
            templateRowType="NUMBER_OF_ORDINARY_BALLOTS_IN_BALLOT_PAPER_ACCOUNT",
            hasMany=True,
            isDerived=False,
            columns=[
                {"columnName": "electionId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "areaId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT},
                {"columnName": "numValue", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT}
            ]
        )
        tally_sheet_template_ce_201_number_of_ordinary_ballots_in_ballot_box = tally_sheet_template_ce_201.add_row(
            templateRowType="NUMBER_OF_ORDINARY_BALLOTS_IN_BALLOT_BOX",
            hasMany=True,
            isDerived=False,
            columns=[
                {"columnName": "electionId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "areaId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT},
                {"columnName": "numValue", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT}
            ]
        )
        tally_sheet_template_ce_201_number_of_tendered_ballots_in_ballot_paper_account = tally_sheet_template_ce_201.add_row(
            templateRowType="NUMBER_OF_TENDERED_BALLOTS_IN_BALLOT_PAPER_ACCOUNT",
            hasMany=True,
            isDerived=False,
            columns=[
                {"columnName": "electionId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "areaId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT},
                {"columnName": "numValue", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT}
            ]
        )
        tally_sheet_template_ce_201_number_of_tendered_ballots_in_ballot_box = tally_sheet_template_ce_201.add_row(
            templateRowType="NUMBER_OF_TENDERED_BALLOTS_IN_BALLOT_BOX",
            hasMany=True,
            isDerived=False,
            columns=[
                {"columnName": "electionId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "areaId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT},
                {"columnName": "numValue", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT}
            ]
        )

        tally_sheet_template_ce_201_pv = Template.create(
            templateName=CE_201_PV
        )

        tally_sheet_template_ce_201_pv_situation_row = tally_sheet_template_ce_201_pv.add_row(
            templateRowType="SITUATION",
            hasMany=False,
            isDerived=False,
            columns=[
                {"columnName": "electionId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "areaId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "strValue", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT}
            ]
        )
        tally_sheet_template_ce_201_pv_time_of_commencement_row = tally_sheet_template_ce_201_pv.add_row(
            templateRowType="TIME_OF_COMMENCEMENT",
            hasMany=False,
            isDerived=False,
            columns=[
                {"columnName": "electionId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "areaId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "strValue", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT}
            ]
        )
        tally_sheet_template_ce_201_pv_ballot_box_row = tally_sheet_template_ce_201_pv.add_row(
            templateRowType="BALLOT_BOX",
            hasMany=True,
            isDerived=False,
            columns=[
                {"columnName": "electionId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "areaId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "ballotBoxId", "grouped": False, "func": None,
                 "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT},
                {"columnName": "strValue", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT}
            ]
        )
        tally_sheet_template_ce_201_pv_number_of_packets_inserted_to_ballot_box_row = tally_sheet_template_ce_201_pv.add_row(
            templateRowType="NUMBER_OF_PACKETS_INSERTED_TO_BALLOT_BOX",
            hasMany=True,
            isDerived=False,
            columns=[
                {"columnName": "electionId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "areaId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "ballotBoxId", "grouped": False, "func": None,
                 "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT},
                {"columnName": "numValue", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT}
            ]
        )
        tally_sheet_template_ce_201_pv_number_of_packets_found_inside_ballot_box_row = tally_sheet_template_ce_201_pv.add_row(
            templateRowType="NUMBER_OF_PACKETS_FOUND_INSIDE_BALLOT_BOX",
            hasMany=True,
            isDerived=False,
            columns=[
                {"columnName": "electionId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "areaId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "ballotBoxId", "grouped": False, "func": None,
                 "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT},
                {"columnName": "numValue", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT}
            ]
        )
        tally_sheet_template_ce_201_pv_number_of_packets_rejected_after_opening_cover_a_row = tally_sheet_template_ce_201_pv.add_row(
            templateRowType="NUMBER_OF_PACKETS_REJECTED_AFTER_OPENING_COVER_A",
            hasMany=False,
            isDerived=False,
            columns=[
                {"columnName": "electionId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "areaId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "numValue", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT}
            ]
        )
        tally_sheet_template_ce_201_pv_number_of_packets_rejected_after_opening_cover_b_row = tally_sheet_template_ce_201_pv.add_row(
            templateRowType="NUMBER_OF_PACKETS_REJECTED_AFTER_OPENING_COVER_B",
            hasMany=False,
            isDerived=False,
            columns=[
                {"columnName": "electionId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "areaId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "numValue", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT}
            ]
        )

        tally_sheet_template_pre_41 = Template.create(
            templateName=PRE_41
        )
        tally_sheet_template_pre_41_candidate_wise_first_preference_row = tally_sheet_template_pre_41.add_row(
            templateRowType="CANDIDATE_FIRST_PREFERENCE",
            hasMany=True,
            isDerived=False,
            columns=[
                {"columnName": "electionId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "areaId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "partyId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT},
                {"columnName": "candidateId", "grouped": False, "func": None,
                 "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT},
                {"columnName": "numValue", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT},
                {"columnName": "strValue", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT}
            ]
        )
        tally_sheet_template_pre_41_rejected_vote_row = tally_sheet_template_pre_41.add_row(
            templateRowType="REJECTED_VOTE",
            hasMany=False,
            isDerived=False,
            columns=[
                {"columnName": "electionId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "areaId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "numValue", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT}
            ]
        )

        tally_sheet_template_pre_30_pd = Template.create(
            templateName=PRE_30_PD
        )
        tally_sheet_template_pre_30_pd_candidate_wise_first_preference_row = tally_sheet_template_pre_30_pd.add_row(
            templateRowType="CANDIDATE_FIRST_PREFERENCE",
            hasMany=True,
            isDerived=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "areaId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "partyId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "candidateId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "numValue", "grouped": False, "func": "sum", "source": TALLY_SHEET_COLUMN_SOURCE_QUERY}
            ]
        ).add_derivative_template_row(tally_sheet_template_pre_41_candidate_wise_first_preference_row)
        tally_sheet_template_pre_30_pd_rejected_vote_row = tally_sheet_template_pre_30_pd.add_row(
            templateRowType="REJECTED_VOTE",
            hasMany=True,
            isDerived=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "areaId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "numValue", "grouped": False, "func": "sum", "source": TALLY_SHEET_COLUMN_SOURCE_QUERY}
            ]
        ).add_derivative_template_row(tally_sheet_template_pre_41_rejected_vote_row)

        tally_sheet_template_pre_30_ed = Template.create(
            templateName=PRE_30_ED
        )
        tally_sheet_template_pre_30_ed_candidate_wise_first_preference_row = tally_sheet_template_pre_30_ed.add_row(
            templateRowType="CANDIDATE_FIRST_PREFERENCE",
            hasMany=True,
            isDerived=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "areaId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "partyId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "candidateId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "numValue", "grouped": False, "func": "sum", "source": TALLY_SHEET_COLUMN_SOURCE_QUERY}
            ]
        ).add_derivative_template_row(tally_sheet_template_pre_30_pd_candidate_wise_first_preference_row)
        tally_sheet_template_pre_30_ed_rejected_vote_row = tally_sheet_template_pre_30_ed.add_row(
            templateRowType="REJECTED_VOTE",
            hasMany=True,
            isDerived=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "areaId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "numValue", "grouped": False, "func": "sum", "source": TALLY_SHEET_COLUMN_SOURCE_QUERY}
            ]
        ).add_derivative_template_row(tally_sheet_template_pre_30_pd_rejected_vote_row)

        tally_sheet_template_pre_all_island_ed = Template.create(
            templateName=PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS
        )
        tally_sheet_template_pre_all_island_ed_candidate_wise_first_preference_row = tally_sheet_template_pre_all_island_ed.add_row(
            templateRowType="CANDIDATE_FIRST_PREFERENCE",
            hasMany=True,
            isDerived=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "areaId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "partyId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "candidateId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "numValue", "grouped": False, "func": "sum", "source": TALLY_SHEET_COLUMN_SOURCE_QUERY}
            ]
        ).add_derivative_template_row(tally_sheet_template_pre_30_ed_candidate_wise_first_preference_row)
        tally_sheet_template_pre_all_island_ed_rejected_vote_row = tally_sheet_template_pre_all_island_ed.add_row(
            templateRowType="REJECTED_VOTE",
            hasMany=False,
            isDerived=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "areaId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "numValue", "grouped": False, "func": "sum", "source": TALLY_SHEET_COLUMN_SOURCE_QUERY}
            ]
        ).add_derivative_template_row(tally_sheet_template_pre_30_ed_rejected_vote_row)

        tally_sheet_template_pre_all_island = Template.create(
            templateName=PRE_ALL_ISLAND_RESULTS
        )
        tally_sheet_template_pre_all_island_candidate_wise_first_preference_row = tally_sheet_template_pre_all_island.add_row(
            templateRowType="CANDIDATE_FIRST_PREFERENCE",
            hasMany=True,
            isDerived=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "areaId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "partyId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "candidateId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "numValue", "grouped": False, "func": "sum", "source": TALLY_SHEET_COLUMN_SOURCE_QUERY}
            ]
        ).add_derivative_template_row(tally_sheet_template_pre_all_island_ed_candidate_wise_first_preference_row)
        tally_sheet_template_pre_all_island_rejected_vote_row = tally_sheet_template_pre_all_island.add_row(
            templateRowType="REJECTED_VOTE",
            hasMany=True,
            isDerived=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "areaId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "numValue", "grouped": False, "func": "sum", "source": TALLY_SHEET_COLUMN_SOURCE_QUERY}
            ]
        ).add_derivative_template_row(tally_sheet_template_pre_all_island_ed_rejected_vote_row)

        tally_sheet_template_pre_34_co = Template.create(
            templateName=PRE_34_CO
        )
        tally_sheet_template_pre_34_co_candidate_wise_second_preference_row = tally_sheet_template_pre_34_co.add_row(
            templateRowType="CANDIDATE_SECOND_PREFERENCE",
            hasMany=True,
            isDerived=False,
            columns=[
                {"columnName": "electionId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "areaId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "partyId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT},
                {"columnName": "candidateId", "grouped": False, "func": None,
                 "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT},
                {"columnName": "numValue", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT}
            ]
        )
        tally_sheet_template_pre_34_co_candidate_wise_third_preference_row = tally_sheet_template_pre_34_co.add_row(
            templateRowType="CANDIDATE_THIRD_PREFERENCE",
            hasMany=True,
            isDerived=False,
            columns=[
                {"columnName": "electionId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "areaId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "partyId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT},
                {"columnName": "candidateId", "grouped": False, "func": None,
                 "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT},
                {"columnName": "numValue", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT}
            ]
        )

        tally_sheet_template_pre_34_i_ro = Template.create(
            templateName=PRE_34_I_RO
        )
        tally_sheet_template_pre_34_i_ro_candidate_wise_second_preference_row = tally_sheet_template_pre_34_i_ro.add_row(
            templateRowType="CANDIDATE_SECOND_PREFERENCE",
            hasMany=True,
            isDerived=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "areaId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "partyId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "candidateId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "numValue", "grouped": False, "func": "sum", "source": TALLY_SHEET_COLUMN_SOURCE_QUERY}
            ]
        ).add_derivative_template_row(tally_sheet_template_pre_34_co_candidate_wise_second_preference_row)
        tally_sheet_template_pre_34_i_ro_candidate_wise_third_preference_row = tally_sheet_template_pre_34_i_ro.add_row(
            templateRowType="CANDIDATE_THIRD_PREFERENCE",
            hasMany=True,
            isDerived=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "areaId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "partyId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "candidateId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "numValue", "grouped": False, "func": "sum", "source": TALLY_SHEET_COLUMN_SOURCE_QUERY}
            ]
        ).add_derivative_template_row(tally_sheet_template_pre_34_co_candidate_wise_third_preference_row)

        tally_sheet_template_pre_34_ii_ro = Template.create(
            templateName=PRE_34_II_RO
        )
        tally_sheet_template_pre_34_ii_ro_candidate_wise_second_preference_row = tally_sheet_template_pre_34_ii_ro.add_row(
            templateRowType="CANDIDATE_SECOND_PREFERENCE",
            hasMany=True,
            isDerived=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "areaId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "partyId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "candidateId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "numValue", "grouped": False, "func": "sum", "source": TALLY_SHEET_COLUMN_SOURCE_QUERY}
            ]
        ).add_derivative_template_row(tally_sheet_template_pre_34_i_ro_candidate_wise_second_preference_row)
        tally_sheet_template_pre_34_ii_ro_candidate_wise_third_preference_row = tally_sheet_template_pre_34_ii_ro.add_row(
            templateRowType="CANDIDATE_THIRD_PREFERENCE",
            hasMany=True,
            isDerived=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "areaId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "partyId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "candidateId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "numValue", "grouped": False, "func": "sum", "source": TALLY_SHEET_COLUMN_SOURCE_QUERY}
            ]
        ).add_derivative_template_row(tally_sheet_template_pre_34_i_ro_candidate_wise_third_preference_row)

        tally_sheet_template_pre_34 = Template.create(
            templateName=PRE_34
        )
        tally_sheet_template_pre_34_candidate_wise_second_preference_row = tally_sheet_template_pre_34.add_row(
            templateRowType="CANDIDATE_SECOND_PREFERENCE",
            hasMany=True,
            isDerived=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "areaId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "partyId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "candidateId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "numValue", "grouped": False, "func": "sum", "source": TALLY_SHEET_COLUMN_SOURCE_QUERY}
            ]
        ).add_derivative_template_row(tally_sheet_template_pre_34_ii_ro_candidate_wise_second_preference_row)
        tally_sheet_template_pre_34_candidate_wise_second_preference_row = tally_sheet_template_pre_34.add_row(
            templateRowType="CANDIDATE_THIRD_PREFERENCE",
            hasMany=True,
            isDerived=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "areaId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "partyId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "candidateId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "numValue", "grouped": False, "func": "sum", "source": TALLY_SHEET_COLUMN_SOURCE_QUERY}
            ]
        ).add_derivative_template_row(tally_sheet_template_pre_34_ii_ro_candidate_wise_third_preference_row)

        tally_sheet_template_pre_34_pd = Template.create(
            templateName=PRE_34_PD
        )
        tally_sheet_template_pre_34_pd_candidate_wise_first_preference_row = tally_sheet_template_pre_34_pd.add_row(
            templateRowType="CANDIDATE_FIRST_PREFERENCE",
            hasMany=True,
            isDerived=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "areaId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "partyId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "candidateId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "numValue", "grouped": False, "func": "sum", "source": TALLY_SHEET_COLUMN_SOURCE_QUERY}
            ]
        ).add_derivative_template_row(tally_sheet_template_pre_30_pd_candidate_wise_first_preference_row)
        tally_sheet_template_pre_34_pd_candidate_wise_second_preference_row = tally_sheet_template_pre_34_pd.add_row(
            templateRowType="CANDIDATE_SECOND_PREFERENCE",
            hasMany=True,
            isDerived=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "areaId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "partyId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "candidateId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "numValue", "grouped": False, "func": "sum", "source": TALLY_SHEET_COLUMN_SOURCE_QUERY}
            ]
        ).add_derivative_template_row(tally_sheet_template_pre_34_i_ro_candidate_wise_second_preference_row)
        tally_sheet_template_pre_34_pd_candidate_wise_third_preference_row = tally_sheet_template_pre_34_pd.add_row(
            templateRowType="CANDIDATE_THIRD_PREFERENCE",
            hasMany=True,
            isDerived=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "areaId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "partyId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "candidateId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "numValue", "grouped": False, "func": "sum", "source": TALLY_SHEET_COLUMN_SOURCE_QUERY}
            ]
        ).add_derivative_template_row(tally_sheet_template_pre_34_i_ro_candidate_wise_third_preference_row)

        tally_sheet_template_pre_34_ed = Template.create(
            templateName=PRE_34_ED
        )
        tally_sheet_template_pre_34_ed_candidate_wise_first_preference_row = tally_sheet_template_pre_34_ed.add_row(
            templateRowType="CANDIDATE_FIRST_PREFERENCE",
            hasMany=True,
            isDerived=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "areaId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "partyId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "candidateId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "numValue", "grouped": False, "func": "sum", "source": TALLY_SHEET_COLUMN_SOURCE_QUERY}
            ]
        ).add_derivative_template_row(tally_sheet_template_pre_34_pd_candidate_wise_first_preference_row)
        tally_sheet_template_pre_34_ed_candidate_wise_second_preference_row = tally_sheet_template_pre_34_ed.add_row(
            templateRowType="CANDIDATE_SECOND_PREFERENCE",
            hasMany=True,
            isDerived=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "areaId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "partyId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "candidateId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "numValue", "grouped": False, "func": "sum", "source": TALLY_SHEET_COLUMN_SOURCE_QUERY}
            ]
        ).add_derivative_template_row(tally_sheet_template_pre_34_pd_candidate_wise_second_preference_row)
        tally_sheet_template_pre_34_ed_candidate_wise_third_preference_row = tally_sheet_template_pre_34_ed.add_row(
            templateRowType="CANDIDATE_THIRD_PREFERENCE",
            hasMany=True,
            isDerived=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "areaId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "partyId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "candidateId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "numValue", "grouped": False, "func": "sum", "source": TALLY_SHEET_COLUMN_SOURCE_QUERY}
            ]
        ).add_derivative_template_row(tally_sheet_template_pre_34_pd_candidate_wise_third_preference_row)

        tally_sheet_template_pre_34_ai = Template.create(
            templateName=PRE_34_AI
        )
        tally_sheet_template_pre_34_ai_candidate_wise_first_preference_row = tally_sheet_template_pre_34_ai.add_row(
            templateRowType="CANDIDATE_FIRST_PREFERENCE",
            hasMany=True,
            isDerived=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "areaId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "partyId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "candidateId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "numValue", "grouped": False, "func": "sum", "source": TALLY_SHEET_COLUMN_SOURCE_QUERY}
            ]
        ).add_derivative_template_row(tally_sheet_template_pre_34_ed_candidate_wise_first_preference_row)
        tally_sheet_template_pre_34_ai_candidate_wise_second_preference_row = tally_sheet_template_pre_34_ai.add_row(
            templateRowType="CANDIDATE_SECOND_PREFERENCE",
            hasMany=True,
            isDerived=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "areaId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "partyId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "candidateId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "numValue", "grouped": False, "func": "sum", "source": TALLY_SHEET_COLUMN_SOURCE_QUERY}
            ]
        ).add_derivative_template_row(tally_sheet_template_pre_34_ed_candidate_wise_second_preference_row)
        tally_sheet_template_pre_34_ai_candidate_wise_third_preference_row = tally_sheet_template_pre_34_ai.add_row(
            templateRowType="CANDIDATE_THIRD_PREFERENCE",
            hasMany=True,
            isDerived=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "areaId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "partyId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "candidateId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "numValue", "grouped": False, "func": "sum", "source": TALLY_SHEET_COLUMN_SOURCE_QUERY}
            ]
        ).add_derivative_template_row(tally_sheet_template_pre_34_ed_candidate_wise_third_preference_row)

        data_entry_store = {
            AreaTypeEnum.Country: {},
            AreaTypeEnum.ElectoralDistrict: {},
            AreaTypeEnum.PollingDivision: {},
            AreaTypeEnum.PollingDistrict: {},
            AreaTypeEnum.PollingStation: {},
            AreaTypeEnum.CountingCentre: {},
            AreaTypeEnum.DistrictCentre: {},
            AreaTypeEnum.ElectionCommission: {},
        }

        def _get_area_entry(election, area_class, area_name, area_key, create_tally_sheets_callback=None):

            area_type = area_class.Model.__mapper_args__["polymorphic_identity"]

            if area_key in data_entry_store[area_type]:
                data_entry_obj = data_entry_store[area_type][area_key]
            else:
                area = area_class.create(area_name, electionId=election.electionId)

                data_entry_obj = {
                    "area": area
                }
                data_entry_store[area_type][area_key] = data_entry_obj

            if "tallySheets" not in data_entry_obj:
                data_entry_obj["tallySheets"] = {}

                if create_tally_sheets_callback is not None:
                    tally_sheets = create_tally_sheets_callback(area)

                    for tally_sheet in tally_sheets:
                        if tally_sheet.tallySheetCode not in data_entry_obj["tallySheets"]:
                            data_entry_obj["tallySheets"][tally_sheet.tallySheetCode] = []

                        data_entry_obj["tallySheets"][tally_sheet.tallySheetCode].append(tally_sheet)

            return data_entry_obj

        def _get_country_entry(election, row):
            area_class = Country
            area_name = row["Country"]
            area_key = area_name

            def _create_country_tally_sheets(area):
                tally_sheets = [
                    TallySheet.create(
                        template=tally_sheet_template_pre_all_island,
                        electionId=election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "electionId": election.electionId
                        }).metaId,
                        workflowInstanceId=workflow_released_report.get_new_instance().workflowInstanceId
                    ),
                    TallySheet.create(
                        template=tally_sheet_template_pre_all_island_ed,
                        electionId=election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "electionId": election.electionId
                        }).metaId,
                        workflowInstanceId=workflow_released_report.get_new_instance().workflowInstanceId
                    ),
                    TallySheet.create(
                        template=tally_sheet_template_pre_34_ai,
                        electionId=election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "electionId": election.electionId
                        }).metaId,
                        workflowInstanceId=workflow_released_report.get_new_instance().workflowInstanceId
                    )
                ]

                return tally_sheets

            data_entry_obj = _get_area_entry(election, area_class, area_name, area_key, _create_country_tally_sheets)

            return data_entry_obj

        def _get_electoral_district_entry(election, row):
            area_class = ElectoralDistrict
            area_name = row["Electoral District"]
            area_key = area_name

            def _create_electoral_district_tally_sheets(area):
                tally_sheets = [
                    TallySheet.create(
                        template=tally_sheet_template_pre_30_ed, electionId=election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "electionId": election.electionId
                        }).metaId,
                        workflowInstanceId=workflow_released_report.get_new_instance().workflowInstanceId
                    ),
                    TallySheet.create(
                        template=tally_sheet_template_pre_34_ed, electionId=election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "electionId": election.electionId
                        }).metaId,
                        workflowInstanceId=workflow_released_report.get_new_instance().workflowInstanceId
                    ),
                    TallySheet.create(
                        template=tally_sheet_template_pre_30_pd, electionId=postal_election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "electionId": postal_election.electionId
                        }).metaId,
                        workflowInstanceId=workflow_released_report.get_new_instance().workflowInstanceId
                    ),
                    TallySheet.create(
                        template=tally_sheet_template_pre_34_pd, electionId=postal_election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "electionId": postal_election.electionId
                        }).metaId,
                        workflowInstanceId=workflow_released_report.get_new_instance().workflowInstanceId
                    ),
                    TallySheet.create(
                        template=tally_sheet_template_pre_34_i_ro, electionId=postal_election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "electionId": postal_election.electionId
                        }).metaId,
                        workflowInstanceId=workflow_released_report.get_new_instance().workflowInstanceId
                    ),
                    TallySheet.create(
                        template=tally_sheet_template_pre_34_ii_ro, electionId=election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "electionId": election.electionId
                        }).metaId,
                        workflowInstanceId=workflow_released_report.get_new_instance().workflowInstanceId
                    ),
                    TallySheet.create(
                        template=tally_sheet_template_pre_34, electionId=election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "electionId": election.electionId
                        }).metaId,
                        workflowInstanceId=workflow_released_report.get_new_instance().workflowInstanceId
                    )
                ]

                return tally_sheets

            data_entry_obj = _get_area_entry(election, area_class, area_name, area_key,
                                             _create_electoral_district_tally_sheets)

            return data_entry_obj

        def _get_polling_division_entry(election, row):
            area_class = PollingDivision
            area_name = row["Polling Division"]
            area_key = area_name

            def _create_polling_division_tally_sheets(area):
                tally_sheets = [
                    TallySheet.create(
                        template=tally_sheet_template_pre_30_pd, electionId=ordinary_election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "electionId": ordinary_election.electionId
                        }).metaId,
                        workflowInstanceId=workflow_released_report.get_new_instance().workflowInstanceId
                    ),
                    TallySheet.create(
                        template=tally_sheet_template_pre_34_pd, electionId=ordinary_election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "electionId": ordinary_election.electionId
                        }).metaId,
                        workflowInstanceId=workflow_released_report.get_new_instance().workflowInstanceId
                    ),
                    TallySheet.create(
                        template=tally_sheet_template_pre_34_i_ro, electionId=ordinary_election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "electionId": ordinary_election.electionId
                        }).metaId,
                        workflowInstanceId=workflow_released_report.get_new_instance().workflowInstanceId
                    )
                ]

                return tally_sheets

            data_entry_obj = _get_area_entry(election, area_class, area_name, area_key,
                                             _create_polling_division_tally_sheets)

            return data_entry_obj

        def _get_polling_district_entry(election, row):
            electoral_district = _get_electoral_district_entry(election, row)["area"]
            polling_division = _get_polling_division_entry(election, row)["area"]

            area_class = PollingDistrict
            area_name = row["Polling District"]
            area_key = "%s-%s-%s" % (electoral_district.areaName, polling_division.areaName, area_name)

            data_entry_obj = _get_area_entry(election, area_class, area_name, area_key)

            return data_entry_obj

        def _get_polling_station_entry(election, row):
            electoral_district = _get_electoral_district_entry(election, row)["area"]
            polling_division = _get_polling_division_entry(election, row)["area"]
            polling_district = _get_polling_district_entry(election, row)["area"]

            area_class = PollingStation
            area_name = row["Polling Station"]
            area_key = "%s-%s-%s-%s" % (
                electoral_district.areaName, polling_division.areaName, polling_district.areaName, area_name
            )

            data_entry_obj = _get_area_entry(election, area_class, area_name, area_key)
            area = data_entry_obj["area"]
            area._registeredVotersCount = row["Registered Voters"]

            return data_entry_obj

        def _get_counting_centre_entry(election, row):
            electoral_district = _get_electoral_district_entry(election, row)["area"]

            area_class = CountingCentre
            area_name = row["Counting Centre"]
            area_key = "%s-%s" % (electoral_district.areaName, area_name)

            def _create_counting_centre_tally_sheets(area):

                tally_sheets = [
                    TallySheet.create(
                        template=tally_sheet_template_pre_41, electionId=election.electionId, areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "electionId": election.electionId
                        }).metaId,
                        workflowInstanceId=workflow_data_entry.get_new_instance().workflowInstanceId
                    ),
                    TallySheet.create(
                        template=tally_sheet_template_pre_34_co, electionId=election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "electionId": election.electionId
                        }).metaId,
                        workflowInstanceId=workflow_data_entry.get_new_instance().workflowInstanceId
                    )
                ]

                if election.voteType == NonPostal:
                    tally_sheets.append(TallySheet.create(
                        template=tally_sheet_template_ce_201, electionId=election.electionId, areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "electionId": election.electionId
                        }).metaId,
                        workflowInstanceId=workflow_data_entry.get_new_instance().workflowInstanceId
                    ))
                elif election.voteType == Postal:
                    area._registeredVotersCount = row["Registered Voters"]
                    tally_sheets.append(TallySheet.create(
                        template=tally_sheet_template_ce_201_pv, electionId=election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "electionId": election.electionId
                        }).metaId,
                        workflowInstanceId=workflow_data_entry.get_new_instance().workflowInstanceId
                    ))

                return tally_sheets

            data_entry_obj = _get_area_entry(election, area_class, area_name, area_key,
                                             _create_counting_centre_tally_sheets)

            return data_entry_obj

        def _get_district_centre_entry(election, row):
            area_class = DistrictCentre
            area_name = row["District Centre"]
            area_key = area_name

            data_entry_obj = _get_area_entry(election, area_class, area_name, area_key)

            return data_entry_obj

        def _get_election_commission_entry(election, row):
            area_class = ElectionCommission
            area_name = row["Election Commission"]
            area_key = area_name

            data_entry_obj = _get_area_entry(election, area_class, area_name, area_key)

            return data_entry_obj

        for row in get_rows_from_csv(party_candidate_dataset_file):
            party = Party.create(
                partyName=row["Party"],
                partySymbol=row["Party Symbol"],
                partyAbbreviation=row["Party Abbreviation"]
            )
            root_election.add_party(partyId=party.partyId)

            candidate = Candidate.create(candidateName=row["Candidate"])
            root_election.add_candidate(candidateId=candidate.candidateId, partyId=party.partyId)

        for row in get_rows_from_csv(invalid_vote_categories_dataset_file):
            root_election.add_invalid_vote_category(row["Invalid Vote Category Description"])

        for row in get_rows_from_csv(polling_station_dataset_file):
            row["Country"] = "Sri Lanka"
            row["Election Commission"] = "Sri Lanka Election Commission"
            row["Polling Station"] = row["Polling Station (English)"]

            print("[ROW] ========= ", row)
            country_entry = _get_country_entry(election=root_election, row=row)
            electoral_district_entry = _get_electoral_district_entry(election=root_election, row=row)
            polling_division_entry = _get_polling_division_entry(election=root_election, row=row)
            polling_district_entry = _get_polling_district_entry(election=root_election, row=row)
            election_commission_entry = _get_election_commission_entry(election=root_election, row=row)
            district_centre_entry = _get_district_centre_entry(election=root_election, row=row)
            counting_centre_entry = _get_counting_centre_entry(election=ordinary_election, row=row)
            polling_station_entry = _get_polling_station_entry(election=root_election, row=row)

            country_entry["area"].add_child(electoral_district_entry["area"].areaId)
            electoral_district_entry["area"].add_child(polling_division_entry["area"].areaId)
            polling_division_entry["area"].add_child(polling_district_entry["area"].areaId)
            polling_district_entry["area"].add_child(polling_station_entry["area"].areaId)
            election_commission_entry["area"].add_child(district_centre_entry["area"].areaId)
            district_centre_entry["area"].add_child(counting_centre_entry["area"].areaId)
            counting_centre_entry["area"].add_child(polling_station_entry["area"].areaId)

            AreaMap.create(
                electionId=root_election.electionId,
                voteType=NonPostal,
                pollingStationId=polling_station_entry["area"].areaId,
                countingCentreId=counting_centre_entry["area"].areaId,
                districtCentreId=district_centre_entry["area"].areaId,
                electionCommissionId=election_commission_entry["area"].areaId,
                pollingDistrictId=polling_district_entry["area"].areaId,
                pollingDivisionId=polling_division_entry["area"].areaId,
                electoralDistrictId=electoral_district_entry["area"].areaId,
                countryId=country_entry["area"].areaId
            )

            pre_41_tally_sheet = counting_centre_entry["tallySheets"][PRE_41][0]
            pre_34_co_tally_sheet = counting_centre_entry["tallySheets"][PRE_34_CO][0]
            ce_201_tally_sheet = counting_centre_entry["tallySheets"][CE_201][0]

            pre_30_pd_tally_sheet = polling_division_entry["tallySheets"][PRE_30_PD][0]
            pre_34_i_ro_tally_sheet = polling_division_entry["tallySheets"][PRE_34_I_RO][0]
            pre_34_pd_tally_sheet = polling_division_entry["tallySheets"][PRE_34_PD][0]

            pre_30_ed_tally_sheet = electoral_district_entry["tallySheets"][PRE_30_ED][0]
            pre_34_ii_ro_tally_sheet = electoral_district_entry["tallySheets"][PRE_34_II_RO][0]
            pre_34_tally_sheet = electoral_district_entry["tallySheets"][PRE_34][0]
            pre_34_ed_tally_sheet = electoral_district_entry["tallySheets"][PRE_34_ED][0]

            pre_all_island_ed_tally_sheet = country_entry["tallySheets"][
                PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS][0]
            pre_all_island_tally_sheet = country_entry["tallySheets"][PRE_ALL_ISLAND_RESULTS][0]
            pre_34_ai_tally_sheet = country_entry["tallySheets"][PRE_34_AI][0]

            pre_30_pd_tally_sheet.add_child(pre_41_tally_sheet)
            pre_30_ed_tally_sheet.add_child(pre_30_pd_tally_sheet)
            pre_all_island_ed_tally_sheet.add_child(pre_30_ed_tally_sheet)
            pre_all_island_tally_sheet.add_child(pre_all_island_ed_tally_sheet)

            pre_34_i_ro_tally_sheet.add_child(pre_34_co_tally_sheet)
            pre_34_ii_ro_tally_sheet.add_child(pre_34_i_ro_tally_sheet)
            pre_34_tally_sheet.add_child(pre_34_ii_ro_tally_sheet)

            pre_34_pd_tally_sheet.add_child(pre_30_pd_tally_sheet)
            pre_34_pd_tally_sheet.add_child(pre_34_i_ro_tally_sheet)
            pre_34_ed_tally_sheet.add_child(pre_34_pd_tally_sheet)
            pre_34_ai_tally_sheet.add_child(pre_34_ed_tally_sheet)

            TallySheetMap.create(
                pre_41_tallySheetId=pre_41_tally_sheet.tallySheetId,
                pre_34_co_tallySheetId=pre_34_co_tally_sheet.tallySheetId,
                ce_201_tallySheetId=ce_201_tally_sheet.tallySheetId,
                ce_201_pv_tallySheetId=None,

                pre_30_pd_tallySheetId=pre_30_pd_tally_sheet.tallySheetId,
                pre_34_i_ro_tallySheetId=pre_34_i_ro_tally_sheet.tallySheetId,
                pre_34_pd_tallySheetId=pre_34_pd_tally_sheet.tallySheetId,

                pre_30_ed_tallySheetId=pre_30_ed_tally_sheet.tallySheetId,
                pre_34_ii_ro_tallySheetId=pre_34_ii_ro_tally_sheet.tallySheetId,
                pre_34_tallySheetId=pre_34_tally_sheet.tallySheetId,
                pre_34_ed_tallySheetId=pre_34_ed_tally_sheet.tallySheetId,

                pre_all_island_ed_tallySheetId=pre_all_island_ed_tally_sheet.tallySheetId,
                pre_all_island_tallySheetId=pre_all_island_tally_sheet.tallySheetId,
                pre_34_ai_tallySheetId=pre_34_ai_tally_sheet.tallySheetId
            )

        for row in get_rows_from_csv(postal_counting_centers_dataset_file):
            row["Country"] = "Sri Lanka"
            row["Election Commission"] = "Sri Lanka Election Commission"
            row["Counting Centre"] = row["Postal Vote Counting Centre"]

            print("[POSTAL ROW] ========= ", row)
            country_entry = _get_country_entry(election=root_election, row=row)
            electoral_district_entry = _get_electoral_district_entry(election=root_election, row=row)
            election_commission_entry = _get_election_commission_entry(election=root_election, row=row)
            district_centre_entry = _get_district_centre_entry(election=root_election, row=row)
            counting_centre_entry = _get_counting_centre_entry(election=postal_election, row=row)

            country_entry["area"].add_child(electoral_district_entry["area"].areaId)
            electoral_district_entry["area"].add_child(counting_centre_entry["area"].areaId)
            district_centre_entry["area"].add_child(counting_centre_entry["area"].areaId)
            election_commission_entry["area"].add_child(district_centre_entry["area"].areaId)

            AreaMap.create(
                electionId=root_election.electionId,
                voteType=Postal,
                countingCentreId=counting_centre_entry["area"].areaId,
                districtCentreId=district_centre_entry["area"].areaId,
                electionCommissionId=election_commission_entry["area"].areaId,
                electoralDistrictId=electoral_district_entry["area"].areaId,
                countryId=country_entry["area"].areaId
            )

            pre_41_tally_sheet = counting_centre_entry["tallySheets"][PRE_41][0]
            pre_34_co_tally_sheet = counting_centre_entry["tallySheets"][PRE_34_CO][0]
            ce_201_pv_tally_sheet = counting_centre_entry["tallySheets"][CE_201_PV][0]

            pre_30_pd_tally_sheet = electoral_district_entry["tallySheets"][PRE_30_PD][0]
            pre_34_i_ro_tally_sheet = electoral_district_entry["tallySheets"][PRE_34_I_RO][0]
            pre_34_pd_tally_sheet = electoral_district_entry["tallySheets"][PRE_34_PD][0]

            pre_30_ed_tally_sheet = electoral_district_entry["tallySheets"][PRE_30_ED][0]
            pre_34_ii_ro_tally_sheet = electoral_district_entry["tallySheets"][PRE_34_II_RO][0]
            pre_34_tally_sheet = electoral_district_entry["tallySheets"][PRE_34][0]
            pre_34_ed_tally_sheet = electoral_district_entry["tallySheets"][PRE_34_ED][0]

            pre_all_island_ed_tally_sheet = country_entry["tallySheets"][
                PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS][0]
            pre_all_island_tally_sheet = country_entry["tallySheets"][PRE_ALL_ISLAND_RESULTS][0]
            pre_34_ai_tally_sheet = country_entry["tallySheets"][PRE_34_AI][0]

            pre_30_pd_tally_sheet.add_child(pre_41_tally_sheet)
            pre_30_ed_tally_sheet.add_child(pre_30_pd_tally_sheet)
            pre_all_island_ed_tally_sheet.add_child(pre_30_ed_tally_sheet)
            pre_all_island_tally_sheet.add_child(pre_all_island_ed_tally_sheet)

            pre_34_i_ro_tally_sheet.add_child(pre_34_co_tally_sheet)
            pre_34_ii_ro_tally_sheet.add_child(pre_34_i_ro_tally_sheet)
            pre_34_tally_sheet.add_child(pre_34_ii_ro_tally_sheet)

            pre_34_pd_tally_sheet.add_child(pre_30_pd_tally_sheet)
            pre_34_pd_tally_sheet.add_child(pre_34_i_ro_tally_sheet)
            pre_34_ed_tally_sheet.add_child(pre_34_pd_tally_sheet)
            pre_34_ai_tally_sheet.add_child(pre_34_ed_tally_sheet)

            TallySheetMap.create(
                pre_41_tallySheetId=pre_41_tally_sheet.tallySheetId,
                pre_34_co_tallySheetId=pre_34_co_tally_sheet.tallySheetId,
                ce_201_tallySheetId=None,
                ce_201_pv_tallySheetId=ce_201_pv_tally_sheet.tallySheetId,

                pre_30_pd_tallySheetId=pre_30_pd_tally_sheet.tallySheetId,
                pre_34_i_ro_tallySheetId=pre_34_i_ro_tally_sheet.tallySheetId,
                pre_34_pd_tallySheetId=pre_34_pd_tally_sheet.tallySheetId,

                pre_30_ed_tallySheetId=pre_30_ed_tally_sheet.tallySheetId,
                pre_34_ii_ro_tallySheetId=pre_34_ii_ro_tally_sheet.tallySheetId,
                pre_34_tallySheetId=pre_34_tally_sheet.tallySheetId,
                pre_34_ed_tallySheetId=pre_34_ed_tally_sheet.tallySheetId,

                pre_all_island_ed_tallySheetId=pre_all_island_ed_tally_sheet.tallySheetId,
                pre_all_island_tallySheetId=pre_all_island_tally_sheet.tallySheetId,
                pre_34_ai_tallySheetId=pre_34_ai_tally_sheet.tallySheetId,
            )

        db.session.commit()

        update_dashboard_tables()

        return root_election
