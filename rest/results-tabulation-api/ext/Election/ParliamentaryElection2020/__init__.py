from app import db
from constants.TALLY_SHEET_CODES import CE_201, CE_201_PV, PRE_41, PRE_30_PD, PRE_30_ED, \
    PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS, PRE_ALL_ISLAND_RESULTS, PRE_34_CO, PRE_34_I_RO, PRE_34_II_RO, PRE_34, \
    PRE_34_PD, PRE_34_ED, PRE_34_AI
from constants.VOTE_TYPES import Postal, NonPostal
from ext.Election.ParliamentaryElection2020 import RoleBasedAccess
from ext.Election.util import get_rows_from_csv, update_dashboard_tables
from orm.entities import Election, Candidate
from orm.entities.Area import AreaMap
from orm.entities.Area.Electorate import Country, ElectoralDistrict, PollingDivision, PollingDistrict
from orm.entities.Area.Office import PollingStation, CountingCentre, DistrictCentre, ElectionCommission
from orm.entities.Submission import TallySheet
from orm.entities.Submission.TallySheet import TallySheetMap
from orm.enums import AreaTypeEnum

role_based_access_config = RoleBasedAccess


def build_election(root_election: Election, party_candidate_dataset_file=None,
                   polling_station_dataset_file=None, postal_counting_centers_dataset_file=None,
                   invalid_vote_categories_dataset_file=None):
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
