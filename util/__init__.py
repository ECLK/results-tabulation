import connexion

from orm.enums import TallySheetCodeEnum, BallotTypeEnum


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


def get_ballot_type(ballotTypeStr):
    if ballotTypeStr == "Ordinary":
        return BallotTypeEnum.Ordinary
    elif ballotTypeStr == "Tendered":
        return BallotTypeEnum.Tendered


def get_tally_sheet_code(tallySheetCodeStr):
    if tallySheetCodeStr == "CE-201":
        return TallySheetCodeEnum.CE_201
    elif tallySheetCodeStr == "PRE-41":
        return TallySheetCodeEnum.PRE_41
    elif tallySheetCodeStr == "PRE-21":
        return TallySheetCodeEnum.PRE_21
    elif tallySheetCodeStr == "PRE-30-PD":
        return TallySheetCodeEnum.PRE_30_PD
    elif tallySheetCodeStr == "PRE-30-ED":
        return TallySheetCodeEnum.PRE_30_ED
    elif tallySheetCodeStr == "PRE_ALL_ISLAND_RESULTS":
        return TallySheetCodeEnum.PRE_ALL_ISLAND_RESULTS
