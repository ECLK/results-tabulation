from app import db
from constants.TALLY_SHEET_COLUMN_SOURCE import TALLY_SHEET_COLUMN_SOURCE_META, TALLY_SHEET_COLUMN_SOURCE_CONTENT, \
    TALLY_SHEET_COLUMN_SOURCE_QUERY
from ext.ExtendedElection.ExtendedElectionPresidentialElection2019.TALLY_SHEET_CODES import CE_201, CE_201_PV, PRE_41, \
    PRE_30_PD, PRE_30_ED, \
    PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS, PRE_ALL_ISLAND_RESULTS, PRE_34_CO, PRE_34_I_RO, PRE_34_II_RO, PRE_34, \
    PRE_34_PD, PRE_34_ED, PRE_34_AI
from constants.VOTE_TYPES import Postal, NonPostal
from ext import TallySheetMap
from ext.ExtendedElection import ExtendedElection
from ext.ExtendedElection.ExtendedElectionPresidentialElection2019 import RoleBasedAccess
from ext.ExtendedElection.ExtendedElectionPresidentialElection2019.ExtendedTallySheetVersion.ExtendedTallySheetVersion_PRE_30_ED import \
    ExtendedTallySheetVersion_PRE_30_ED
from ext.ExtendedElection.ExtendedElectionPresidentialElection2019.ExtendedTallySheetVersion.ExtendedTallySheetVersion_PRE_30_PD import \
    ExtendedTallySheetVersion_PRE_30_PD
from ext.ExtendedElection.ExtendedElectionPresidentialElection2019.ExtendedTallySheetVersion.ExtendedTallySheetVersion_PRE_41 import \
    ExtendedTallySheetVersion_PRE_41
from ext.ExtendedElection.ExtendedElectionPresidentialElection2019.ExtendedTallySheetVersion.ExtendedTallySheetVersion_PRE_AI import \
    ExtendedTallySheetVersion_PRE_AI
from ext.ExtendedElection.ExtendedElectionPresidentialElection2019.ExtendedTallySheetVersion.ExtendedTallySheetVersion_PRE_AI_ED import \
    ExtendedTallySheetVersion_PRE_AI_ED
from ext.ExtendedElection.util import get_rows_from_csv, update_dashboard_tables
from orm.entities import Election, Candidate, Template, Party, Meta
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

    def get_extended_tally_sheet_version_class(self, templateName):
        EXTENDED_TEMPLATE_MAP = {
            PRE_41: ExtendedTallySheetVersion_PRE_41,
            PRE_30_PD: ExtendedTallySheetVersion_PRE_30_PD,
            PRE_30_ED: ExtendedTallySheetVersion_PRE_30_ED,
            PRE_ALL_ISLAND_RESULTS: ExtendedTallySheetVersion_PRE_AI,
            PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS: ExtendedTallySheetVersion_PRE_AI_ED
        }

        if templateName in EXTENDED_TEMPLATE_MAP:
            return EXTENDED_TEMPLATE_MAP[templateName]
        else:
            return super(ExtendedElectionPresidentialElection2019, self).get_extended_tally_sheet_version_class(
                templateName=templateName
            )

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
                        }).metaId
                    ),
                    TallySheet.create(
                        template=tally_sheet_template_pre_all_island_ed,
                        electionId=election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "electionId": election.electionId
                        }).metaId
                    ),
                    TallySheet.create(
                        template=tally_sheet_template_pre_34_ai,
                        electionId=election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "electionId": election.electionId
                        }).metaId
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
                        }).metaId
                    ),
                    TallySheet.create(
                        template=tally_sheet_template_pre_34_ed, electionId=election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "electionId": election.electionId
                        }).metaId
                    ),
                    TallySheet.create(
                        template=tally_sheet_template_pre_30_pd, electionId=postal_election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "electionId": postal_election.electionId
                        }).metaId
                    ),
                    TallySheet.create(
                        template=tally_sheet_template_pre_34_pd, electionId=postal_election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "electionId": postal_election.electionId
                        }).metaId
                    ),
                    TallySheet.create(
                        template=tally_sheet_template_pre_34_i_ro, electionId=postal_election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "electionId": postal_election.electionId
                        }).metaId
                    ),
                    TallySheet.create(
                        template=tally_sheet_template_pre_34_ii_ro, electionId=election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "electionId": election.electionId
                        }).metaId
                    ),
                    TallySheet.create(
                        template=tally_sheet_template_pre_34, electionId=election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "electionId": election.electionId
                        }).metaId
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
                        }).metaId
                    ),
                    TallySheet.create(
                        template=tally_sheet_template_pre_34_pd, electionId=ordinary_election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "electionId": ordinary_election.electionId
                        }).metaId
                    ),
                    TallySheet.create(
                        template=tally_sheet_template_pre_34_i_ro, electionId=ordinary_election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "electionId": ordinary_election.electionId
                        }).metaId
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
                        }).metaId
                    ),
                    TallySheet.create(
                        template=tally_sheet_template_pre_34_co, electionId=election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "electionId": election.electionId
                        }).metaId
                    )
                ]

                if election.voteType is NonPostal:
                    tally_sheets.append(TallySheet.create(
                        template=tally_sheet_template_ce_201, electionId=election.electionId, areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "electionId": election.electionId
                        }).metaId
                    ))
                elif election.voteType is Postal:
                    area._registeredVotersCount = row["Registered Voters"]
                    tally_sheets.append(TallySheet.create(
                        template=tally_sheet_template_ce_201_pv, electionId=election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "electionId": election.electionId
                        }).metaId
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
