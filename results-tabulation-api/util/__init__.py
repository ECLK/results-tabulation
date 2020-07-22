import math

import connexion

from orm.enums import BallotTypeEnum, AreaTypeEnum
from sqlalchemy import func
import base64
import numpy as np


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


def to_comma_seperated_num(value, num_type=int, round_to=2):
    if value is None:
        return ""
    else:
        try:
            if np.isnan(value):
                return ""
        except Exception as e:
            pass

        return f'{round(num_type(value), round_to):,}'


def convert_image_to_data_uri(value):
    data_image = ''

    with open(value, "rb") as img_file:
        data_image = base64.b64encode(img_file.read()).decode()

    return data_image


def get_dict_key_value_or_none(dict, key):
    if key in dict:
        return dict[key]
    else:
        return None


def split_area_name(name):
    split_array = name.split("-")
    if len(split_array) == 2:
        return split_array[0].strip(), split_array[1].strip()
    print("Error: invalid are name", name)
    return "None", name


def get_sum_of_numbers_only_and_nan_otherwise(array):
    result = np.nan
    for val in array:
        if val is not None and not math.isnan(val):
            if math.isnan(result):
                result = val
            else:
                result += val

    return result


def get_sum_of_all_and_nan_otherwise(array):
    result = np.nan
    for val in array:
        if val is not None and not math.isnan(val):
            result = np.nan
            break

        if math.isnan(result):
            result = val
        else:
            result += val

    return result


def validate_tally_sheet_version_request_content_special_characters(content_array):
    invalid_strings = ["'", "\"", "<", ">", "=", ",", ";"]
    for array_item in content_array:
        if "strValue" in array_item:
            text_value = str(array_item["strValue"])
            for char in invalid_strings:
                if char in text_value or len(text_value) > 500:
                    return False, char + " included in " + text_value
    return True, ""
