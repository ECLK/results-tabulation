from app import db
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.CANDIDATE_TYPE import CANDIDATE_TYPE_NORMAL, \
    CANDIDATE_TYPE_NATIONAL_LIST
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_CE_201 import \
    ExtendedTallySheet_CE_201
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_CE_201_PV import \
    ExtendedTallySheet_CE_201_PV
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_PCE_42 import \
    ExtendedTallySheet_PCE_42
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_PCE_31 import \
    ExtendedTallySheet_PCE_31
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_PCE_35 import \
    ExtendedTallySheet_PCE_35
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_PCE_34 import \
    ExtendedTallySheet_PCE_34
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_PCE_CE_CO_PR_4 import \
    ExtendedTallySheet_PCE_CE_CO_PR_4
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_PCE_CE_RO_PR_1 import \
    ExtendedTallySheet_PCE_CE_RO_PR_1
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_PCE_CE_RO_PR_2 import \
    ExtendedTallySheet_PCE_CE_RO_PR_2
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_PCE_CE_RO_PR_3 import \
    ExtendedTallySheet_PCE_CE_RO_PR_3
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_PCE_CE_RO_V1 import \
    ExtendedTallySheet_PCE_CE_RO_V1
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_PCE_CE_RO_V2 import \
    ExtendedTallySheet_PCE_CE_RO_V2
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedTallySheet.ExtendedTallySheet_PCE_R2 import \
    ExtendedTallySheet_PCE_R2
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.META_DATA_KEY import \
    META_DATA_KEY_ELECTION_NUMBER_OF_SEATS_ALLOCATED, META_DATA_KEY_ELECTION_NUMBER_OF_BONUS_SEATS_ALLOCATED, \
    META_DATA_KEY_ELECTION_NUMBER_OF_VALID_VOTE_PERCENTAGE_REQUIRED_FOR_SEAT_ALLOCATION
from constants.VOTE_TYPES import NonPostal, PostalAndNonPostal
from ext.ExtendedElection import ExtendedElection
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021 import RoleBasedAccess
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.TEMPLATE_ROW_TYPE import \
    TEMPLATE_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_1, TEMPLATE_ROW_TYPE_VALID_VOTES_REMAIN_FROM_ROUND_1, \
    TEMPLATE_ROW_TYPE_SEATS_ALLOCATED_FROM_ROUND_2, TEMPLATE_ROW_TYPE_BONUS_SEATS_ALLOCATED, \
    TEMPLATE_ROW_TYPE_VALID_VOTE_COUNT_CEIL_PER_SEAT, \
    TEMPLATE_ROW_TYPE_MINIMUM_VALID_VOTE_COUNT_REQUIRED_FOR_SEAT_ALLOCATION, TEMPLATE_ROW_TYPE_SEATS_ALLOCATED, \
    TEMPLATE_ROW_TYPE_ELECTED_CANDIDATE, TEMPLATE_ROW_TYPE_DRAFT_SEATS_ALLOCATED_FROM_ROUND_2, \
    TEMPLATE_ROW_TYPE_DRAFT_BONUS_SEATS_ALLOCATED, TEMPLATE_ROW_TYPE_DRAFT_ELECTED_CANDIDATE, \
    TEMPLATE_ROW_TYPE_NATIONAL_LIST_SEATS_ALLOCATED
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.WORKFLOW_ACTION_TYPE import \
    WORKFLOW_ACTION_TYPE_VIEW, \
    WORKFLOW_ACTION_TYPE_SAVE, WORKFLOW_ACTION_TYPE_SUBMIT, WORKFLOW_ACTION_TYPE_REQUEST_CHANGES, \
    WORKFLOW_ACTION_TYPE_VERIFY, WORKFLOW_ACTION_TYPE_EDIT, \
    WORKFLOW_ACTION_TYPE_MOVE_TO_CERTIFY, WORKFLOW_ACTION_TYPE_CERTIFY, WORKFLOW_ACTION_TYPE_RELEASE, \
    WORKFLOW_ACTION_TYPE_PRINT, WORKFLOW_ACTION_TYPE_UPLOAD_PROOF_DOCUMENT, WORKFLOW_ACTION_TYPE_PRINT_LETTER, \
    WORKFLOW_ACTION_TYPE_RELEASE_NOTIFY, WORKFLOW_ACTION_TYPE_BACK_TO_VERIFIED
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.WORKFLOW_STATUS_TYPE import \
    WORKFLOW_STATUS_TYPE_EMPTY, \
    WORKFLOW_STATUS_TYPE_SAVED, WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED, WORKFLOW_STATUS_TYPE_SUBMITTED, \
    WORKFLOW_STATUS_TYPE_VERIFIED, WORKFLOW_STATUS_TYPE_READY_TO_CERTIFY, \
    WORKFLOW_STATUS_TYPE_CERTIFIED, WORKFLOW_STATUS_TYPE_RELEASED, WORKFLOW_STATUS_TYPE_RELEASE_NOTIFIED
from ext.ExtendedElection.util import get_rows_from_csv
from orm.entities import Candidate, Party, Meta, Workflow, TallySheet
from orm.entities.Area import AreaMap
from orm.entities.Area.Electorate import Country, Province, AdministrativeDistrict, PollingDivision, PollingDistrict
from orm.entities.Area.Office import PollingStation, CountingCentre, DistrictCentre, ElectionCommission
from orm.enums import AreaTypeEnum
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.ExtendedFunctions import \
    get_area_map_query, get_extended_tally_sheet_class, get_root_token
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.Workflows import data_entry, report, \
    released_report, edit_allowed_released_report
from ext.ExtendedElection.ExtendedElectionProvincialCouncilElection2021.TallysheetTemplates import ce_201, ce_201_pv, \
    pce_31, pce_34, pce_35, pce_ce_ro_v1, pce_ce_ro_v2, pce_r2, pce_ce_co_pr_4, pce_ce_ro_pr_1, pce_ce_ro_pr_2, \
    pce_ce_ro_pr_3, pce_ce_co_pr_3, pce_42, pce_r1, administrative_district_result_party_wise_postal, \
    polling_division_result_party_wise, provincial_result_candidates, provincial_result_party_wise_with_seats, \
    polling_division_results

role_based_access_config = RoleBasedAccess.role_based_access_config


class ExtendedElectionProvincialCouncilElection2021(ExtendedElection):
    def __init__(self, election):
        super(ExtendedElectionProvincialCouncilElection2021, self).__init__(
            election=election,
            role_based_access_config=role_based_access_config
        )

    def get_area_map_query(self):
        return get_area_map_query.get_area_map_query(self)

    def get_extended_tally_sheet_class(self, templateName):
        return get_extended_tally_sheet_class.get_extended_tally_sheet_class(self, templateName)

    def build_election(self, party_candidate_dataset_file=None,
                       polling_station_dataset_file=None, postal_counting_centers_dataset_file=None,
                       invalid_vote_categories_dataset_file=None, number_of_seats_dataset_file=None):

        root_election = self.election

        workflow_data_entry: Workflow = data_entry.create_workflow()
        workflow_report: Workflow = report.create_workflow()
        workflow_released_report: Workflow = released_report.create_workflow()
        workflow_edit_allowed_released_report: Workflow = edit_allowed_released_report.create_workflow()

        if not party_candidate_dataset_file:
            party_candidate_dataset_file = root_election.partyCandidateDataset.fileContent

        if not polling_station_dataset_file:
            polling_station_dataset_file = root_election.pollingStationsDataset.fileContent
        if not postal_counting_centers_dataset_file:
            postal_counting_centers_dataset_file = root_election.postalCountingCentresDataset.fileContent

        if not number_of_seats_dataset_file:
            number_of_seats_dataset_file = root_election.numberOfSeatsDataset.fileContent

        if not invalid_vote_categories_dataset_file:
            invalid_vote_categories_dataset_file = root_election.invalidVoteCategoriesDataset.fileContent

        tally_sheet_template_ce_201 = ce_201.create_template()
        tally_sheet_template_ce_201_pv = ce_201_pv.create_template()
        tally_sheet_template_pce_34 = pce_34.create_template()
        tally_sheet_template_pce_35 = pce_35.create_template()

        tally_sheet_template_pce_31 = pce_31.create_template()
        tally_sheet_template_pce_ce_co_pr_3 = pce_ce_co_pr_3.create_template()
        tally_sheet_template_pce_ce_co_pr_4 = pce_ce_co_pr_4.create_template()

        tally_sheet_template_pce_ce_ro_v1 = pce_ce_ro_v1.create_template()
        tally_sheet_template_pce_r1 = pce_r1.create_template()
        tally_sheet_template_pce_ce_ro_v2 = pce_ce_ro_v2.create_template()
        tally_sheet_template_pce_r2 = pce_r2.create_template()

        tally_sheet_template_pce_ce_ro_pr_1 = pce_ce_ro_pr_1.create_template()
        tally_sheet_template_pce_ce_ro_pr_2 = pce_ce_ro_pr_2.create_template()
        tally_sheet_template_pce_ce_ro_pr_3 = pce_ce_ro_pr_3.create_template()

        tally_sheet_template_pce_42 = pce_42.create_template()

        tally_sheet_template_administrative_district_result_party_wise_postal = administrative_district_result_party_wise_postal.create_template()
        tally_sheet_template_polling_division_result_party_wise = polling_division_result_party_wise.create_template()
        tally_sheet_template_polling_division_results = polling_division_results.create_template()
        tally_sheet_template_provincial_result_party_wise_with_seats = provincial_result_party_wise_with_seats.create_template()
        tally_sheet_template_provincial_result_candidates = provincial_result_candidates.create_template()

        data_entry_store = {
            AreaTypeEnum.Country: {},
            AreaTypeEnum.Province: {},
            AreaTypeEnum.AdministrativeDistrict: {},
            AreaTypeEnum.PollingDivision: {},
            AreaTypeEnum.PollingDistrict: {},
            AreaTypeEnum.PollingStation: {},
            AreaTypeEnum.CountingCentre: {},
            AreaTypeEnum.DistrictCentre: {},
            AreaTypeEnum.ElectionCommission: {},
        }

        province_election_store = {}
        province_sub_election_store = {}
        administrative_district_election_store = {}
        administrative_district_sub_election_store = {}
        party_store = {}

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

        def _get_candidate(row):
            candidate_type = row["Candidate Type"]
            party = _get_party(row)

            candidate = Candidate.create(
                candidateName=row["Candidate Name"], candidateNumber=row["Candidate Number"],
                candidateType=candidate_type)

            root_election.add_candidate(candidateId=candidate.candidateId, partyId=party.partyId)

            if candidate_type == CANDIDATE_TYPE_NORMAL:

                administrative_district_election = _get_administrative_district_election(row)
                administrative_district_election.add_candidate(candidateId=candidate.candidateId, partyId=party.partyId)

                for administrative_district_sub_election in administrative_district_election.subElections:
                    administrative_district_sub_election.add_candidate(candidateId=candidate.candidateId,
                                                                       partyId=party.partyId)

            return candidate

        def _get_party(row):
            candidate_type = row["Candidate Type"]
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

            if candidate_type == CANDIDATE_TYPE_NORMAL:
                administrative_district_election = _get_administrative_district_election(row)
                administrative_district_election.add_party(partyId=party.partyId)
                for administrative_district_sub_election in administrative_district_election.subElections:
                    administrative_district_sub_election.add_party(partyId=party.partyId)

            return party_store[party_name_unique]

        def _get_country_entry(row):
            area_class = Country
            area_name = row["Country"]
            area_key = area_name

            data_entry_obj = _get_area_entry(root_election, area_class, area_name, area_key,
                                             None)

            return data_entry_obj

        def _get_election_commission_entry(row):
            administrative_district_election = _get_administrative_district_election(row)

            area_class = ElectionCommission
            area_name = row["Election Commission"]
            area_key = area_name

            data_entry_obj = _get_area_entry(administrative_district_election, area_class, area_name, area_key)

            return data_entry_obj

        def _get_province_entry(row):
            area_class = Province
            area_name = row["Province"]
            area_key = area_name

            def _create_province_tally_sheets(area):
                # TODO : create province tallysheet templates
                return None

            data_entry_obj = _get_area_entry(root_election, area_class, area_name, area_key,
                                             None)

            return data_entry_obj

        def _get_province_sub_election_map(row):
            province_name = row["Province"]

            return province_sub_election_store[province_name]

        def _get_province_sub_election(row, vote_type):
            province_name = row["Province"]
            province_election = _get_province_election(row)
            election_map = _get_province_sub_election_map(row)

            if vote_type not in election_map:
                sub_election = province_election.add_sub_election(
                    electionName="%s - %s - %s" % (root_election.electionName, province_name, vote_type),
                    voteType=vote_type, isListed=False
                )
                election_map[vote_type] = sub_election
                for party in province_election.parties:
                    sub_election.add_party(partyId=party.partyId)
                    for candidate in party.candidates:
                        sub_election.add_candidate(partyId=party.partyId, candidateId=candidate.candidateId)

                if vote_type is not NonPostal:
                    _get_sub_province_entry(row, vote_type=vote_type)
            else:
                sub_election = election_map[vote_type]

            return sub_election

        def _get_province_election(row):
            province_name = row["Province"]

            if province_name not in province_election_store:
                election = root_election.add_sub_election(
                    electionName="%s - %s" % (root_election.electionName, province_name),
                    voteType=PostalAndNonPostal, isListed=True
                )
                province_election_store[province_name] = election
            else:
                election = province_election_store[province_name]

            return election

        def _get_administrative_district_sub_election_map(row):
            administrative_district_name = row["Administrative District"]

            return administrative_district_sub_election_store[administrative_district_name]

        def _get_administrative_district_sub_election(row, vote_type):
            administrative_district_name = row["Administrative District"]
            administrative_district_election = _get_administrative_district_election(row)
            election_map = _get_administrative_district_sub_election_map(row)

            if vote_type not in election_map:
                sub_election = administrative_district_election.add_sub_election(
                    electionName="%s - %s - %s" % (root_election.electionName, administrative_district_name, vote_type),
                    voteType=vote_type, isListed=False
                )
                election_map[vote_type] = sub_election
                for party in administrative_district_election.parties:
                    sub_election.add_party(partyId=party.partyId)
                    for candidate in party.candidates:
                        sub_election.add_candidate(partyId=party.partyId, candidateId=candidate.candidateId)

                if vote_type is not NonPostal:
                    _get_sub_administrative_district_entry(row, vote_type=vote_type)
            else:
                sub_election = election_map[vote_type]

            return sub_election

        def _get_administrative_district_election(row):
            administrative_district_name = row["Administrative District"]
            province_election = _get_province_election(row)

            if administrative_district_name not in administrative_district_election_store:
                election = province_election.add_sub_election(
                    electionName="%s - %s" % (root_election.electionName, administrative_district_name),
                    voteType=PostalAndNonPostal, isListed=True
                )
                administrative_district_election_store[administrative_district_name] = election
                administrative_district_sub_election_store[administrative_district_name] = {}
            else:
                election = administrative_district_election_store[administrative_district_name]

            return election

        def _get_sub_administrative_district_entry(row, vote_type=None):
            administrative_district = _get_administrative_district_entry(row)
            administrative_district_sub_election = _get_administrative_district_sub_election(row, vote_type=vote_type)

            polling_division_results_tally_sheet = TallySheet.create(
                template=polling_division_result_party_wise,
                electionId=administrative_district_sub_election.electionId,
                areaId=administrative_district.areaId,
                metaId=Meta.create({
                    "areaId": administrative_district.areaId,
                    "electionId": administrative_district_sub_election.electionId
                }).metaId,
                workflowInstanceId=workflow_report.get_new_instance().workflowInstanceId
            )
            administrative_district.polling_division_results_tally_sheet_list.append(
                polling_division_results_tally_sheet)
            pce_ce_ro_v1_tally_sheet = TallySheet.create(
                template=tally_sheet_template_pce_ce_ro_v1, electionId=administrative_district_sub_election.electionId,
                areaId=administrative_district.areaId,
                metaId=Meta.create({
                    "areaId": administrative_district.areaId,
                    "electionId": administrative_district_sub_election.electionId
                }).metaId,
                parentTallySheets=[polling_division_results_tally_sheet,
                                   *administrative_district.pce_ce_ro_v2_tally_sheet_list],
                workflowInstanceId=workflow_released_report.get_new_instance().workflowInstanceId
            )
            administrative_district.pce_ce_ro_v1_tally_sheet_list.append(pce_ce_ro_v1_tally_sheet)
            administrative_district.pce_ce_ro_v1_tally_sheet_list_vote_type_wise_map[vote_type] = [
                pce_ce_ro_v1_tally_sheet]

            for party in administrative_district_sub_election.parties:
                pce_ce_ro_pr_1_tally_sheet = TallySheet.create(
                    template=tally_sheet_template_pce_ce_ro_pr_1,
                    electionId=administrative_district_sub_election.electionId,
                    areaId=administrative_district.areaId,
                    metaId=Meta.create({
                        "areaId": administrative_district.areaId,
                        "partyId": party.partyId,
                        "electionId": administrative_district_sub_election.electionId
                    }).metaId,
                    parentTallySheets=[
                        *administrative_district.pce_ce_ro_pr_2_tally_sheet_list_party_id_wise_map[party.partyId]],
                    workflowInstanceId=workflow_report.get_new_instance().workflowInstanceId
                )
                administrative_district.pce_ce_ro_pr_1_tally_sheet_list.append(pce_ce_ro_pr_1_tally_sheet)

                party_id_and_vote_type_key = "%s%s" % (party.partyId, vote_type)
                if party_id_and_vote_type_key not in administrative_district.pce_ce_ro_pr_1_tally_sheet_list_party_id_and_vote_type_wise_map:
                    administrative_district.pce_ce_ro_pr_1_tally_sheet_list_party_id_and_vote_type_wise_map[
                        party_id_and_vote_type_key] = [pce_ce_ro_pr_1_tally_sheet]
                else:
                    administrative_district.pce_ce_ro_pr_1_tally_sheet_list_party_id_and_vote_type_wise_map[
                        party_id_and_vote_type_key].append(pce_ce_ro_pr_1_tally_sheet)

        def _get_administrative_district_entry(row):
            administrative_district_election = _get_administrative_district_election(row)
            province = _get_province_entry(row)
            country = _get_country_entry(row)

            area_class = AdministrativeDistrict
            area_name = row["Administrative District"]
            area_key = area_name

            def _create_administrative_district_tally_sheets(area):
                pce_ai_ed_tally_sheet_list = country.pce_ai_ed_tally_sheet_list
                pce_ai_sa_tally_sheet_list = country.pce_ai_sa_tally_sheet_list
                pce_ai_1_tally_sheet_list = country.pce_ai_1_tally_sheet_list
                pce_ai_2_tally_sheet_list = country.pce_ai_2_tally_sheet_list

                pce_21_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_pce_r2, electionId=administrative_district_election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": administrative_district_election.electionId
                    }).metaId,
                    parentTallySheets=[*pce_ai_2_tally_sheet_list],
                    workflowInstanceId=workflow_edit_allowed_released_report.get_new_instance().workflowInstanceId
                )]

                pce_r2_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_pce_r2, electionId=administrative_district_election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": administrative_district_election.electionId
                    }).metaId,
                    parentTallySheets=[*pce_21_tally_sheet_list, *pce_ai_sa_tally_sheet_list,
                                       *pce_ai_1_tally_sheet_list],
                    workflowInstanceId=workflow_edit_allowed_released_report.get_new_instance().workflowInstanceId
                )]

                pce_ce_ro_v2_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_pce_ce_ro_v2, electionId=administrative_district_election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": administrative_district_election.electionId
                    }).metaId,
                    parentTallySheets=[*pce_r2_tally_sheet_list, *pce_ai_ed_tally_sheet_list],
                    workflowInstanceId=workflow_report.get_new_instance().workflowInstanceId
                )]

                polling_division_results_tally_sheet_list = []
                pce_ce_ro_v1_tally_sheet_list = []
                pce_ce_ro_v1_tally_sheet_list_vote_type_wise_map = {}

                pce_ce_ro_pr_1_tally_sheet_list = []
                pce_ce_ro_pr_1_tally_sheet_list_party_id_and_vote_type_wise_map = {}
                pce_ce_ro_pr_2_tally_sheet_list = []
                pce_ce_ro_pr_2_tally_sheet_list_party_id_wise_map = {}
                pce_ce_ro_pr_3_tally_sheet_list = []
                pce_ce_ro_pr_3_tally_sheet_list_party_id_wise_map = {}
                for party in administrative_district_election.parties:
                    pce_ce_ro_pr_3_tally_sheet = TallySheet.create(
                        template=tally_sheet_template_pce_ce_ro_pr_3,
                        electionId=administrative_district_election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "partyId": party.partyId,
                            "electionId": administrative_district_election.electionId
                        }).metaId,
                        parentTallySheets=pce_21_tally_sheet_list,
                        workflowInstanceId=workflow_report.get_new_instance().workflowInstanceId
                    )
                    pce_ce_ro_pr_3_tally_sheet_list.append(pce_ce_ro_pr_3_tally_sheet)
                    if party.partyId not in pce_ce_ro_pr_3_tally_sheet_list_party_id_wise_map:
                        pce_ce_ro_pr_3_tally_sheet_list_party_id_wise_map[party.partyId] = [pce_ce_ro_pr_3_tally_sheet]
                    else:
                        pce_ce_ro_pr_3_tally_sheet_list_party_id_wise_map[party.partyId].append(
                            pce_ce_ro_pr_3_tally_sheet)

                    pce_ce_ro_pr_2_tally_sheet = TallySheet.create(
                        template=tally_sheet_template_pce_ce_ro_pr_2,
                        electionId=administrative_district_election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "partyId": party.partyId,
                            "electionId": administrative_district_election.electionId
                        }).metaId,
                        parentTallySheets=[*pce_ce_ro_pr_3_tally_sheet_list_party_id_wise_map[party.partyId]],
                        workflowInstanceId=workflow_report.get_new_instance().workflowInstanceId
                    )
                    pce_ce_ro_pr_2_tally_sheet_list.append(pce_ce_ro_pr_2_tally_sheet)
                    if party.partyId not in pce_ce_ro_pr_2_tally_sheet_list_party_id_wise_map:
                        pce_ce_ro_pr_2_tally_sheet_list_party_id_wise_map[party.partyId] = [pce_ce_ro_pr_2_tally_sheet]
                    else:
                        pce_ce_ro_pr_2_tally_sheet_list_party_id_wise_map[party.partyId].append(
                            pce_ce_ro_pr_2_tally_sheet)

                return {
                    "pce_ce_ro_v1_tally_sheet_list": pce_ce_ro_v1_tally_sheet_list,
                    "pce_ce_ro_v1_tally_sheet_list_vote_type_wise_map": pce_ce_ro_v1_tally_sheet_list_vote_type_wise_map,
                    "polling_division_results_tally_sheet_list": polling_division_results_tally_sheet_list,
                    "pce_r2_tally_sheet_list": pce_r2_tally_sheet_list,
                    "pce_ce_ro_v2_tally_sheet_list": pce_ce_ro_v2_tally_sheet_list,
                    "pce_ce_ro_pr_1_tally_sheet_list": pce_ce_ro_pr_1_tally_sheet_list,
                    "pce_ce_ro_pr_1_tally_sheet_list_party_id_and_vote_type_wise_map": pce_ce_ro_pr_1_tally_sheet_list_party_id_and_vote_type_wise_map,
                    "pce_ce_ro_pr_2_tally_sheet_list": pce_ce_ro_pr_2_tally_sheet_list,
                    "pce_ce_ro_pr_2_tally_sheet_list_party_id_wise_map": pce_ce_ro_pr_2_tally_sheet_list_party_id_wise_map,
                    "pce_ce_ro_pr_3_tally_sheet_list": pce_ce_ro_pr_3_tally_sheet_list,
                    "pce_ce_ro_pr_3_tally_sheet_list_party_id_wise_map": pce_ce_ro_pr_3_tally_sheet_list_party_id_wise_map
                }

            data_entry_obj = _get_area_entry(administrative_district_election, area_class, area_name, area_key,
                                             _create_administrative_district_tally_sheets)

            return data_entry_obj

        def _get_administrative_district_counting_centre_entry(row):
            area_class = CountingCentre
            area_name = row["Counting Centre"]
            vote_type = row["Vote Type"]

            administrative_district_sub_election = _get_administrative_district_sub_election(row, vote_type=vote_type)
            administrative_district = _get_administrative_district_entry(row=row)

            area_key = "%s-%s" % (administrative_district.areaName, area_name)

            def _create_counting_centre_tally_sheets(area):
                pce_ce_ro_v1_tally_sheet_list_vote_type_wise_map = administrative_district.pce_ce_ro_v1_tally_sheet_list_vote_type_wise_map
                pce_ce_ro_pr_1_tally_sheet_list_party_id_and_vote_type_wise_map = administrative_district.pce_ce_ro_pr_1_tally_sheet_list_party_id_and_vote_type_wise_map

                pce_35_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_pce_35, electionId=administrative_district_sub_election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": administrative_district_sub_election.electionId
                    }).metaId,
                    parentTallySheets=pce_ce_ro_v1_tally_sheet_list_vote_type_wise_map[vote_type],
                    workflowInstanceId=workflow_data_entry.get_new_instance().workflowInstanceId
                )]

                pce_34_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_pce_34,
                    electionId=administrative_district_sub_election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": administrative_district_sub_election.electionId
                    }).metaId,
                    workflowInstanceId=workflow_data_entry.get_new_instance().workflowInstanceId
                )]
                pce_31_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_pce_31,
                    electionId=administrative_district_sub_election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": administrative_district_sub_election.electionId
                    }).metaId,
                    workflowInstanceId=workflow_data_entry.get_new_instance().workflowInstanceId
                )]

                pce_ce_co_pr_4_tally_sheet_list = []
                pce_ce_co_pr_4_tally_sheet_list_party_id_wise_map = {}
                for party in administrative_district_sub_election.parties:
                    pce_ce_co_pr_4_tally_sheet = TallySheet.create(
                        template=tally_sheet_template_pce_ce_co_pr_4,
                        electionId=administrative_district_sub_election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "partyId": party.partyId,
                            "electionId": administrative_district_sub_election.electionId
                        }).metaId,
                        parentTallySheets=[*pce_ce_ro_pr_1_tally_sheet_list_party_id_and_vote_type_wise_map[
                            "%s%s" % (party.partyId, vote_type)]],
                        workflowInstanceId=workflow_data_entry.get_new_instance().workflowInstanceId
                    )
                    pce_ce_co_pr_4_tally_sheet_list.append(pce_ce_co_pr_4_tally_sheet)

                    if party.partyId not in pce_ce_co_pr_4_tally_sheet_list_party_id_wise_map:
                        pce_ce_co_pr_4_tally_sheet_list_party_id_wise_map[party.partyId] = [pce_ce_co_pr_4_tally_sheet]
                    else:
                        pce_ce_co_pr_4_tally_sheet_list_party_id_wise_map[party.partyId].append(
                            pce_ce_co_pr_4_tally_sheet)

                pce_ce_201_pv_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_ce_201_pv, electionId=administrative_district_sub_election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": administrative_district_sub_election.electionId
                    }).metaId,
                    workflowInstanceId=workflow_data_entry.get_new_instance().workflowInstanceId
                )]

                return {
                    "pce_35_tally_sheet_list": pce_35_tally_sheet_list,
                    "pce_34_tally_sheet_list": pce_34_tally_sheet_list,
                    "pce_31_tally_sheet_list": pce_31_tally_sheet_list,
                    "pce_ce_co_pr_4_tally_sheet_list": pce_ce_co_pr_4_tally_sheet_list,
                    "pce_ce_co_pr_4_tally_sheet_list_party_id_wise_map": pce_ce_co_pr_4_tally_sheet_list_party_id_wise_map,
                    "pce_ce_201_pv_tally_sheet_list": pce_ce_201_pv_tally_sheet_list
                }

            data_entry_obj = _get_area_entry(administrative_district_sub_election, area_class, area_name, area_key,
                                             _create_counting_centre_tally_sheets)

            return data_entry_obj

        def _get_polling_division_entry(row):
            administrative_district_ordinary_election = _get_administrative_district_sub_election(row,
                                                                                                  vote_type=NonPostal)

            administrative_district = _get_administrative_district_entry(row)

            area_class = PollingDivision
            area_name = row["Polling Division"]
            area_key = area_name

            def _create_polling_division_tally_sheets(area):
                pce_ce_ro_pr_2_tally_sheet_list_party_id_wise_map = administrative_district.pce_ce_ro_pr_2_tally_sheet_list_party_id_wise_map
                pce_ce_ro_v2_tally_sheet_list = administrative_district.pce_ce_ro_v2_tally_sheet_list

                polling_division_results_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_polling_division_results,
                    electionId=administrative_district_ordinary_election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": administrative_district_ordinary_election.electionId
                    }).metaId,
                    workflowInstanceId=workflow_report.get_new_instance().workflowInstanceId
                )]

                pce_ce_ro_v1_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_pce_ce_ro_v1,
                    electionId=administrative_district_ordinary_election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": administrative_district_ordinary_election.electionId
                    }).metaId,
                    parentTallySheets=[*polling_division_results_tally_sheet_list, *pce_ce_ro_v2_tally_sheet_list],
                    workflowInstanceId=workflow_released_report.get_new_instance().workflowInstanceId
                )]

                pce_ce_ro_pr_1_tally_sheet_list = []
                pce_ce_ro_pr_1_tally_sheet_list_party_id_and_vote_type_wise_map = {}
                for party in administrative_district_ordinary_election.parties:
                    pce_ce_ro_pr_1_tally_sheet = TallySheet.create(
                        template=tally_sheet_template_pce_ce_ro_pr_1,
                        electionId=administrative_district_ordinary_election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "partyId": party.partyId,
                            "electionId": administrative_district_ordinary_election.electionId
                        }).metaId,
                        parentTallySheets=[*pce_ce_ro_pr_2_tally_sheet_list_party_id_wise_map[party.partyId]],
                        workflowInstanceId=workflow_report.get_new_instance().workflowInstanceId
                    )
                    pce_ce_ro_pr_1_tally_sheet_list.append(pce_ce_ro_pr_1_tally_sheet)

                    party_id_and_vote_type_key = "%s%s" % (party.partyId, NonPostal)
                    if party_id_and_vote_type_key not in pce_ce_ro_pr_1_tally_sheet_list_party_id_and_vote_type_wise_map:
                        pce_ce_ro_pr_1_tally_sheet_list_party_id_and_vote_type_wise_map[
                            party_id_and_vote_type_key] = [
                            pce_ce_ro_pr_1_tally_sheet]
                    else:
                        pce_ce_ro_pr_1_tally_sheet_list_party_id_and_vote_type_wise_map[
                            party_id_and_vote_type_key].append(pce_ce_ro_pr_1_tally_sheet)

                return {
                    "pce_ce_ro_v1_tally_sheet_list": pce_ce_ro_v1_tally_sheet_list,
                    "pce_ce_ro_pr_1_tally_sheet_list": pce_ce_ro_pr_1_tally_sheet_list,
                    "pce_ce_ro_pr_1_tally_sheet_list_party_id_and_vote_type_wise_map": pce_ce_ro_pr_1_tally_sheet_list_party_id_and_vote_type_wise_map,
                    "polling_division_results_tally_sheet_list": polling_division_results_tally_sheet_list,
                }

            data_entry_obj = _get_area_entry(administrative_district_ordinary_election, area_class, area_name, area_key,
                                             _create_polling_division_tally_sheets)

            return data_entry_obj

        def _get_polling_district_entry(row):
            administrative_district_ordinary_election = _get_administrative_district_sub_election(row,
                                                                                                  vote_type=NonPostal)

            administrative_district = _get_administrative_district_entry(row)
            polling_division = _get_polling_division_entry(row)

            area_class = PollingDistrict
            area_name = row["Polling District"]
            area_key = "%s-%s-%s" % (administrative_district.areaName, polling_division.areaName, area_name)

            data_entry_obj = _get_area_entry(administrative_district_ordinary_election, area_class, area_name, area_key)

            return data_entry_obj

        def _get_polling_station_entry(row):
            administrative_district_ordinary_election = _get_administrative_district_sub_election(row,
                                                                                                  vote_type=NonPostal)

            administrative_district = _get_administrative_district_entry(row)
            polling_division = _get_polling_division_entry(row)
            polling_district = _get_polling_district_entry(row)

            area_class = PollingStation
            area_name = row["Polling Station"]
            area_key = "%s-%s-%s-%s" % (
                administrative_district.areaName, polling_division.areaName, polling_district.areaName, area_name
            )

            area = _get_area_entry(administrative_district_ordinary_election, area_class, area_name, area_key)

            area._registeredVotersCount = row["Registered Normal Voters"]
            area._registeredPostalVotersCount = row["Registered Postal Voters"]
            area._registeredQuarantineVotersCount = row["Registered Quarantine Voters"]
            area._registeredDisplacedVotersCount = row["Registered Displaced Voters"]

            return area

        def _get_counting_centre_entry(row):
            administrative_district_ordinary_election = _get_administrative_district_sub_election(row,
                                                                                                  vote_type=NonPostal)

            administrative_district = _get_administrative_district_entry(row)
            polling_division = _get_polling_division_entry(row)

            area_class = CountingCentre
            area_name = row["Counting Centre"]
            area_key = "%s-%s" % (administrative_district.areaName, area_name)

            def _create_counting_centre_tally_sheets(area):
                pce_ce_ro_v1_tally_sheet_list = polling_division.pce_ce_ro_v1_tally_sheet_list
                pce_ce_ro_pr_1_tally_sheet_list_party_id_and_vote_type_wise_map = polling_division.pce_ce_ro_pr_1_tally_sheet_list_party_id_and_vote_type_wise_map

                pce_35_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_pce_35,
                    electionId=administrative_district_ordinary_election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": administrative_district_ordinary_election.electionId
                    }).metaId,
                    parentTallySheets=pce_ce_ro_v1_tally_sheet_list,
                    workflowInstanceId=workflow_data_entry.get_new_instance().workflowInstanceId
                )]

                pce_34_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_pce_34, electionId=administrative_district_ordinary_election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": administrative_district_ordinary_election.electionId
                    }).metaId,
                    workflowInstanceId=workflow_data_entry.get_new_instance().workflowInstanceId
                )]
                pce_31_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_pce_31, electionId=administrative_district_ordinary_election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": administrative_district_ordinary_election.electionId
                    }).metaId,
                    workflowInstanceId=workflow_data_entry.get_new_instance().workflowInstanceId
                )]

                pce_ce_co_pr_4_tally_sheet_list = []
                pce_ce_co_pr_4_tally_sheet_list_party_id_wise_map = {}
                for party in administrative_district_ordinary_election.parties:
                    pce_ce_co_pr_4_tally_sheet = TallySheet.create(
                        template=tally_sheet_template_pce_ce_co_pr_4,
                        electionId=administrative_district_ordinary_election.electionId,
                        areaId=area.areaId,
                        metaId=Meta.create({
                            "areaId": area.areaId,
                            "partyId": party.partyId,
                            "electionId": administrative_district_ordinary_election.electionId
                        }).metaId,
                        parentTallySheets=[*pce_ce_ro_pr_1_tally_sheet_list_party_id_and_vote_type_wise_map[
                            "%s%s" % (party.partyId, NonPostal)]],
                        workflowInstanceId=workflow_data_entry.get_new_instance().workflowInstanceId
                    )
                    pce_ce_co_pr_4_tally_sheet_list.append(pce_ce_co_pr_4_tally_sheet)

                    if party.partyId not in pce_ce_co_pr_4_tally_sheet_list_party_id_wise_map:
                        pce_ce_co_pr_4_tally_sheet_list_party_id_wise_map[party.partyId] = [pce_ce_co_pr_4_tally_sheet]
                    else:
                        pce_ce_co_pr_4_tally_sheet_list_party_id_wise_map[party.partyId].append(
                            pce_ce_co_pr_4_tally_sheet)

                pce_ce_201_tally_sheet_list = [TallySheet.create(
                    template=tally_sheet_template_ce_201,
                    electionId=administrative_district_ordinary_election.electionId,
                    areaId=area.areaId,
                    metaId=Meta.create({
                        "areaId": area.areaId,
                        "electionId": administrative_district_ordinary_election.electionId
                    }).metaId,
                    workflowInstanceId=workflow_data_entry.get_new_instance().workflowInstanceId
                )]

                return {
                    "pce_35_tally_sheet_list": pce_35_tally_sheet_list,
                    "pce_34_tally_sheet_list": pce_34_tally_sheet_list,
                    "pce_31_tally_sheet_list": pce_31_tally_sheet_list,
                    "pce_ce_co_pr_4_tally_sheet_list": pce_ce_co_pr_4_tally_sheet_list,
                    "pce_ce_co_pr_4_tally_sheet_list_party_id_wise_map": pce_ce_co_pr_4_tally_sheet_list_party_id_wise_map,
                    "pce_ce_201_tally_sheet_list": pce_ce_201_tally_sheet_list
                }

            data_entry_obj = _get_area_entry(administrative_district_ordinary_election, area_class, area_name, area_key,
                                             _create_counting_centre_tally_sheets)

            return data_entry_obj

        def _get_district_centre_entry(row):
            administrative_district_election = _get_administrative_district_election(row)

            area_class = DistrictCentre
            area_name = row["District Centre"]
            area_key = area_name

            data_entry_obj = _get_area_entry(administrative_district_election, area_class, area_name, area_key)

            return data_entry_obj

        # def extract_csv_files():
        for row in get_rows_from_csv(party_candidate_dataset_file):
            _get_candidate(row)

        for row in get_rows_from_csv(polling_station_dataset_file):
            row["Country"] = "Sri Lanka"
            row["Election Commission"] = "Sri Lanka Election Commission"
            row["Polling Station"] = row["Polling Station (English)"]

            country = _get_country_entry(row=row)
            province = _get_province_entry(row=row)
            administrative_district = _get_administrative_district_entry(row=row)
            polling_division = _get_polling_division_entry(row=row)
            polling_district = _get_polling_district_entry(row=row)
            election_commission = _get_election_commission_entry(row=row)
            district_centre = _get_district_centre_entry(row=row)
            counting_centre = _get_counting_centre_entry(row=row)
            polling_station = _get_polling_station_entry(row=row)

            country.add_child(province.areaId)
            province.add_child(administrative_district.areaId)
            administrative_district.add_child(polling_division.areaId)
            polling_division.add_child(polling_district.areaId)
            polling_district.add_child(polling_station.areaId)
            election_commission.add_child(district_centre.areaId)
            district_centre.add_child(counting_centre.areaId)
            counting_centre.add_child(polling_station.areaId)

            AreaMap.create(
                electionId=root_election.electionId,
                voteType=NonPostal,
                pollingStationId=polling_station.areaId,
                countingCentreId=counting_centre.areaId,
                districtCentreId=district_centre.areaId,
                electionCommissionId=election_commission.areaId,
                pollingDistrictId=polling_district.areaId,
                pollingDivisionId=polling_division.areaId,
                administrativeDistrictId=administrative_district.areaId,
                provinceId=province.areaId,
                countryId=country.areaId
            )

        for row in get_rows_from_csv(postal_counting_centers_dataset_file):
            vote_type = row["Vote Type"]
            row["Country"] = "Sri Lanka"
            row["Election Commission"] = "Sri Lanka Election Commission"

            country = _get_country_entry(row=row)
            province = _get_province_entry(row=row)
            administrative_district = _get_administrative_district_entry(row=row)
            election_commission = _get_election_commission_entry(row=row)
            district_centre = _get_district_centre_entry(row=row)
            postal_vote_counting_centre = _get_administrative_district_counting_centre_entry(row=row)

            country.add_child(province.areaId)
            province.add_child(administrative_district.areaId)
            election_commission.add_child(district_centre.areaId)
            district_centre.add_child(postal_vote_counting_centre.areaId)
            administrative_district.add_child(postal_vote_counting_centre.areaId)

            AreaMap.create(
                electionId=root_election.electionId,
                voteType=vote_type,
                countingCentreId=postal_vote_counting_centre.areaId,
                districtCentreId=district_centre.areaId,
                electionCommissionId=election_commission.areaId,
                administrativeDistrictId=administrative_district.areaId,
                provinceId=province.areaId,
                countryId=country.areaId
            )

        for row in get_rows_from_csv(number_of_seats_dataset_file):
            province_election = _get_province_election(row)
            province_election.meta.add_meta_data(
                metaDataKey=META_DATA_KEY_ELECTION_NUMBER_OF_BONUS_SEATS_ALLOCATED,
                metaDataValue=row["Bonus seats"]
            )

            administrative_district_election = _get_administrative_district_election(row)
            administrative_district_election.meta.add_meta_data(
                metaDataKey=META_DATA_KEY_ELECTION_NUMBER_OF_SEATS_ALLOCATED,
                metaDataValue=row["Number of seats"]
            )
            administrative_district_election.meta.add_meta_data(
                metaDataKey=META_DATA_KEY_ELECTION_NUMBER_OF_VALID_VOTE_PERCENTAGE_REQUIRED_FOR_SEAT_ALLOCATION,
                metaDataValue=0.05
            )

        # extract_csv_files()

        db.session.commit()

        return root_election

    def get_root_token(self):
        return get_root_token.get_root_token(self)
