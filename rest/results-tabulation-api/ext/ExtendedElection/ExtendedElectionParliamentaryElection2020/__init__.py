from app import db
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.TALLY_SHEET_CODES import PE_27, PE_4, PE_CE_RO_V1, \
    PE_R1, PE_CE_RO_PR_1, \
    PE_CE_RO_V2, PE_R2, PE_CE_RO_PR_2, PE_CE_RO_PR_3, CE_201, CE_201_PV
from constants.VOTE_TYPES import Postal, NonPostal
from ext import TallySheetMap
from ext.ExtendedElection import ExtendedElection
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020 import RoleBasedAccess
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.ExtendedTallySheetVersion.ExtendedTallySheetVersion_PE_CE_RO_V1 import \
    ExtendedTallySheetVersion_PE_CE_RO_V1
from ext.ExtendedElection.ExtendedElectionParliamentaryElection2020.ExtendedTallySheetVersion.ExtendedTallySheetVersion_PE_R1 import \
    ExtendedTallySheetVersion_PE_R1
from ext.ExtendedElection.util import get_rows_from_csv, update_dashboard_tables
from orm.entities import Election, Candidate, Template, Party
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
            PE_R1: ExtendedTallySheetVersion_PE_R1
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
                {"columnName": "electionId", "grouped": False, "func": None},
                {"columnName": "areaId", "grouped": False, "func": None},
                {"columnName": "ballotBoxId", "grouped": False, "func": None}
            ]
        )
        tally_sheet_template_ce_201_number_of_ballots_received = tally_sheet_template_ce_201.add_row(
            templateRowType="NUMBER_OF_BALLOTS_RECEIVED",
            hasMany=True,
            isDerived=False,
            columns=[
                {"columnName": "electionId", "grouped": False, "func": None},
                {"columnName": "areaId", "grouped": False, "func": None},
                {"columnName": "numValue", "grouped": False, "func": None}
            ]
        )
        tally_sheet_template_ce_201_number_of_ballots_spoilt = tally_sheet_template_ce_201.add_row(
            templateRowType="NUMBER_OF_BALLOTS_SPOILT",
            hasMany=True,
            isDerived=False,
            columns=[
                {"columnName": "electionId", "grouped": False, "func": None},
                {"columnName": "areaId", "grouped": False, "func": None},
                {"columnName": "numValue", "grouped": False, "func": None}
            ]
        )
        tally_sheet_template_ce_201_number_of_ballots_issued = tally_sheet_template_ce_201.add_row(
            templateRowType="NUMBER_OF_BALLOTS_ISSUED",
            hasMany=True,
            isDerived=False,
            columns=[
                {"columnName": "electionId", "grouped": False, "func": None},
                {"columnName": "areaId", "grouped": False, "func": None},
                {"columnName": "numValue", "grouped": False, "func": None}
            ]
        )
        tally_sheet_template_ce_201_number_of_ballots_unused = tally_sheet_template_ce_201.add_row(
            templateRowType="NUMBER_OF_BALLOTS_UNUSED",
            hasMany=True,
            isDerived=False,
            columns=[
                {"columnName": "electionId", "grouped": False, "func": None},
                {"columnName": "areaId", "grouped": False, "func": None},
                {"columnName": "numValue", "grouped": False, "func": None}
            ]
        )
        tally_sheet_template_ce_201_number_of_ordinary_ballots_in_ballot_paper_account = tally_sheet_template_ce_201.add_row(
            templateRowType="NUMBER_OF_ORDINARY_BALLOTS_IN_BALLOT_PAPER_ACCOUNT",
            hasMany=True,
            isDerived=False,
            columns=[
                {"columnName": "electionId", "grouped": False, "func": None},
                {"columnName": "areaId", "grouped": False, "func": None},
                {"columnName": "numValue", "grouped": False, "func": None}
            ]
        )
        tally_sheet_template_ce_201_number_of_ordinary_ballots_in_ballot_box = tally_sheet_template_ce_201.add_row(
            templateRowType="NUMBER_OF_ORDINARY_BALLOTS_IN_BALLOT_BOX",
            hasMany=True,
            isDerived=False,
            columns=[
                {"columnName": "electionId", "grouped": False, "func": None},
                {"columnName": "areaId", "grouped": False, "func": None},
                {"columnName": "numValue", "grouped": False, "func": None}
            ]
        )
        tally_sheet_template_ce_201_number_of_tendered_ballots_in_ballot_paper_account = tally_sheet_template_ce_201.add_row(
            templateRowType="NUMBER_OF_TENDERED_BALLOTS_IN_BALLOT_PAPER_ACCOUNT",
            hasMany=True,
            isDerived=False,
            columns=[
                {"columnName": "electionId", "grouped": False, "func": None},
                {"columnName": "areaId", "grouped": False, "func": None},
                {"columnName": "numValue", "grouped": False, "func": None}
            ]
        )
        tally_sheet_template_ce_201_number_of_tendered_ballots_in_ballot_box = tally_sheet_template_ce_201.add_row(
            templateRowType="NUMBER_OF_TENDERED_BALLOTS_IN_BALLOT_BOX",
            hasMany=True,
            isDerived=False,
            columns=[
                {"columnName": "electionId", "grouped": False, "func": None},
                {"columnName": "areaId", "grouped": False, "func": None},
                {"columnName": "numValue", "grouped": False, "func": None}
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
                {"columnName": "electionId", "grouped": False, "func": None},
                {"columnName": "areaId", "grouped": False, "func": None},
                {"columnName": "strValue", "grouped": False, "func": None}
            ]
        )
        tally_sheet_template_ce_201_pv_time_of_commencement_row = tally_sheet_template_ce_201_pv.add_row(
            templateRowType="TIME_OF_COMMENCEMENT",
            hasMany=False,
            isDerived=False,
            columns=[
                {"columnName": "electionId", "grouped": False, "func": None},
                {"columnName": "areaId", "grouped": False, "func": None},
                {"columnName": "strValue", "grouped": False, "func": None}
            ]
        )
        tally_sheet_template_ce_201_pv_ballot_box_row = tally_sheet_template_ce_201_pv.add_row(
            templateRowType="BALLOT_BOX",
            hasMany=True,
            isDerived=False,
            columns=[
                {"columnName": "electionId", "grouped": False, "func": None},
                {"columnName": "areaId", "grouped": False, "func": None},
                {"columnName": "ballotBoxId", "grouped": False, "func": None}
            ]
        )
        tally_sheet_template_ce_201_pv_number_of_packets_inserted_to_ballot_box_row = tally_sheet_template_ce_201_pv.add_row(
            templateRowType="NUMBER_OF_PACKETS_INSERTED_TO_BALLOT_BOX",
            hasMany=True,
            isDerived=False,
            columns=[
                {"columnName": "electionId", "grouped": False, "func": None},
                {"columnName": "areaId", "grouped": False, "func": None},
                {"columnName": "numValue", "grouped": False, "func": None}
            ]
        )
        tally_sheet_template_ce_201_pv_number_of_packets_found_inside_ballot_box_row = tally_sheet_template_ce_201_pv.add_row(
            templateRowType="NUMBER_OF_PACKETS_FOUND_INSIDE_BALLOT_BOX",
            hasMany=True,
            isDerived=False,
            columns=[
                {"columnName": "electionId", "grouped": False, "func": None},
                {"columnName": "areaId", "grouped": False, "func": None},
                {"columnName": "numValue", "grouped": False, "func": None}
            ]
        )
        tally_sheet_template_ce_201_pv_number_of_packets_rejected_after_opening_cover_a_row = tally_sheet_template_ce_201_pv.add_row(
            templateRowType="NUMBER_OF_PACKETS_REJECTED_AFTER_OPENING_COVER_A",
            hasMany=False,
            isDerived=False,
            columns=[
                {"columnName": "electionId", "grouped": False, "func": None},
                {"columnName": "areaId", "grouped": False, "func": None},
                {"columnName": "numValue", "grouped": False, "func": None}
            ]
        )
        tally_sheet_template_ce_201_pv_number_of_packets_rejected_after_opening_cover_b_row = tally_sheet_template_ce_201_pv.add_row(
            templateRowType="NUMBER_OF_PACKETS_REJECTED_AFTER_OPENING_COVER_B",
            hasMany=False,
            isDerived=False,
            columns=[
                {"columnName": "electionId", "grouped": False, "func": None},
                {"columnName": "areaId", "grouped": False, "func": None},
                {"columnName": "numValue", "grouped": False, "func": None}
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
                {"columnName": "electionId", "grouped": False, "func": None},
                {"columnName": "areaId", "grouped": False, "func": None},
                {"columnName": "partyId", "grouped": False, "func": None},
                {"columnName": "numValue", "grouped": False, "func": None},
                {"columnName": "strValue", "grouped": False, "func": None}
            ]
        )
        tally_sheet_template_pe_27_rejected_vote_row = tally_sheet_template_pe_27.add_row(
            templateRowType="REJECTED_VOTE",
            hasMany=False,
            isDerived=False,
            columns=[
                {"columnName": "electionId", "grouped": False, "func": None},
                {"columnName": "areaId", "grouped": False, "func": None},
                {"columnName": "numValue", "grouped": False, "func": None}
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
                {"columnName": "electionId", "grouped": True, "func": None},
                {"columnName": "areaId", "grouped": True, "func": None},
                {"columnName": "partyId", "grouped": True, "func": None},
                {"columnName": "numValue", "grouped": False, "func": "sum"}
            ]
        ).add_derivative_template_row(tally_sheet_template_pe_27_party_wise_vote_row)
        tally_sheet_template_pe_ce_ro_v1_rejected_vote_row = tally_sheet_template_pe_ce_ro_v1.add_row(
            templateRowType="REJECTED_VOTE",
            hasMany=True,
            isDerived=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None},
                {"columnName": "areaId", "grouped": True, "func": None},
                {"columnName": "numValue", "grouped": False, "func": "sum"}
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
                {"columnName": "electionId", "grouped": True, "func": None},
                {"columnName": "areaId", "grouped": True, "func": None},
                {"columnName": "partyId", "grouped": True, "func": None},
                {"columnName": "numValue", "grouped": False, "func": "sum"}
            ]
        ).add_derivative_template_row(tally_sheet_template_pe_ce_ro_v1_party_wise_vote_row)
        tally_sheet_template_pe_r1_rejected_vote_row = tally_sheet_template_pe_r1.add_row(
            templateRowType="REJECTED_VOTE",
            hasMany=True,
            isDerived=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None},
                {"columnName": "areaId", "grouped": True, "func": None},
                {"columnName": "numValue", "grouped": False, "func": "sum"}
            ]
        ).add_derivative_template_row(tally_sheet_template_pe_ce_ro_v1_rejected_vote_row)

        tally_sheet_template_pe_ce_ro_v2 = Template.create(
            templateName=PE_CE_RO_V2
        )
        tally_sheet_template_pe_ce_ro_v2_party_wise_vote_row = tally_sheet_template_pe_ce_ro_v2.add_row(
            templateRowType="CANDIDATE_FIRST_PREFERENCE",
            hasMany=True,
            isDerived=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None},
                {"columnName": "areaId", "grouped": True, "func": None},
                {"columnName": "partyId", "grouped": True, "func": None},
                {"columnName": "numValue", "grouped": False, "func": "sum"}
            ]
        ).add_derivative_template_row(tally_sheet_template_pe_ce_ro_v1_party_wise_vote_row)
        tally_sheet_template_pe_ce_ro_v2_rejected_vote_row = tally_sheet_template_pe_ce_ro_v2.add_row(
            templateRowType="REJECTED_VOTE",
            hasMany=True,
            isDerived=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None},
                {"columnName": "areaId", "grouped": True, "func": None},
                {"columnName": "numValue", "grouped": False, "func": "sum"}
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
                {"columnName": "electionId", "grouped": True, "func": None},
                {"columnName": "areaId", "grouped": True, "func": None},
                {"columnName": "partyId", "grouped": True, "func": None},
                {"columnName": "numValue", "grouped": False, "func": "sum"}
            ]
        ).add_derivative_template_row(tally_sheet_template_pe_ce_ro_v2_party_wise_vote_row)
        tally_sheet_template_pe_r2_rejected_vote_row = tally_sheet_template_pe_r2.add_row(
            templateRowType="REJECTED_VOTE",
            hasMany=True,
            isDerived=True,
            columns=[
                {"columnName": "electionId", "grouped": True, "func": None},
                {"columnName": "areaId", "grouped": True, "func": None},
                {"columnName": "numValue", "grouped": False, "func": "sum"}
            ]
        ).add_derivative_template_row(tally_sheet_template_pe_ce_ro_v2_rejected_vote_row)

        tally_sheet_template_pe_4 = Template.create(
            templateName=PE_4
        )
        tally_sheet_template_pe_4_candidate_wise_first_preference_row = tally_sheet_template_pe_4.add_row(
            templateRowType="CANDIDATE_FIRST_PREFERENCE",
            hasMany=True,
            isDerived=False,
            columns=[
                {"columnName": "electionId", "grouped": False, "func": None},
                {"columnName": "areaId", "grouped": False, "func": None},
                {"columnName": "partyId", "grouped": False, "func": None},
                {"columnName": "candidateId", "grouped": False, "func": None},
                {"columnName": "numValue", "grouped": False, "func": None}
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
                {"columnName": "electionId", "grouped": True, "func": None},
                {"columnName": "areaId", "grouped": True, "func": None},
                {"columnName": "partyId", "grouped": True, "func": None},
                {"columnName": "candidateId", "grouped": True, "func": None},
                {"columnName": "numValue", "grouped": False, "func": "sum"}
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
                {"columnName": "electionId", "grouped": True, "func": None},
                {"columnName": "areaId", "grouped": True, "func": None},
                {"columnName": "partyId", "grouped": True, "func": None},
                {"columnName": "candidateId", "grouped": True, "func": None},
                {"columnName": "numValue", "grouped": False, "func": "sum"}
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
                {"columnName": "electionId", "grouped": True, "func": None},
                {"columnName": "areaId", "grouped": True, "func": None},
                {"columnName": "partyId", "grouped": True, "func": None},
                {"columnName": "candidateId", "grouped": True, "func": None},
                {"columnName": "numValue", "grouped": False, "func": "sum"}
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
                tally_sheets = []

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
                        template=tally_sheet_template_pe_ce_ro_v2, electionId=election.electionId,
                        areaId=area.areaId
                    ),
                    TallySheet.create(
                        template=tally_sheet_template_pe_r2, electionId=election.electionId,
                        areaId=area.areaId
                    ),
                    TallySheet.create(
                        template=tally_sheet_template_pe_ce_ro_v1, electionId=postal_election.electionId,
                        areaId=area.areaId
                    ),
                    TallySheet.create(
                        template=tally_sheet_template_pe_r1, electionId=postal_election.electionId,
                        areaId=area.areaId
                    ),
                    TallySheet.create(
                        template=tally_sheet_template_pe_ce_ro_pr_1, electionId=postal_election.electionId,
                        areaId=area.areaId
                    ),
                    TallySheet.create(
                        template=tally_sheet_template_pe_ce_ro_pr_2, electionId=election.electionId,
                        areaId=area.areaId
                    ),
                    TallySheet.create(
                        template=tally_sheet_template_pe_ce_ro_pr_3, electionId=election.electionId,
                        areaId=area.areaId
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
                        template=tally_sheet_template_pe_ce_ro_v1, electionId=ordinary_election.electionId,
                        areaId=area.areaId
                    ),
                    TallySheet.create(
                        template=tally_sheet_template_pe_r1, electionId=ordinary_election.electionId,
                        areaId=area.areaId
                    ),
                    TallySheet.create(
                        template=tally_sheet_template_pe_ce_ro_pr_1, electionId=ordinary_election.electionId,
                        areaId=area.areaId
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
                        template=tally_sheet_template_pe_27, electionId=election.electionId, areaId=area.areaId
                    ),
                    TallySheet.create(
                        template=tally_sheet_template_pe_4, electionId=election.electionId,
                        areaId=area.areaId
                    )
                ]

                if election.voteType is NonPostal:
                    tally_sheets.append(TallySheet.create(
                        template=tally_sheet_template_ce_201, electionId=election.electionId, areaId=area.areaId
                    ))
                elif election.voteType is Postal:
                    area._registeredVotersCount = row["Registered Voters"]
                    tally_sheets.append(TallySheet.create(
                        template=tally_sheet_template_ce_201_pv, electionId=election.electionId,
                        areaId=area.areaId
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

            pe_27_tally_sheet = counting_centre_entry["tallySheets"][PE_27][0]
            pe_4_tally_sheet = counting_centre_entry["tallySheets"][PE_4][0]

            pe_ce_ro_v1_tally_sheet = polling_division_entry["tallySheets"][PE_CE_RO_V1][0]
            pe_r1_tally_sheet = polling_division_entry["tallySheets"][PE_R1][0]
            pe_ce_ro_pr_1_tally_sheet = polling_division_entry["tallySheets"][PE_CE_RO_PR_1][0]

            pe_ce_ro_v2_tally_sheet = electoral_district_entry["tallySheets"][PE_CE_RO_V2][0]
            pe_r2_tally_sheet = electoral_district_entry["tallySheets"][PE_R2][0]
            pe_ce_ro_pr_2_tally_sheet = electoral_district_entry["tallySheets"][PE_CE_RO_PR_2][0]
            pe_ce_ro_pr_3_tally_sheet = electoral_district_entry["tallySheets"][PE_CE_RO_PR_3][0]

            pe_ce_ro_v1_tally_sheet.add_child(pe_27_tally_sheet)
            pe_r1_tally_sheet.add_child(pe_ce_ro_v1_tally_sheet)
            pe_ce_ro_v2_tally_sheet.add_child(pe_ce_ro_v1_tally_sheet)
            pe_r2_tally_sheet.add_child(pe_ce_ro_v2_tally_sheet)

            pe_ce_ro_pr_1_tally_sheet.add_child(pe_4_tally_sheet)
            pe_ce_ro_pr_2_tally_sheet.add_child(pe_ce_ro_pr_1_tally_sheet)
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

            pe_27_tally_sheet = counting_centre_entry["tallySheets"][PE_27][0]
            pe_4_tally_sheet = counting_centre_entry["tallySheets"][PE_4][0]

            pe_ce_ro_v1_tally_sheet = electoral_district_entry["tallySheets"][PE_CE_RO_V1][0]
            pe_r1_tally_sheet = electoral_district_entry["tallySheets"][PE_R1][0]
            pe_ce_ro_pr_1_tally_sheet = electoral_district_entry["tallySheets"][PE_CE_RO_PR_1][0]

            pe_ce_ro_v2_tally_sheet = electoral_district_entry["tallySheets"][PE_CE_RO_V2][0]
            pe_r2_tally_sheet = electoral_district_entry["tallySheets"][PE_R2][0]
            pe_ce_ro_pr_2_tally_sheet = electoral_district_entry["tallySheets"][PE_CE_RO_PR_2][0]
            pe_ce_ro_pr_3_tally_sheet = electoral_district_entry["tallySheets"][PE_CE_RO_PR_3][0]

            pe_ce_ro_v1_tally_sheet.add_child(pe_27_tally_sheet)
            pe_r1_tally_sheet.add_child(pe_ce_ro_v1_tally_sheet)
            pe_ce_ro_v2_tally_sheet.add_child(pe_ce_ro_v1_tally_sheet)
            pe_r2_tally_sheet.add_child(pe_ce_ro_v2_tally_sheet)

            pe_ce_ro_pr_1_tally_sheet.add_child(pe_4_tally_sheet)
            pe_ce_ro_pr_2_tally_sheet.add_child(pe_ce_ro_pr_1_tally_sheet)
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

        db.session.commit()

        update_dashboard_tables()

        return root_election
