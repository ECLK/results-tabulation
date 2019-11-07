import connexion

from orm.enums import TallySheetCodeEnum, BallotTypeEnum, AreaTypeEnum
from sqlalchemy import func


class RequestBody:
    def __init__(self, body):
        self.body = body

    def get(self, property_name):
        if property_name in self.body:
            return self.body[property_name]
        else:
            return None


class Auth:
    def get_user_id(self):
        return 2


def get_paginated_query(query):
    if "limit" in connexion.request.args and connexion.request.args["limit"] is not None:
        query = query.limit(connexion.request.args["limit"])

    if "offset" in connexion.request.args and connexion.request.args["offset"] is not None:
        query = query.offset(connexion.request.args["offset"])

    return query


def get_array(array_or_value):
    if array_or_value is None:
        return []
    elif isinstance(array_or_value, list) is False:
        return [array_or_value]
    else:
        return array_or_value


def get_ballot_type(ballot_type_str):
    if ballot_type_str == "Ordinary":
        return BallotTypeEnum.Ordinary
    elif ballot_type_str == "Tendered":
        return BallotTypeEnum.Tendered


def get_tally_sheet_code(tally_sheet_code_str):
    if tally_sheet_code_str == "CE-201":
        return TallySheetCodeEnum.CE_201
    elif tally_sheet_code_str == "CE-201-PV":
        return TallySheetCodeEnum.CE_201_PV
    elif tally_sheet_code_str == "PRE-41":
        return TallySheetCodeEnum.PRE_41
    elif tally_sheet_code_str == "PRE-21":
        return TallySheetCodeEnum.PRE_21
    elif tally_sheet_code_str == "PRE-30-PD":
        return TallySheetCodeEnum.PRE_30_PD
    elif tally_sheet_code_str == "PRE-30-PD-PV":
        return TallySheetCodeEnum.PRE_30_PD_PV
    elif tally_sheet_code_str == "PRE-30-ED":
        return TallySheetCodeEnum.PRE_30_ED
    elif tally_sheet_code_str == "PRE-34-CO":
        return TallySheetCodeEnum.PRE_34_CO
    elif tally_sheet_code_str == "PRE-34-I-RO":
        return TallySheetCodeEnum.PRE_34_I_RO
    elif tally_sheet_code_str == "PRE-34-II-RO":
        return TallySheetCodeEnum.PRE_34_II_RO
    elif tally_sheet_code_str == "PRE-34":
        return TallySheetCodeEnum.PRE_34
    elif tally_sheet_code_str == "PRE-ALL-ISLAND-RESULTS":
        return TallySheetCodeEnum.PRE_ALL_ISLAND_RESULTS
    elif tally_sheet_code_str == "PRE-ALL-ISLAND-RESULTS-BY-ELECTORAL-DISTRICTS":
        return TallySheetCodeEnum.PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS


def get_tally_sheet_code_string(tally_sheet_code):
    if tally_sheet_code is TallySheetCodeEnum.CE_201:
        return "CE-201"
    elif tally_sheet_code is TallySheetCodeEnum.CE_201_PV:
        return "CE-201-PV"
    elif tally_sheet_code is TallySheetCodeEnum.PRE_41:
        return "PRE-41"
    elif tally_sheet_code is TallySheetCodeEnum.PRE_21:
        return "PRE-21"
    elif tally_sheet_code is TallySheetCodeEnum.PRE_30_PD:
        return "PRE-30-PD"
    elif tally_sheet_code is TallySheetCodeEnum.PRE_30_PD_PV:
        return "PRE-30-PD-PV"
    elif tally_sheet_code is TallySheetCodeEnum.PRE_30_ED:
        return "PRE-30-ED"
    elif tally_sheet_code is TallySheetCodeEnum.PRE_34_CO:
        return "PRE-34-CO"
    elif tally_sheet_code is TallySheetCodeEnum.PRE_34_I_RO:
        return "PRE-34-I-RO"
    elif tally_sheet_code is TallySheetCodeEnum.PRE_34_II_RO:
        return "PRE-34-II-RO"
    elif tally_sheet_code is TallySheetCodeEnum.PRE_34:
        return "PRE-34"
    elif tally_sheet_code is TallySheetCodeEnum.PRE_ALL_ISLAND_RESULTS:
        return "PRE-ALL-ISLAND-RESULTS"
    elif tally_sheet_code is TallySheetCodeEnum.PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS:
        return "PRE-ALL-ISLAND-RESULTS-BY-ELECTORAL-DISTRICTS"


def get_tally_sheet_version_class(tally_sheet_version_code):
    from orm.entities.SubmissionVersion.TallySheetVersion import TallySheetVersionPRE41, TallySheetVersion_CE_201_PV, \
        TallySheetVersionCE201, TallySheetVersionPRE21, TallySheetVersion_PRE_30_PD, TallySheetVersion_PRE_34_CO \
        , TallySheetVersion_PRE_30_ED, \
        TallySheetVersion_PRE_ALL_ISLAND_RESULT, TallySheetVersion_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS

    if tally_sheet_version_code is TallySheetCodeEnum.CE_201:
        return TallySheetVersionCE201
    elif tally_sheet_version_code is TallySheetCodeEnum.CE_201_PV:
        return TallySheetVersion_CE_201_PV
    elif tally_sheet_version_code is TallySheetCodeEnum.PRE_41:
        return TallySheetVersionPRE41
    elif tally_sheet_version_code is TallySheetCodeEnum.PRE_21:
        return TallySheetVersionPRE21
    elif tally_sheet_version_code is TallySheetCodeEnum.PRE_30_PD:
        return TallySheetVersion_PRE_30_PD
    elif tally_sheet_version_code is TallySheetCodeEnum.PRE_30_PD_PV:
        return TallySheetVersion_PRE_30_PD
    elif tally_sheet_version_code is TallySheetCodeEnum.PRE_30_ED:
        return TallySheetVersion_PRE_30_ED
    elif tally_sheet_version_code is TallySheetCodeEnum.PRE_34_CO:
        return TallySheetVersion_PRE_34_CO
    elif tally_sheet_version_code is TallySheetCodeEnum.PRE_ALL_ISLAND_RESULTS:
        return TallySheetVersion_PRE_ALL_ISLAND_RESULT
    elif tally_sheet_version_code is TallySheetCodeEnum.PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS:
        return TallySheetVersion_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS


def sqlalchemy_num_or_zero(column):
    return func.IF(
        column == None, 0,
        column
    )


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


def to_empty_string_or_value(value):
    if value is None:
        return ""
    else:
        return value


def to_percentage(value, round_to=2):
    if value is None:
        return "%"
    else:
        return f'{round(value, round_to)}%'


def to_comma_seperated_num(value):
    if value is None:
        return ""
    else:
        return f'{value:,}'
