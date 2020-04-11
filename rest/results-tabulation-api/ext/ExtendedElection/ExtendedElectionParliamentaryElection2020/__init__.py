from app import db
from constants.TALLY_SHEET_COLUMN_SOURCE import TALLY_SHEET_COLUMN_SOURCE_META, TALLY_SHEET_COLUMN_SOURCE_CONTENT, \
    TALLY_SHEET_COLUMN_SOURCE_QUERY
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.ExtendedTallySheet.ExtendedTallySheet_POLLING_DIVISION_RESULTS import \
    ExtendedTallySheet_POLLING_DIVISION_RESULTS
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.ExtendedTallySheet.ExtendedTallySheet_ALL_ISLAND_RESULT import \
    ExtendedTallySheet_ALL_ISLAND_RESULT
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.ExtendedTallySheet.ExtendedTallySheet_CE_201 import \
    ExtendedTallySheet_CE_201
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.ExtendedTallySheet.ExtendedTallySheet_PE_21 import \
    ExtendedTallySheet_PE_21
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.ExtendedTallySheet.ExtendedTallySheet_PE_22 import \
    ExtendedTallySheet_PE_22
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.ExtendedTallySheet.ExtendedTallySheet_PE_27 import \
    ExtendedTallySheet_PE_27
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.ExtendedTallySheet.ExtendedTallySheet_PE_39 import \
    ExtendedTallySheet_PE_39
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.ExtendedTallySheet.ExtendedTallySheet_PE_4 import \
    ExtendedTallySheet_PE_4
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.ExtendedTallySheet.ExtendedTallySheet_PE_CE_RO_PR_1 import \
    ExtendedTallySheet_PE_CE_RO_PR_1
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.ExtendedTallySheet.ExtendedTallySheet_PE_CE_RO_PR_2 import \
    ExtendedTallySheet_PE_CE_RO_PR_2
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.ExtendedTallySheet.ExtendedTallySheet_PE_CE_RO_PR_3 import \
    ExtendedTallySheet_PE_CE_RO_PR_3
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.ExtendedTallySheet.ExtendedTallySheet_PE_CE_RO_V1 import \
    ExtendedTallySheet_PE_CE_RO_V1
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.ExtendedTallySheet.ExtendedTallySheet_PE_CE_RO_V2 import \
    ExtendedTallySheet_PE_CE_RO_V2
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.ExtendedTallySheet.ExtendedTallySheet_PE_R2 import \
    ExtendedTallySheet_PE_R2
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.META_DATA_KEY import \
    META_DATA_KEY_ELECTION_NUMBER_OF_SEATS_ALLOCATED, \
    META_DATA_KEY_ELECTION_NUMBER_OF_VALID_VOTE_PERCENTAGE_REQUIRED_FOR_SEAT_ALLOCATION
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.TALLY_SHEET_CODES import PE_27, PE_4, PE_CE_RO_V1, \
    PE_CE_RO_PR_1, \
    PE_CE_RO_V2, PE_R2, PE_CE_RO_PR_2, PE_CE_RO_PR_3, CE_201, CE_201_PV, PE_39, PE_22, PE_21, POLLING_DIVISION_RESULTS, \
    ALL_ISLAND_RESULT
from constants.VOTE_TYPES import Postal, NonPostal, PostalAndNonPostal
from ext.ExtendedElection import ExtendedElection
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020 import RoleBasedAccess
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.TEMPLATE_ROW_TYPE import \
    TEMPLATE_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_1, TEMPLATE_ROW_TYPE_VALID_VOTES_REMAIN_FROM_ROUND_1, \
    TEMPLATE_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_2, TEMPLATE_ROW_TYPE_BONUS_SEATS_ALLOCATED, \
    TEMPLATE_ROW_TYPE_VALID_VOTE_COUNT_CEIL_PER_SEAT, \
    TEMPLATE_ROW_TYPE_MINIMUM_VALID_VOTE_COUNT_REQUIRED_FOR_SEAT_ALLOCATION, TEMPLATE_ROW_TYPE_SEATS_ALLOCATED, \
    TEMPLATE_ROW_TYPE_ELECTED_CANDIDATE
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.WORKFLOW_ACTION_TYPE import \
    WORKFLOW_ACTION_TYPE_VIEW, \
    WORKFLOW_ACTION_TYPE_SAVE, WORKFLOW_ACTION_TYPE_SUBMIT, WORKFLOW_ACTION_TYPE_REQUEST_CHANGES, \
    WORKFLOW_ACTION_TYPE_VERIFY, WORKFLOW_ACTION_TYPE_EDIT, \
    WORKFLOW_ACTION_TYPE_MOVE_TO_CERTIFY, WORKFLOW_ACTION_TYPE_CERTIFY, WORKFLOW_ACTION_TYPE_RELEASE, \
    WORKFLOW_ACTION_TYPE_PRINT
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.WORKFLOW_STATUS_TYPE import \
    WORKFLOW_STATUS_TYPE_EMPTY, \
    WORKFLOW_STATUS_TYPE_SAVED, WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED, WORKFLOW_STATUS_TYPE_SUBMITTED, \
    WORKFLOW_STATUS_TYPE_VERIFIED, WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY, \
    WORKFLOW_STATUS_TYPE_CERTIFIED, WORKFLOW_STATUS_TYPE_RELEASED
from ext.ExtendedElection.util import get_rows_from_csv, update_dashboard_tables
from orm.entities import Candidate, Template, Party, Meta, Workflow
from orm.entities.Area import AreaMap
from orm.entities.Area.Electorate import Country, ElectoralDistrict, PollingDivision, PollingDistrict
from orm.entities.Area.Office import PollingStation, CountingCentre, DistrictCentre, ElectionCommission
from orm.entities.Submission import TallySheet
from orm.enums import AreaTypeEnum

role_based_access_config = RoleBasedAccess.role_based_access_config


class ExtendedElectionParliamentaryElection2020(ExtendedElection):
    def __init__(self, election):
        super(ExtendedElectionParliamentaryElection2020, self).__init__(
            election=election,
            role_based_access_config=role_based_access_config
        )

    def get_extended_tally_sheet_class(self, templateName):
        EXTENDED_TEMPLATE_MAP = {
            PE_CE_RO_V1: ExtendedTallySheet_PE_CE_RO_V1,
            PE_R2: ExtendedTallySheet_PE_R2,
            PE_CE_RO_V2: ExtendedTallySheet_PE_CE_RO_V2,
            PE_27: ExtendedTallySheet_PE_27,
            PE_4: ExtendedTallySheet_PE_4,
            CE_201: ExtendedTallySheet_CE_201,
            PE_39: ExtendedTallySheet_PE_39,
            PE_22: ExtendedTallySheet_PE_22,
            PE_CE_RO_PR_1: ExtendedTallySheet_PE_CE_RO_PR_1,
            PE_CE_RO_PR_2: ExtendedTallySheet_PE_CE_RO_PR_2,
            PE_CE_RO_PR_3: ExtendedTallySheet_PE_CE_RO_PR_3,
            PE_21: ExtendedTallySheet_PE_21,
            POLLING_DIVISION_RESULTS: ExtendedTallySheet_POLLING_DIVISION_RESULTS,
            ALL_ISLAND_RESULT: ExtendedTallySheet_ALL_ISLAND_RESULT
        }

        if templateName in EXTENDED_TEMPLATE_MAP:
            return EXTENDED_TEMPLATE_MAP[templateName]
        else:
            return super(ExtendedElectionParliamentaryElection2020, self).get_extended_tally_sheet_class(
                templateName=templateName
            )

    def build_election(self, party_candidate_dataset_file=None,
                       polling_station_dataset_file=None, postal_counting_centers_dataset_file=None,
                       invalid_vote_categories_dataset_file=None, number_of_seats_dataset_file=None):
        root_election = self.election

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

        if not party_candidate_dataset_file:
            party_candidate_dataset_file = root_election.partyCandidateDataset.fileContent

        if not polling_station_dataset_file:
            polling_station_dataset_file = root_election.pollingStationsDataset.fileContent

        if not number_of_seats_dataset_file:
            number_of_seats_dataset_file = root_election.numberOfSeatsDataset.fileContent

        if not invalid_vote_categories_dataset_file:
            invalid_vote_categories_dataset_file = root_election.invalidVoteCategoriesDataset.fileContent

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

        tally_sheet_template_pe_27 = Template.create(
            templateName=PE_27
        )
        tally_sheet_template_pe_27_party_wise_vote_row = tally_sheet_template_pe_27.add_row(
            templateRowType="PARTY_WISE_VOTE",
            hasMany=True,
            isDerived=False,
            columns=[
                {"columnName": "electionId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "areaId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "partyId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT},
                {"columnName": "numValue", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT},
                {"columnName": "strValue", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT}
            ]
        )
        tally_sheet_template_pe_27_rejected_vote_row = tally_sheet_template_pe_27.add_row(
            templateRowType="REJECTED_VOTE",
            hasMany=False,
            isDerived=False,
            columns=[
                {"columnName": "electionId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "areaId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "numValue", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT}
            ]
        )

        tally_sheet_template_pe_39 = Template.create(
            templateName=PE_39
        )
        tally_sheet_template_pe_39_ground_of_rejection_wise_row = tally_sheet_template_pe_39.add_row(
            templateRowType="NUMBER_OF_VOTES_REJECTED_AGAINST_GROUNDS_FOR_REJECTION",
            hasMany=True,
            isDerived=False,
            columns=[
                {"columnName": "electionId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "areaId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "invalidVoteCategoryId", "grouped": False, "func": None,
                 "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT},
                {"columnName": "numValue", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT}
            ]
        )

        tally_sheet_template_pe_22 = Template.create(
            templateName=PE_22
        )
        tally_sheet_template_pe_22_party_and_invalid_vote_category_wise_vote_count_row = tally_sheet_template_pe_22.add_row(
            templateRowType="PARTY_WISE_INVALID_VOTE_COUNT",
            hasMany=True,
            isDerived=False,
            columns=[
                {"columnName": "electionId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "areaId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "partyId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT},
                {"columnName": "invalidVoteCategoryId", "grouped": False, "func": None,
                 "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT},
                {"columnName": "numValue", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT}
            ]
        )

        tally_sheet_template_pe_ce_ro_v1 = Template.create(
            templateName=PE_CE_RO_V1
        )
        tally_sheet_template_pe_ce_ro_v1_party_wise_vote_row = tally_sheet_template_pe_ce_ro_v1.add_row(
            templateRowType="PARTY_WISE_VOTE",
            hasMany=True,
            isDerived=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "areaId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "partyId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "numValue", "grouped": False, "func": "sum", "source": TALLY_SHEET_COLUMN_SOURCE_QUERY}
            ]
        ).add_derivative_template_row(tally_sheet_template_pe_27_party_wise_vote_row)
        tally_sheet_template_pe_ce_ro_v1_rejected_vote_row = tally_sheet_template_pe_ce_ro_v1.add_row(
            templateRowType="REJECTED_VOTE",
            hasMany=True,
            isDerived=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "areaId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "numValue", "grouped": False, "func": "sum", "source": TALLY_SHEET_COLUMN_SOURCE_QUERY}
            ]
        ).add_derivative_template_row(tally_sheet_template_pe_27_rejected_vote_row)

        tally_sheet_template_polling_division_results = Template.create(
            templateName=POLLING_DIVISION_RESULTS
        )
        tally_sheet_template_polling_division_results_party_wise_vote_row = tally_sheet_template_polling_division_results.add_row(
            templateRowType="PARTY_WISE_VOTE",
            hasMany=True,
            isDerived=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "areaId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "partyId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "numValue", "grouped": False, "func": "sum", "source": TALLY_SHEET_COLUMN_SOURCE_QUERY}
            ]
        ).add_derivative_template_row(tally_sheet_template_pe_ce_ro_v1_party_wise_vote_row)
        tally_sheet_template_polling_division_results_rejected_vote_row = tally_sheet_template_polling_division_results.add_row(
            templateRowType="REJECTED_VOTE",
            hasMany=True,
            isDerived=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "areaId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "numValue", "grouped": False, "func": "sum", "source": TALLY_SHEET_COLUMN_SOURCE_QUERY}
            ]
        ).add_derivative_template_row(tally_sheet_template_pe_ce_ro_v1_rejected_vote_row)

        tally_sheet_template_pe_ce_ro_v2 = Template.create(
            templateName=PE_CE_RO_V2
        )
        tally_sheet_template_pe_ce_ro_v2_party_wise_vote_row = tally_sheet_template_pe_ce_ro_v2.add_row(
            templateRowType="PARTY_WISE_VOTE",
            hasMany=True,
            isDerived=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "areaId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "partyId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "numValue", "grouped": False, "func": "sum", "source": TALLY_SHEET_COLUMN_SOURCE_QUERY}
            ]
        ).add_derivative_template_row(tally_sheet_template_pe_ce_ro_v1_party_wise_vote_row)
        tally_sheet_template_pe_ce_ro_v2_rejected_vote_row = tally_sheet_template_pe_ce_ro_v2.add_row(
            templateRowType="REJECTED_VOTE",
            hasMany=True,
            isDerived=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "areaId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "numValue", "grouped": False, "func": "sum", "source": TALLY_SHEET_COLUMN_SOURCE_QUERY}
            ]
        ).add_derivative_template_row(tally_sheet_template_pe_ce_ro_v1_rejected_vote_row)

        tally_sheet_template_all_island_result = Template.create(
            templateName=ALL_ISLAND_RESULT
        )
        tally_sheet_template_all_island_result_party_wise_vote_row = tally_sheet_template_all_island_result.add_row(
            templateRowType="PARTY_WISE_VOTE",
            hasMany=True,
            isDerived=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "areaId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "partyId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "numValue", "grouped": False, "func": "sum", "source": TALLY_SHEET_COLUMN_SOURCE_QUERY}
            ]
        ).add_derivative_template_row(tally_sheet_template_pe_ce_ro_v2_party_wise_vote_row)
        tally_sheet_template_all_island_result_rejected_vote_row = tally_sheet_template_all_island_result.add_row(
            templateRowType="REJECTED_VOTE",
            hasMany=True,
            isDerived=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "areaId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "numValue", "grouped": False, "func": "sum", "source": TALLY_SHEET_COLUMN_SOURCE_QUERY}
            ]
        ).add_derivative_template_row(tally_sheet_template_pe_ce_ro_v2_rejected_vote_row)

        tally_sheet_template_pe_r2 = Template.create(
            templateName=PE_R2
        )
        tally_sheet_template_pe_r2_party_wise_vote_row = tally_sheet_template_pe_r2.add_row(
            templateRowType="PARTY_WISE_VOTE",
            hasMany=True,
            isDerived=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "areaId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "partyId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "numValue", "grouped": False, "func": "sum", "source": TALLY_SHEET_COLUMN_SOURCE_QUERY}
            ]
        ).add_derivative_template_row(tally_sheet_template_pe_ce_ro_v2_party_wise_vote_row)
        tally_sheet_template_pe_r2_rejected_vote_row = tally_sheet_template_pe_r2.add_row(
            templateRowType="REJECTED_VOTE",
            hasMany=True,
            isDerived=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "areaId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_QUERY},
                {"columnName": "numValue", "grouped": False, "func": "sum", "source": TALLY_SHEET_COLUMN_SOURCE_QUERY}
            ]
        ).add_derivative_template_row(tally_sheet_template_pe_ce_ro_v2_rejected_vote_row)
        tally_sheet_template_pe_r2_valid_vote_count_ceil_per_seat = tally_sheet_template_pe_r2.add_row(
            templateRowType=TEMPLATE_ROW_TYPE_VALID_VOTE_COUNT_CEIL_PER_SEAT,
            hasMany=True,
            isDerived=True,
            loadOnPostSave=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "areaId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "numValue", "grouped": False, "func": "sum", "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT}
            ]
        )
        tally_sheet_template_pe_r2_valid_vote_count_qualified_for_seat_allocation = tally_sheet_template_pe_r2.add_row(
            templateRowType=TEMPLATE_ROW_TYPE_MINIMUM_VALID_VOTE_COUNT_REQUIRED_FOR_SEAT_ALLOCATION,
            hasMany=True,
            isDerived=True,
            loadOnPostSave=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "areaId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "numValue", "grouped": False, "func": "sum", "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT}
            ]
        )
        tally_sheet_template_pe_r2_seats_allocated_from_round_1_row = tally_sheet_template_pe_r2.add_row(
            templateRowType=TEMPLATE_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_1,
            hasMany=True,
            isDerived=True,
            loadOnPostSave=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "areaId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "partyId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT},
                {"columnName": "numValue", "grouped": False, "func": "sum", "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT}
            ]
        )
        tally_sheet_template_pe_r2_valid_votes_remain_from_round_1_row = tally_sheet_template_pe_r2.add_row(
            templateRowType=TEMPLATE_ROW_TYPE_VALID_VOTES_REMAIN_FROM_ROUND_1,
            hasMany=True,
            isDerived=True,
            loadOnPostSave=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "areaId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "partyId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT},
                {"columnName": "numValue", "grouped": False, "func": "sum", "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT}
            ]
        )
        tally_sheet_template_pe_r2_seats_allocated_from_round_2_row = tally_sheet_template_pe_r2.add_row(
            templateRowType=TEMPLATE_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_2,
            hasMany=True,
            isDerived=True,
            loadOnPostSave=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "areaId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "partyId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT},
                {"columnName": "numValue", "grouped": False, "func": "sum", "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT}
            ]
        )
        tally_sheet_template_pe_r2_bonus_seats_allocated = tally_sheet_template_pe_r2.add_row(
            templateRowType=TEMPLATE_ROW_TYPE_BONUS_SEATS_ALLOCATED,
            hasMany=True,
            isDerived=True,
            loadOnPostSave=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "areaId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "partyId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT},
                {"columnName": "numValue", "grouped": False, "func": "sum", "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT}
            ]
        )

        tally_sheet_template_pe_4 = Template.create(
            templateName=PE_4
        )
        tally_sheet_template_pe_4_candidate_wise_first_preference_row = tally_sheet_template_pe_4.add_row(
            templateRowType="CANDIDATE_FIRST_PREFERENCE",
            hasMany=True,
            isDerived=False,
            columns=[
                {"columnName": "electionId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "areaId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "partyId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "candidateId", "grouped": False, "func": None,
                 "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT},
                {"columnName": "numValue", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT}
            ]
        )

        tally_sheet_template_pe_ce_ro_pr_1 = Template.create(
            templateName=PE_CE_RO_PR_1
        )
        tally_sheet_template_pe_ce_ro_pr_1_candidate_wise_first_preference_row = tally_sheet_template_pe_ce_ro_pr_1.add_row(
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
        ).add_derivative_template_row(tally_sheet_template_pe_4_candidate_wise_first_preference_row)

        tally_sheet_template_pe_ce_ro_pr_2 = Template.create(
            templateName=PE_CE_RO_PR_2
        )
        tally_sheet_template_pe_ce_ro_pr_2_candidate_wise_first_preference_row = tally_sheet_template_pe_ce_ro_pr_2.add_row(
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
        ).add_derivative_template_row(tally_sheet_template_pe_ce_ro_pr_1_candidate_wise_first_preference_row)

        tally_sheet_template_pe_ce_ro_pr_3 = Template.create(
            templateName=PE_CE_RO_PR_3
        )
        tally_sheet_template_pe_ce_ro_pr_3_candidate_wise_first_preference_row = tally_sheet_template_pe_ce_ro_pr_3.add_row(
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
        ).add_derivative_template_row(tally_sheet_template_pe_ce_ro_pr_2_candidate_wise_first_preference_row)

        tally_sheet_template_pe_21 = Template.create(
            templateName=PE_21
        )
        tally_sheet_template_pe_21_elected_candidates = tally_sheet_template_pe_21.add_row(
            templateRowType=TEMPLATE_ROW_TYPE_ELECTED_CANDIDATE,
            hasMany=True,
            isDerived=True,
            loadOnPostSave=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "areaId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "partyId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT},
                {"columnName": "candidateId", "grouped": True, "func": None,
                 "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT}
            ]
        )
        tally_sheet_template_pe_21_candidate_wise_first_preference_row = tally_sheet_template_pe_21.add_row(
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
        ).add_derivative_template_row(tally_sheet_template_pe_ce_ro_pr_3_candidate_wise_first_preference_row)
        tally_sheet_template_pe_21_party_wise_seat_allocation = tally_sheet_template_pe_21.add_row(
            templateRowType=TEMPLATE_ROW_TYPE_SEATS_ALLOCATED,
            hasMany=True,
            isDerived=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "areaId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "partyId", "grouped": True, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT},
                {"columnName": "numValue", "grouped": False, "func": "sum", "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT}
            ]
        ).add_derivative_template_row(
            tally_sheet_template_pe_r2_seats_allocated_from_round_1_row
        ).add_derivative_template_row(
            tally_sheet_template_pe_r2_seats_allocated_from_round_2_row
        ).add_derivative_template_row(
            tally_sheet_template_pe_r2_bonus_seats_allocated
        )

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

        electoral_district_election_store = {}
        party_store = {}

        def _get_candidate(row):
            election, postal_election, ordinary_election = _get_electoral_district_election(row)

            party = _get_party(row)

            candidate = Candidate.create(candidateName=row["Candidate Name"], candidateNumber=row["Candidate Number"])

            root_election.add_candidate(candidateId=candidate.candidateId, partyId=party.partyId)
            election.add_candidate(candidateId=candidate.candidateId, partyId=party.partyId)
            postal_election.add_candidate(candidateId=candidate.candidateId, partyId=party.partyId)
            ordinary_election.add_candidate(candidateId=candidate.candidateId, partyId=party.partyId)

            return candidate

        def _get_party(row):
            election, postal_election, ordinary_election = _get_electoral_district_election(row)

            party_name = row["Party Name (Unique)"]
            party_name_unique = row["Party Name (Unique)"]
            party_symbol = row["Party Symbol (Text)"]
            party_abbreviation = row["Party Abbreviation"]

            if party_name_unique not in party_store:
                party = Party.create(
                    partyName=party_name,
                    partySymbol=party_symbol,
                    partyAbbreviation=party_abbreviation
                )

                party_store[party_name_unique] = party

            party = party_store[party_name_unique]

            root_election.add_party(partyId=party.partyId)
            election.add_party(partyId=party.partyId)
            postal_election.add_party(partyId=party.partyId)
            ordinary_election.add_party(partyId=party.partyId)

            return party_store[party_name_unique]

        def _get_electoral_district_election(row):
            electoral_district_name = row["Electoral District"]

            if electoral_district_name not in electoral_district_election_store:
                election = root_election.add_sub_election(
                    electionName="%s - %s" % (root_election.electionName, electoral_district_name),
                    voteType=PostalAndNonPostal, isListed=True
                )
                postal_election = election.add_sub_election(
                    electionName="%s - %s - Postal" % (root_election.electionName, electoral_district_name),
                    voteType=Postal
                )
                ordinary_election = election.add_sub_election(
                    electionName="%s - %s - Ordinary" % (root_election.electionName, electoral_district_name),
                    voteType=NonPostal
                )

                electoral_district_election_store[electoral_district_name] = [election, postal_election,
                                                                              ordinary_election]

            election_list = electoral_district_election_store[electoral_district_name]

            return election_list[0], election_list[1], election_list[2]

        def _get_area_entry(election, area_class, area_name, area_key, create_tally_sheets_callback=None):

            area_type = area_class.Model.__mapper_args__["polymorphic_identity"]

            if area_key in data_entry_store[area_type]:
                area = data_entry_store[area_type][area_key]
            else:
                area = area_class.create(area_name, electionId=election.electionId)

                data_entry_store[area_type][area_key] = area

                if create_tally_sheets_callback is not None:
                    tally_sheet_mappings = create_tally_sheets_callback(area)

                    for tally_sheet_mapping_key in tally_sheet_mappings.keys():
                        tally_sheet_mapping_value = tally_sheet_mappings[tally_sheet_mapping_key]
                        setattr(area, tally_sheet_mapping_key, tally_sheet_mapping_value)

            return area

        def _get_country_entry(row):
            area_class = Country
            area_name = row["Country"]
            area_key = area_name

            def _create_country_tally_sheets(area):
                all_island_results_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_all_island_result, electionId=root_election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": root_election.electionId
                    }).metaId,
                    workflowInstanceId=workflow_released_report.get_new_instance().workflowInstanceId
                )]
                return {
                    "all_island_results_tally_sheet_list": all_island_results_tally_sheet_list
                }

            data_entry_obj = _get_area_entry(root_election, area_class, area_name, area_key,
                                             _create_country_tally_sheets)

            return data_entry_obj

        def _get_electoral_district_entry(row):
            election, postal_election, ordinary_election = _get_electoral_district_election(row)

            country = _get_country_entry(row)

            area_class = ElectoralDistrict
            area_name = row["Electoral District"]
            area_key = area_name

            def _create_electoral_district_tally_sheets(area):
                all_island_results_tally_sheet_list = country.all_island_results_tally_sheet_list

                pe_21_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_pe_21, electionId=election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": election.electionId
                    }).metaId,
                    workflowInstanceId=workflow_released_report.get_new_instance().workflowInstanceId
                )]

                pe_r2_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_pe_r2, electionId=election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": election.electionId
                    }).metaId,
                    parentTallySheets=pe_21_tally_sheet_list,
                    workflowInstanceId=workflow_released_report.get_new_instance().workflowInstanceId
                )]

                pe_ce_ro_v2_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_pe_ce_ro_v2, electionId=election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": election.electionId
                    }).metaId,
                    parentTallySheets=[*pe_r2_tally_sheet_list, *all_island_results_tally_sheet_list],
                    workflowInstanceId=workflow_report.get_new_instance().workflowInstanceId
                )]

                polling_division_results_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_polling_division_results, electionId=postal_election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": postal_election.electionId
                    }).metaId,
                    workflowInstanceId=workflow_report.get_new_instance().workflowInstanceId
                )]
                pe_ce_ro_v1_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_pe_ce_ro_v1, electionId=postal_election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": postal_election.electionId
                    }).metaId,
                    parentTallySheets=[*polling_division_results_tally_sheet_list],
                    workflowInstanceId=workflow_released_report.get_new_instance().workflowInstanceId
                )]

                pe_ce_ro_pr_1_tally_sheet_list = []
                pe_ce_ro_pr_1_tally_sheet_party_id_wise_map = {}
                pe_ce_ro_pr_2_tally_sheet_list = []
                pe_ce_ro_pr_2_tally_sheet_party_id_wise_map = {}
                pe_ce_ro_pr_3_tally_sheet_list = []
                pe_ce_ro_pr_3_tally_sheet_party_id_wise_map = {}
                for party in election.parties:
                    pe_ce_ro_pr_3_tally_sheet = TallySheet.create(
                        template=tally_sheet_template_pe_ce_ro_pr_3, electionId=election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "partyId": party.partyId,
                            "electionId": election.electionId
                        }).metaId,
                        parentTallySheets=pe_21_tally_sheet_list,
                        workflowInstanceId=workflow_report.get_new_instance().workflowInstanceId
                    )
                    pe_ce_ro_pr_3_tally_sheet_list.append(pe_ce_ro_pr_3_tally_sheet)
                    pe_ce_ro_pr_3_tally_sheet_party_id_wise_map[party.partyId] = pe_ce_ro_pr_3_tally_sheet

                    pe_ce_ro_pr_2_tally_sheet = TallySheet.create(
                        template=tally_sheet_template_pe_ce_ro_pr_2, electionId=election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "partyId": party.partyId,
                            "electionId": election.electionId
                        }).metaId,
                        parentTallySheets=[pe_ce_ro_pr_3_tally_sheet],
                        workflowInstanceId=workflow_report.get_new_instance().workflowInstanceId
                    )
                    pe_ce_ro_pr_2_tally_sheet_list.append(pe_ce_ro_pr_2_tally_sheet)
                    pe_ce_ro_pr_2_tally_sheet_party_id_wise_map[party.partyId] = pe_ce_ro_pr_2_tally_sheet

                    pe_ce_ro_pr_1_tally_sheet = TallySheet.create(
                        template=tally_sheet_template_pe_ce_ro_pr_1, electionId=postal_election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "partyId": party.partyId,
                            "electionId": postal_election.electionId
                        }).metaId,
                        parentTallySheets=[pe_ce_ro_pr_2_tally_sheet],
                        workflowInstanceId=workflow_report.get_new_instance().workflowInstanceId
                    )
                    pe_ce_ro_pr_1_tally_sheet_list.append(pe_ce_ro_pr_1_tally_sheet)
                    pe_ce_ro_pr_1_tally_sheet_party_id_wise_map[party.partyId] = pe_ce_ro_pr_1_tally_sheet

                return {
                    "pe_ce_ro_v1_tally_sheet_list": pe_ce_ro_v1_tally_sheet_list,
                    "polling_division_results_tally_sheet_list": polling_division_results_tally_sheet_list,
                    "pe_r2_tally_sheet_list": pe_r2_tally_sheet_list,
                    "pe_ce_ro_v2_tally_sheet_list": pe_ce_ro_v2_tally_sheet_list,
                    "pe_ce_ro_pr_1_tally_sheet_list": pe_ce_ro_pr_1_tally_sheet_list,
                    "pe_ce_ro_pr_1_tally_sheet_party_id_wise_map": pe_ce_ro_pr_1_tally_sheet_party_id_wise_map,
                    "pe_ce_ro_pr_2_tally_sheet_list": pe_ce_ro_pr_2_tally_sheet_list,
                    "pe_ce_ro_pr_2_tally_sheet_party_id_wise_map": pe_ce_ro_pr_2_tally_sheet_party_id_wise_map,
                    "pe_ce_ro_pr_3_tally_sheet_list": pe_ce_ro_pr_3_tally_sheet_list,
                    "pe_ce_ro_pr_3_tally_sheet_party_id_wise_map": pe_ce_ro_pr_3_tally_sheet_party_id_wise_map
                }

            data_entry_obj = _get_area_entry(election, area_class, area_name, area_key,
                                             _create_electoral_district_tally_sheets)

            return data_entry_obj

        def _get_polling_division_entry(row):
            election, postal_election, ordinary_election = _get_electoral_district_election(row)

            electoral_district = _get_electoral_district_entry(row)

            area_class = PollingDivision
            area_name = row["Polling Division"]
            area_key = area_name

            def _create_polling_division_tally_sheets(area):
                pe_ce_ro_pr_2_tally_sheet_party_id_wise_map = electoral_district.pe_ce_ro_pr_2_tally_sheet_party_id_wise_map
                pe_ce_ro_v2_tally_sheet_list = electoral_district.pe_ce_ro_v2_tally_sheet_list

                polling_division_results_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_polling_division_results, electionId=ordinary_election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": ordinary_election.electionId
                    }).metaId,
                    workflowInstanceId=workflow_report.get_new_instance().workflowInstanceId
                )]

                pe_ce_ro_v1_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_pe_ce_ro_v1, electionId=ordinary_election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": ordinary_election.electionId
                    }).metaId,
                    parentTallySheets=[*polling_division_results_tally_sheet_list],
                    workflowInstanceId=workflow_report.get_new_instance().workflowInstanceId
                )]

                pe_ce_ro_pr_1_tally_sheet_list = []
                pe_ce_ro_pr_1_tally_sheet_party_id_wise_map = {}
                for party in election.parties:
                    pe_ce_ro_pr_1_tally_sheet = TallySheet.create(
                        template=tally_sheet_template_pe_ce_ro_pr_1, electionId=ordinary_election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "partyId": party.partyId,
                            "electionId": ordinary_election.electionId
                        }).metaId,
                        parentTallySheets=[pe_ce_ro_pr_2_tally_sheet_party_id_wise_map[party.partyId]],
                        workflowInstanceId=workflow_report.get_new_instance().workflowInstanceId
                    )
                    pe_ce_ro_pr_1_tally_sheet_list.append(pe_ce_ro_pr_1_tally_sheet)
                    pe_ce_ro_pr_1_tally_sheet_party_id_wise_map[party.partyId] = pe_ce_ro_pr_1_tally_sheet

                return {
                    "pe_ce_ro_v1_tally_sheet_list": pe_ce_ro_v1_tally_sheet_list,
                    "pe_ce_ro_pr_1_tally_sheet_list": pe_ce_ro_pr_1_tally_sheet_list,
                    "pe_ce_ro_pr_1_tally_sheet_party_id_wise_map": pe_ce_ro_pr_1_tally_sheet_party_id_wise_map,
                    "polling_division_results_tally_sheet_list": polling_division_results_tally_sheet_list,
                }

            data_entry_obj = _get_area_entry(election, area_class, area_name, area_key,
                                             _create_polling_division_tally_sheets)

            return data_entry_obj

        def _get_polling_district_entry(row):
            election, postal_election, ordinary_election = _get_electoral_district_election(row)

            electoral_district = _get_electoral_district_entry(row)
            polling_division = _get_polling_division_entry(row)

            area_class = PollingDistrict
            area_name = row["Polling District"]
            area_key = "%s-%s-%s" % (electoral_district.areaName, polling_division.areaName, area_name)

            data_entry_obj = _get_area_entry(election, area_class, area_name, area_key)

            return data_entry_obj

        def _get_polling_station_entry(row):
            election, postal_election, ordinary_election = _get_electoral_district_election(row)

            electoral_district = _get_electoral_district_entry(row)
            polling_division = _get_polling_division_entry(row)
            polling_district = _get_polling_district_entry(row)

            area_class = PollingStation
            area_name = row["Polling Station"]
            area_key = "%s-%s-%s-%s" % (
                electoral_district.areaName, polling_division.areaName, polling_district.areaName, area_name
            )

            area = _get_area_entry(election, area_class, area_name, area_key)

            area._registeredVotersCount = row["Registered Normal Voters"]
            area._registeredPostalVotersCount = row["Registered Postal Voters"]

            return area

        def _get_counting_centre_entry(row):
            election, postal_election, ordinary_election = _get_electoral_district_election(row)

            electoral_district = _get_electoral_district_entry(row)
            polling_division = _get_polling_division_entry(row)

            area_class = CountingCentre
            area_name = row["Counting Centre"]
            area_key = "%s-%s" % (electoral_district.areaName, area_name)

            def _create_counting_centre_tally_sheets(area):
                pe_ce_ro_v1_tally_sheet_list = polling_division.pe_ce_ro_v1_tally_sheet_list
                pe_ce_ro_pr_1_tally_sheets_list = polling_division.pe_ce_ro_pr_1_tally_sheet_list

                pe_27_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_pe_27, electionId=ordinary_election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": ordinary_election.electionId
                    }).metaId,
                    parentTallySheets=pe_ce_ro_v1_tally_sheet_list,
                    workflowInstanceId=workflow_data_entry.get_new_instance().workflowInstanceId
                )]

                pe_39_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_pe_39, electionId=ordinary_election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": ordinary_election.electionId
                    }).metaId,
                    workflowInstanceId=workflow_data_entry.get_new_instance().workflowInstanceId
                )]
                pe_22_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_pe_22, electionId=ordinary_election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": ordinary_election.electionId
                    }).metaId,
                    workflowInstanceId=workflow_data_entry.get_new_instance().workflowInstanceId
                )]

                pe_4_tally_sheet_list = []
                pe_4_tally_sheet_party_id_wise_map = {}
                for party in election.parties:
                    pe_4_tally_sheet = TallySheet.create(
                        template=tally_sheet_template_pe_4, electionId=ordinary_election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "partyId": party.partyId,
                            "electionId": ordinary_election.electionId
                        }).metaId,
                        parentTallySheets=pe_ce_ro_pr_1_tally_sheets_list,
                        workflowInstanceId=workflow_data_entry.get_new_instance().workflowInstanceId
                    )
                    pe_4_tally_sheet_list.append(pe_4_tally_sheet)
                    pe_4_tally_sheet_party_id_wise_map[party.partyId] = pe_4_tally_sheet

                pe_ce_201_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_ce_201, electionId=ordinary_election.electionId, areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": ordinary_election.electionId
                    }).metaId,
                    workflowInstanceId=workflow_data_entry.get_new_instance().workflowInstanceId
                )]

                return {
                    "pe_27_tally_sheet_list": pe_27_tally_sheet_list,
                    "pe_39_tally_sheet_list": pe_39_tally_sheet_list,
                    "pe_22_tally_sheet_list": pe_22_tally_sheet_list,
                    "pe_4_tally_sheet_list": pe_4_tally_sheet_list,
                    "pe_4_tally_sheet_party_id_wise_map": pe_4_tally_sheet_party_id_wise_map,
                    "pe_ce_201_tally_sheet_list": pe_ce_201_tally_sheet_list
                }

            data_entry_obj = _get_area_entry(ordinary_election, area_class, area_name, area_key,
                                             _create_counting_centre_tally_sheets)

            return data_entry_obj

        def _get_postal_vote_counting_centre_entry(row):
            election, postal_election, ordinary_election = _get_electoral_district_election(row)

            electoral_district = _get_electoral_district_entry(row=row)

            area_class = CountingCentre
            area_name = row["Postal Vote Counting Centre"]
            area_key = "%s-%s" % (electoral_district.areaName, area_name)

            def _create_counting_centre_tally_sheets(area):
                pe_ce_ro_v1_tally_sheet_list = electoral_district.pe_ce_ro_v1_tally_sheet_list
                pe_ce_ro_pr_1_tally_sheet_list = electoral_district.pe_ce_ro_pr_1_tally_sheet_list

                pe_27_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_pe_27, electionId=postal_election.electionId, areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": postal_election.electionId
                    }).metaId,
                    parentTallySheets=pe_ce_ro_v1_tally_sheet_list,
                    workflowInstanceId=workflow_data_entry.get_new_instance().workflowInstanceId
                )]

                pe_39_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_pe_39, electionId=postal_election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": postal_election.electionId
                    }).metaId,
                    workflowInstanceId=workflow_data_entry.get_new_instance().workflowInstanceId
                )]

                pe_22_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_pe_22, electionId=postal_election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": postal_election.electionId
                    }).metaId,
                    workflowInstanceId=workflow_data_entry.get_new_instance().workflowInstanceId
                )]

                pe_4_tally_sheet_list = []
                pe_4_tally_sheet_party_id_wise_map = {}
                for party in postal_election.parties:
                    pe_4_tally_sheet = TallySheet.create(
                        template=tally_sheet_template_pe_4, electionId=postal_election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "partyId": party.partyId,
                            "electionId": postal_election.electionId
                        }).metaId,
                        parentTallySheets=pe_ce_ro_pr_1_tally_sheet_list,
                        workflowInstanceId=workflow_data_entry.get_new_instance().workflowInstanceId
                    )
                    pe_4_tally_sheet_list.append(pe_4_tally_sheet)
                    pe_4_tally_sheet_party_id_wise_map[party.partyId] = pe_4_tally_sheet

                pe_ce_201_pv_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_ce_201_pv, electionId=postal_election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": postal_election.electionId
                    }).metaId,
                    workflowInstanceId=workflow_data_entry.get_new_instance().workflowInstanceId
                )]

                return {
                    "pe_27_tally_sheet_list": pe_27_tally_sheet_list,
                    "pe_39_tally_sheet_list": pe_39_tally_sheet_list,
                    "pe_22_tally_sheet_list": pe_22_tally_sheet_list,
                    "pe_4_tally_sheet_list": pe_4_tally_sheet_list,
                    "pe_4_tally_sheet_party_id_wise_map": pe_4_tally_sheet_party_id_wise_map,
                    "pe_ce_201_pv_tally_sheet_list": pe_ce_201_pv_tally_sheet_list
                }

            data_entry_obj = _get_area_entry(postal_election, area_class, area_name, area_key,
                                             _create_counting_centre_tally_sheets)

            return data_entry_obj

        def _get_district_centre_entry(row):
            election, postal_election, ordinary_election = _get_electoral_district_election(row)

            area_class = DistrictCentre
            area_name = row["District Centre"]
            area_key = area_name

            data_entry_obj = _get_area_entry(election, area_class, area_name, area_key)

            return data_entry_obj

        def _get_election_commission_entry(row):
            election, postal_election, ordinary_election = _get_electoral_district_election(row)

            area_class = ElectionCommission
            area_name = row["Election Commission"]
            area_key = area_name

            data_entry_obj = _get_area_entry(election, area_class, area_name, area_key)

            return data_entry_obj

        for row in get_rows_from_csv(party_candidate_dataset_file):
            _get_candidate(row)

        for row in get_rows_from_csv(invalid_vote_categories_dataset_file):
            if "Invalid Vote Category Type" in row.keys():
                root_election.add_invalid_vote_category(row["Invalid Vote Category Description"],
                                                        row["Invalid Vote Category Type"])
            else:
                root_election.add_invalid_vote_category(row["Invalid Vote Category Description"])

        for row in get_rows_from_csv(polling_station_dataset_file):
            row["Country"] = "Sri Lanka"
            row["Election Commission"] = "Sri Lanka Election Commission"
            row["Polling Station"] = row["Polling Station (English)"]

            country = _get_country_entry(row=row)

            electoral_district = _get_electoral_district_entry(row=row)
            polling_division = _get_polling_division_entry(row=row)
            polling_district = _get_polling_district_entry(row=row)
            election_commission = _get_election_commission_entry(row=row)
            district_centre = _get_district_centre_entry(row=row)
            counting_centre = _get_counting_centre_entry(row=row)
            postal_vote_counting_centre = _get_postal_vote_counting_centre_entry(row=row)
            polling_station = _get_polling_station_entry(row=row)

            country.add_child(electoral_district.areaId)
            electoral_district.add_child(polling_division.areaId)
            polling_division.add_child(polling_district.areaId)
            polling_district.add_child(polling_station.areaId)
            election_commission.add_child(district_centre.areaId)

            district_centre.add_child(counting_centre.areaId)
            counting_centre.add_child(polling_station.areaId)

            district_centre.add_child(postal_vote_counting_centre.areaId)
            postal_vote_counting_centre.add_child(polling_station.areaId)

            AreaMap.create(
                electionId=root_election.electionId,
                voteType=NonPostal,
                pollingStationId=polling_station.areaId,
                countingCentreId=counting_centre.areaId,
                districtCentreId=district_centre.areaId,
                electionCommissionId=election_commission.areaId,
                pollingDistrictId=polling_district.areaId,
                pollingDivisionId=polling_division.areaId,
                electoralDistrictId=electoral_district.areaId,
                countryId=country.areaId
            )

            AreaMap.create(
                electionId=root_election.electionId,
                voteType=Postal,
                pollingStationId=polling_station.areaId,
                countingCentreId=postal_vote_counting_centre.areaId,
                districtCentreId=district_centre.areaId,
                electionCommissionId=election_commission.areaId,
                pollingDistrictId=polling_district.areaId,
                pollingDivisionId=polling_division.areaId,
                electoralDistrictId=electoral_district.areaId,
                countryId=country.areaId
            )

        for row in get_rows_from_csv(number_of_seats_dataset_file):
            # pass
            election, postal_election, ordinary_election = _get_electoral_district_election(row)
            election.meta.add_meta_data(
                metaDataKey=META_DATA_KEY_ELECTION_NUMBER_OF_SEATS_ALLOCATED,
                metaDataValue=row["Number of seats"]
            )
            election.meta.add_meta_data(
                metaDataKey=META_DATA_KEY_ELECTION_NUMBER_OF_VALID_VOTE_PERCENTAGE_REQUIRED_FOR_SEAT_ALLOCATION,
                metaDataValue=row["Required percentage of valid votes"]
            )

        db.session.commit()

        update_dashboard_tables()

        return root_election
