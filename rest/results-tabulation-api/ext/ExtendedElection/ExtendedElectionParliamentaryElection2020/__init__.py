from sqlalchemy import bindparam
from sqlalchemy.orm import aliased

from app import db
from constants.TALLY_SHEET_COLUMN_SOURCE import TALLY_SHEET_COLUMN_SOURCE_META, TALLY_SHEET_COLUMN_SOURCE_CONTENT, \
    TALLY_SHEET_COLUMN_SOURCE_QUERY
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.ExtendedTallySheetVersion.ExtendedTallySheetVersion_PE_R2 import \
    ExtendedTallySheetVersion_PE_R2
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.META_DATA_KEY import \
    META_DATA_KEY_ELECTION_NUMBER_OF_SEATS_ALLOCATED, \
    META_DATA_KEY_ELECTION_NUMBER_OF_VALID_VOTE_PERCENTAGE_REQUIRED_FOR_SEAT_ALLOCATION
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.TALLY_SHEET_CODES import PE_27, PE_4, PE_CE_RO_V1, \
    PE_R1, PE_CE_RO_PR_1, \
    PE_CE_RO_V2, PE_R2, PE_CE_RO_PR_2, PE_CE_RO_PR_3, CE_201, CE_201_PV, PE_39, PE_22
from constants.VOTE_TYPES import Postal, NonPostal, PostalAndNonPostal
from ext import TallySheetMap
from ext.ExtendedElection import ExtendedElection
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020 import RoleBasedAccess
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.ExtendedTallySheetVersion.ExtendedTallySheetVersion_PE_CE_RO_V1 import \
    ExtendedTallySheetVersion_PE_CE_RO_V1
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.ExtendedTallySheetVersion.ExtendedTallySheetVersion_PE_R1 import \
    ExtendedTallySheetVersion_PE_R1
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.ExtendedTallySheetVersion.ExtendedTallySheetVersion_PE_CE_RO_V2 import \
    ExtendedTallySheetVersion_PE_CE_RO_V2
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.ExtendedTallySheetVersion.ExtendedTallySheetVersion_PE_27 import \
    ExtendedTallySheetVersion_PE_27
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.ExtendedTallySheetVersion.ExtendedTallySheetVersion_PE_4 import \
    ExtendedTallySheetVersion_PE_4
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.ExtendedTallySheetVersion.ExtendedTallySheetVersion_CE_201 import \
    ExtendedTallySheetVersion_CE_201
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.ExtendedTallySheetVersion.ExtendedTallySheetVersion_PE_39 import \
    ExtendedTallySheetVersion_PE_39
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.ExtendedTallySheetVersion.ExtendedTallySheetVersion_PE_22 import \
    ExtendedTallySheetVersion_PE_22
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.TEMPLATE_ROW_TYPE import \
    TEMPLATE_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_1, TEMPLATE_ROW_TYPE_VALID_VOTES_REMAIN_FROM_ROUND_1, \
    TEMPLATE_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_2, TEMPLATE_ROW_TYPE_BONUS_SEATS_ALLOCATED, \
    TEMPLATE_ROW_TYPE_VALID_VOTE_COUNT_CEIL_PER_SEAT, \
    TEMPLATE_ROW_TYPE_MINIMUM_VALID_VOTE_COUNT_REQUIRED_FOR_SEAT_ALLOCATION
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.ExtendedTallySheetVersion.ExtendedTallySheetVersion_PE_CE_RO_PR_1 import \
    ExtendedTallySheetVersion_PE_CE_RO_PR_1
from ext.ExtendedElection.util import get_rows_from_csv, update_dashboard_tables
from orm.entities import Candidate, Template, Party, Meta
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

    def get_extended_tally_sheet_version_class(self, templateName):
        EXTENDED_TEMPLATE_MAP = {
            PE_CE_RO_V1: ExtendedTallySheetVersion_PE_CE_RO_V1,
            PE_R1: ExtendedTallySheetVersion_PE_R1,
            PE_R2: ExtendedTallySheetVersion_PE_R2,
            PE_CE_RO_V2: ExtendedTallySheetVersion_PE_CE_RO_V2,
            PE_27: ExtendedTallySheetVersion_PE_27,
            PE_4: ExtendedTallySheetVersion_PE_4,
            CE_201: ExtendedTallySheetVersion_CE_201,
            PE_39: ExtendedTallySheetVersion_PE_39,
            PE_22: ExtendedTallySheetVersion_PE_22,
            PE_CE_RO_PR_1: ExtendedTallySheetVersion_PE_CE_RO_PR_1
        }

        if templateName in EXTENDED_TEMPLATE_MAP:
            return EXTENDED_TEMPLATE_MAP[templateName]
        else:
            return super(ExtendedElectionParliamentaryElection2020, self).get_extended_tally_sheet_version_class(
                templateName=templateName
            )

    def build_election(self, party_candidate_dataset_file=None,
                       polling_station_dataset_file=None, postal_counting_centers_dataset_file=None,
                       invalid_vote_categories_dataset_file=None, number_of_seats_dataset_file=None):
        root_election = self.election
        # postal_election = root_election.add_sub_election(electionName="Postal", voteType=Postal)
        # ordinary_election = root_election.add_sub_election(electionName="Ordinary", voteType=NonPostal)

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
                 "source": TALLY_SHEET_COLUMN_SOURCE_CONTENT}
            ]
        )
        tally_sheet_template_ce_201_pv_number_of_packets_inserted_to_ballot_box_row = tally_sheet_template_ce_201_pv.add_row(
            templateRowType="NUMBER_OF_PACKETS_INSERTED_TO_BALLOT_BOX",
            hasMany=True,
            isDerived=False,
            columns=[
                {"columnName": "electionId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
                {"columnName": "areaId", "grouped": False, "func": None, "source": TALLY_SHEET_COLUMN_SOURCE_META},
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

        tally_sheet_template_pe_r1 = Template.create(
            templateName=PE_R1
        )
        tally_sheet_template_pe_r1_party_wise_vote_row = tally_sheet_template_pe_r1.add_row(
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
        tally_sheet_template_pe_r1_rejected_vote_row = tally_sheet_template_pe_r1.add_row(
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
        tally_sheet_template_pe_r2_seats_allocated_from_round_2_row = tally_sheet_template_pe_r2.add_row(
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
        tally_sheet_template_pe_ce_ro_pr_1_candidate_wise_first_preference_row = tally_sheet_template_pe_ce_ro_pr_3.add_row(
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

        def _get_country_entry(row):
            area_class = Country
            area_name = row["Country"]
            area_key = area_name

            def _create_country_tally_sheets(area):
                tally_sheets = []

                return tally_sheets

            data_entry_obj = _get_area_entry(root_election, area_class, area_name, area_key,
                                             _create_country_tally_sheets)

            return data_entry_obj

        def _get_electoral_district_entry(row):
            election, postal_election, ordinary_election = _get_electoral_district_election(row)

            area_class = ElectoralDistrict
            area_name = row["Electoral District"]
            area_key = area_name

            def _create_electoral_district_tally_sheets(area):
                tally_sheets = [
                    TallySheet.create(
                        template=tally_sheet_template_pe_ce_ro_v2, electionId=election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "electionId": election.electionId
                        }).metaId
                    ),
                    TallySheet.create(
                        template=tally_sheet_template_pe_r2, electionId=election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "electionId": election.electionId
                        }).metaId
                    ),
                    TallySheet.create(
                        template=tally_sheet_template_pe_ce_ro_v1, electionId=postal_election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "electionId": postal_election.electionId
                        }).metaId
                    ),
                    TallySheet.create(
                        template=tally_sheet_template_pe_r1, electionId=postal_election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "electionId": postal_election.electionId
                        }).metaId
                    )
                ]

                for party in election.parties:
                    tally_sheets += [
                        TallySheet.create(
                            template=tally_sheet_template_pe_ce_ro_pr_1, electionId=postal_election.electionId,
                            areaId=area.areaId,
                            metaId=Meta.create({
                                "areaId": area.areaId,
                                "partyId": party.partyId,
                                "electionId": postal_election.electionId
                            }).metaId
                        ),
                        TallySheet.create(
                            template=tally_sheet_template_pe_ce_ro_pr_2, electionId=election.electionId,
                            areaId=area.areaId,
                            metaId=Meta.create({
                                "areaId": area.areaId,
                                "partyId": party.partyId,
                                "electionId": election.electionId
                            }).metaId
                        ),
                        TallySheet.create(
                            template=tally_sheet_template_pe_ce_ro_pr_3, electionId=election.electionId,
                            areaId=area.areaId,
                            metaId=Meta.create({
                                "areaId": area.areaId,
                                "partyId": party.partyId,
                                "electionId": election.electionId
                            }).metaId
                        )
                    ]

                return tally_sheets

            data_entry_obj = _get_area_entry(election, area_class, area_name, area_key,
                                             _create_electoral_district_tally_sheets)

            return data_entry_obj

        def _get_polling_division_entry(row):
            election, postal_election, ordinary_election = _get_electoral_district_election(row)

            area_class = PollingDivision
            area_name = row["Polling Division"]
            area_key = area_name

            def _create_polling_division_tally_sheets(area):
                tally_sheets = [
                    TallySheet.create(
                        template=tally_sheet_template_pe_ce_ro_v1, electionId=ordinary_election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "electionId": ordinary_election.electionId
                        }).metaId
                    ),
                    TallySheet.create(
                        template=tally_sheet_template_pe_r1, electionId=ordinary_election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "electionId": ordinary_election.electionId
                        }).metaId
                    )
                ]

                for party in election.parties:
                    tally_sheets.append(TallySheet.create(
                        template=tally_sheet_template_pe_ce_ro_pr_1, electionId=ordinary_election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "partyId": party.partyId,
                            "electionId": ordinary_election.electionId
                        }).metaId
                    ))

                return tally_sheets

            data_entry_obj = _get_area_entry(election, area_class, area_name, area_key,
                                             _create_polling_division_tally_sheets)

            return data_entry_obj

        def _get_polling_district_entry(row):
            election, postal_election, ordinary_election = _get_electoral_district_election(row)

            electoral_district = _get_electoral_district_entry(row)["area"]
            polling_division = _get_polling_division_entry(row)["area"]

            area_class = PollingDistrict
            area_name = row["Polling District"]
            area_key = "%s-%s-%s" % (electoral_district.areaName, polling_division.areaName, area_name)

            data_entry_obj = _get_area_entry(election, area_class, area_name, area_key)

            return data_entry_obj

        def _get_polling_station_entry(row):
            election, postal_election, ordinary_election = _get_electoral_district_election(row)

            electoral_district = _get_electoral_district_entry(row)["area"]
            polling_division = _get_polling_division_entry(row)["area"]
            polling_district = _get_polling_district_entry(row)["area"]

            area_class = PollingStation
            area_name = row["Polling Station"]
            area_key = "%s-%s-%s-%s" % (
                electoral_district.areaName, polling_division.areaName, polling_district.areaName, area_name
            )

            data_entry_obj = _get_area_entry(election, area_class, area_name, area_key)
            area = data_entry_obj["area"]

            area._registeredVotersCount = row["Registered Normal Voters"]
            area._registeredPostalVotersCount = row["Registered Postal Voters"]

            return data_entry_obj

        def _get_counting_centre_entry(row):
            election, postal_election, ordinary_election = _get_electoral_district_election(row)

            electoral_district = _get_electoral_district_entry(row)["area"]

            area_class = CountingCentre
            area_name = row["Counting Centre"]
            area_key = "%s-%s" % (electoral_district.areaName, area_name)

            def _create_counting_centre_tally_sheets(area):
                tally_sheets = [
                    TallySheet.create(
                        template=tally_sheet_template_pe_27, electionId=ordinary_election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "electionId": ordinary_election.electionId
                        }).metaId
                    ),
                    TallySheet.create(
                        template=tally_sheet_template_pe_39, electionId=ordinary_election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "electionId": ordinary_election.electionId
                        }).metaId
                    ),
                    TallySheet.create(
                        template=tally_sheet_template_pe_22, electionId=ordinary_election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "electionId": ordinary_election.electionId
                        }).metaId
                    )
                ]

                for party in election.parties:
                    tally_sheets.append(TallySheet.create(
                        template=tally_sheet_template_pe_4, electionId=ordinary_election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "partyId": party.partyId,
                            "electionId": ordinary_election.electionId
                        }).metaId
                    ))

                tally_sheets.append(TallySheet.create(
                    template=tally_sheet_template_ce_201, electionId=ordinary_election.electionId, areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": ordinary_election.electionId
                    }).metaId
                ))

                return tally_sheets

            data_entry_obj = _get_area_entry(ordinary_election, area_class, area_name, area_key,
                                             _create_counting_centre_tally_sheets)

            return data_entry_obj

        def _get_postal_vote_counting_centre_entry(row):
            election, postal_election, ordinary_election = _get_electoral_district_election(row)

            electoral_district = _get_electoral_district_entry(row)["area"]

            area_class = CountingCentre
            area_name = row["Postal Vote Counting Centre"]
            area_key = "%s-%s" % (electoral_district.areaName, area_name)

            def _create_counting_centre_tally_sheets(area):
                tally_sheets = [
                    TallySheet.create(
                        template=tally_sheet_template_pe_27, electionId=postal_election.electionId, areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "electionId": postal_election.electionId
                        }).metaId
                    ),
                    TallySheet.create(
                        template=tally_sheet_template_pe_39, electionId=postal_election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "electionId": postal_election.electionId
                        }).metaId
                    ),
                    TallySheet.create(
                        template=tally_sheet_template_pe_22, electionId=postal_election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "electionId": postal_election.electionId
                        }).metaId
                    )
                ]

                for party in postal_election.parties:
                    tally_sheets.append(TallySheet.create(
                        template=tally_sheet_template_pe_4, electionId=postal_election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "partyId": party.partyId,
                            "electionId": postal_election.electionId
                        }).metaId
                    ))

                tally_sheets.append(TallySheet.create(
                    template=tally_sheet_template_ce_201_pv, electionId=postal_election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": postal_election.electionId
                    }).metaId
                ))

                return tally_sheets

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

            country_entry = _get_country_entry(row=row)

            electoral_district_entry = _get_electoral_district_entry(row=row)
            polling_division_entry = _get_polling_division_entry(row=row)
            polling_district_entry = _get_polling_district_entry(row=row)
            election_commission_entry = _get_election_commission_entry(row=row)
            district_centre_entry = _get_district_centre_entry(row=row)
            counting_centre_entry = _get_counting_centre_entry(row=row)
            postal_vote_counting_centre_entry = _get_postal_vote_counting_centre_entry(row=row)
            polling_station_entry = _get_polling_station_entry(row=row)

            country_entry["area"].add_child(electoral_district_entry["area"].areaId)
            electoral_district_entry["area"].add_child(polling_division_entry["area"].areaId)
            polling_division_entry["area"].add_child(polling_district_entry["area"].areaId)
            polling_district_entry["area"].add_child(polling_station_entry["area"].areaId)
            election_commission_entry["area"].add_child(district_centre_entry["area"].areaId)

            district_centre_entry["area"].add_child(counting_centre_entry["area"].areaId)
            counting_centre_entry["area"].add_child(polling_station_entry["area"].areaId)

            district_centre_entry["area"].add_child(postal_vote_counting_centre_entry["area"].areaId)
            postal_vote_counting_centre_entry["area"].add_child(polling_station_entry["area"].areaId)

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

            AreaMap.create(
                electionId=root_election.electionId,
                voteType=Postal,
                pollingStationId=polling_station_entry["area"].areaId,
                countingCentreId=postal_vote_counting_centre_entry["area"].areaId,
                districtCentreId=district_centre_entry["area"].areaId,
                electionCommissionId=election_commission_entry["area"].areaId,
                pollingDistrictId=polling_district_entry["area"].areaId,
                pollingDivisionId=polling_division_entry["area"].areaId,
                electoralDistrictId=electoral_district_entry["area"].areaId,
                countryId=country_entry["area"].areaId
            )

            pe_27_tally_sheet = counting_centre_entry["tallySheets"][PE_27][0]
            pe_4_tally_sheet = counting_centre_entry["tallySheets"][PE_4][0]
            pe_27_pv_tally_sheet = postal_vote_counting_centre_entry["tallySheets"][PE_27][0]
            pe_4_pv_tally_sheet = postal_vote_counting_centre_entry["tallySheets"][PE_4][0]

            pe_ce_ro_v1_tally_sheet = polling_division_entry["tallySheets"][PE_CE_RO_V1][0]
            pe_r1_tally_sheet = polling_division_entry["tallySheets"][PE_R1][0]
            pe_ce_ro_pr_1_tally_sheet = polling_division_entry["tallySheets"][PE_CE_RO_PR_1][0]
            pe_ce_ro_v1_pv_tally_sheet = electoral_district_entry["tallySheets"][PE_CE_RO_V1][0]
            pe_r1_pv_tally_sheet = electoral_district_entry["tallySheets"][PE_R1][0]
            pe_ce_ro_pr_1_pv_tally_sheet = electoral_district_entry["tallySheets"][PE_CE_RO_PR_1][0]

            pe_ce_ro_v2_tally_sheet = electoral_district_entry["tallySheets"][PE_CE_RO_V2][0]
            pe_r2_tally_sheet = electoral_district_entry["tallySheets"][PE_R2][0]
            pe_ce_ro_pr_2_tally_sheet = electoral_district_entry["tallySheets"][PE_CE_RO_PR_2][0]
            pe_ce_ro_pr_3_tally_sheet = electoral_district_entry["tallySheets"][PE_CE_RO_PR_3][0]

            pe_ce_ro_v1_tally_sheet.add_child(pe_27_tally_sheet)
            pe_r1_tally_sheet.add_child(pe_ce_ro_v1_tally_sheet)
            pe_ce_ro_v1_pv_tally_sheet.add_child(pe_27_pv_tally_sheet)
            pe_r1_pv_tally_sheet.add_child(pe_ce_ro_v1_pv_tally_sheet)

            pe_ce_ro_v2_tally_sheet.add_child(pe_ce_ro_v1_tally_sheet)
            pe_ce_ro_v2_tally_sheet.add_child(pe_ce_ro_v1_pv_tally_sheet)
            pe_r2_tally_sheet.add_child(pe_ce_ro_v2_tally_sheet)

            pe_ce_ro_pr_1_tally_sheet.add_child(pe_4_tally_sheet)
            pe_ce_ro_pr_1_pv_tally_sheet.add_child(pe_4_pv_tally_sheet)
            pe_ce_ro_pr_2_tally_sheet.add_child(pe_ce_ro_pr_1_tally_sheet)
            pe_ce_ro_pr_2_tally_sheet.add_child(pe_ce_ro_pr_1_pv_tally_sheet)
            pe_ce_ro_pr_3_tally_sheet.add_child(pe_ce_ro_pr_2_tally_sheet)

            TallySheetMap.create(
                pe_27_tallySheetId=pe_27_tally_sheet.tallySheetId,
                pe_4_tallySheetId=pe_4_tally_sheet.tallySheetId,
                pe_ce_ro_v1_tallySheetId=pe_ce_ro_v1_tally_sheet.tallySheetId,
                pe_r1_tallySheetId=pe_r1_tally_sheet.tallySheetId,
                pe_ce_ro_pr_1_tallySheetId=pe_ce_ro_pr_1_tally_sheet.tallySheetId,
                pe_ce_ro_v2_tallySheetId=pe_ce_ro_v2_tally_sheet.tallySheetId,
                pe_r2_tallySheetId=pe_r2_tally_sheet.tallySheetId,
                pe_ce_ro_pr_2_tallySheetId=pe_ce_ro_pr_2_tally_sheet.tallySheetId,
                pe_ce_ro_pr_3_tallySheetId=pe_ce_ro_pr_3_tally_sheet.tallySheetId
            )

            TallySheetMap.create(
                pe_27_tallySheetId=pe_27_pv_tally_sheet.tallySheetId,
                pe_4_tallySheetId=pe_4_pv_tally_sheet.tallySheetId,
                pe_ce_ro_v1_tallySheetId=pe_ce_ro_v1_pv_tally_sheet.tallySheetId,
                pe_r1_tallySheetId=pe_r1_pv_tally_sheet.tallySheetId,
                pe_ce_ro_pr_1_tallySheetId=pe_ce_ro_pr_1_pv_tally_sheet.tallySheetId,
                pe_ce_ro_v2_tallySheetId=pe_ce_ro_v2_tally_sheet.tallySheetId,
                pe_r2_tallySheetId=pe_r2_tally_sheet.tallySheetId,
                pe_ce_ro_pr_2_tallySheetId=pe_ce_ro_pr_2_tally_sheet.tallySheetId,
                pe_ce_ro_pr_3_tallySheetId=pe_ce_ro_pr_3_tally_sheet.tallySheetId
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
