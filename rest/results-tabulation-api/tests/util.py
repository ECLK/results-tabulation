from orm.enums import AreaTypeEnum
from ext.ExtendedElection.ExtendedElectionPresidentialElection2019.TALLY_SHEET_CODES import PRE_41, PRE_30_PD, \
    PRE_30_ED, PRE_21, PRE_34_CO, PRE_34_I_RO, PRE_34_II_RO, PRE_34, PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS, \
    PRE_ALL_ISLAND_RESULTS, CE_201_PV, PRE_30_PD_PV, CE_201, PRE_34_PD, PRE_34_ED, PRE_34_AI


def get_tally_sheet_code(tally_sheet_code_str):
    if tally_sheet_code_str == "CE-201":
        return CE_201
    elif tally_sheet_code_str == "CE-201-PV":
        return CE_201_PV
    elif tally_sheet_code_str == "PRE-41":
        return PRE_41
    elif tally_sheet_code_str == "PRE-21":
        return PRE_21
    elif tally_sheet_code_str == "PRE-30-PD":
        return PRE_30_PD
    elif tally_sheet_code_str == "PRE-30-PD-PV":
        return PRE_30_PD_PV
    elif tally_sheet_code_str == "PRE-30-ED":
        return PRE_30_ED
    elif tally_sheet_code_str == "PRE-34-CO":
        return PRE_34_CO
    elif tally_sheet_code_str == "PRE-34-I-RO":
        return PRE_34_I_RO
    elif tally_sheet_code_str == "PRE-34-II-RO":
        return PRE_34_II_RO
    elif tally_sheet_code_str == "PRE-34":
        return PRE_34
    elif tally_sheet_code_str == "PRE-ALL-ISLAND-RESULTS":
        return PRE_ALL_ISLAND_RESULTS
    elif tally_sheet_code_str == "PRE-ALL-ISLAND-RESULTS-BY-ELECTORAL-DISTRICTS":
        return PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS
    elif tally_sheet_code_str == "PRE-34-PD":
        return PRE_34_PD
    elif tally_sheet_code_str == "PRE-34-ED":
        return PRE_34_ED
    elif tally_sheet_code_str == "PRE-34-AI":
        return PRE_34_AI


def get_area_type(area_type):
    if area_type == "Country":
        return AreaTypeEnum.Country
    elif area_type == "ElectoralDistrict":
        return AreaTypeEnum.ElectoralDistrict
    elif area_type == "PollingDivision":
        return AreaTypeEnum.PollingDivision
    elif area_type == "PollingDistrict":
        return AreaTypeEnum.PollingDistrict
    elif area_type == "PollingStation":
        return AreaTypeEnum.PollingStation
    elif area_type == "CountingCentre":
        return AreaTypeEnum.CountingCentre
    elif area_type == "PostalVoteCountingCentre":
        return AreaTypeEnum.PostalVoteCountingCentre
    elif area_type == "DistrictCentre":
        return AreaTypeEnum.DistrictCentre
    elif area_type == "ElectionCommission":
        return AreaTypeEnum.ElectionCommission
    elif area_type == "AdministrativeDistrict":
        return AreaTypeEnum.AdministrativeDistrict
