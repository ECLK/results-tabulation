from typing import Dict, Set

from flask import request
import connexion
from decorator import decorator
from jose import jwt

from app import db, cache
from auth.AuthConstants import EC_LEADERSHIP_ROLE, NATIONAL_REPORT_GENERATOR_ROLE, NATIONAL_REPORT_VIEWER_ROLE, \
    SUB, DATA_EDITOR_ROLE, POLLING_DIVISION_REPORT_VIEWER_ROLE, POLLING_DIVISION_REPORT_GENERATOR_ROLE, \
    ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE, ELECTORAL_DISTRICT_REPORT_GENERATOR_ROLE, ROLE_CLAIM_PREFIX, ADMIN_ROLE, \
    JWT_TOKEN_HEADER_KEY
from exception import UnauthorizedException
import json

JWT_SECRET = "jwt_secret"
AREA_ID = "areaId"
USER_ACCESS_AREA_IDS = "userAccessAreaIds"
USER_NAME = "userName"


@cache.cached(key_prefix='global_area_map')
def init_global_area_map():
    # TODO Refactor

    print("############# init_global_area_map ###############")
    from orm.entities import Area
    from orm.enums import AreaTypeEnum

    global_area_map = {}

    electoral_districts = Area.get_all(area_type=AreaTypeEnum.ElectoralDistrict)
    global_area_map["electoral_district_counting_centre"] = {}
    for electoral_district in electoral_districts:
        counting_centre_area_ids = [
            counting_centre.areaId for counting_centre in
            electoral_district.get_associated_areas(areaType=AreaTypeEnum.CountingCentre)
        ]
        global_area_map["electoral_district_counting_centre"][electoral_district.areaId] = counting_centre_area_ids

    global_area_map["electoral_district_polling_division"] = {}
    for electoral_district in electoral_districts:
        polling_division_area_ids = [
            polling_division.areaId for polling_division in
            electoral_district.get_associated_areas(areaType=AreaTypeEnum.PollingDivision)
        ]
        global_area_map["electoral_district_polling_division"][
            electoral_district.areaId] = polling_division_area_ids

    print("############# init_global_area_map ###############", global_area_map)

    return global_area_map


def decode_token(token):
    try:
        token = jwt.decode(
            token, key=JWT_SECRET,
            options={"verify_signature": False, "verify_exp": False}
        )

        return token
    except Exception as e:
        raise UnauthorizedException("Invalid authorization token.")


def get_jwt_token():
    if JWT_TOKEN_HEADER_KEY not in request.headers:
        raise UnauthorizedException("No authorization header found.")

    return request.headers.get(JWT_TOKEN_HEADER_KEY)


def get_claims() -> Dict[str, Dict]:
    """
    Gets all user role related claims from all the claims in token_info.

    Decoded JWT information are set to connexion.context['token_info'] by the security decorators in connexion.

    :return: dict of claim id to claim value.
    """

    claims: dict = decode_token(get_jwt_token())
    filtered_claims = {}

    area_assignment_claim_keys = [
        ROLE_CLAIM_PREFIX + ADMIN_ROLE,
        ROLE_CLAIM_PREFIX + DATA_EDITOR_ROLE,
        ROLE_CLAIM_PREFIX + POLLING_DIVISION_REPORT_VIEWER_ROLE,
        ROLE_CLAIM_PREFIX + POLLING_DIVISION_REPORT_GENERATOR_ROLE,
        ROLE_CLAIM_PREFIX + ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE,
        ROLE_CLAIM_PREFIX + ELECTORAL_DISTRICT_REPORT_GENERATOR_ROLE,
        ROLE_CLAIM_PREFIX + NATIONAL_REPORT_VIEWER_ROLE,
        ROLE_CLAIM_PREFIX + NATIONAL_REPORT_GENERATOR_ROLE,
        ROLE_CLAIM_PREFIX + EC_LEADERSHIP_ROLE
    ]
    for area_assignment_claim_key in area_assignment_claim_keys:
        if area_assignment_claim_key in claims.keys():
            area_assignment_claim_value = claims.get(area_assignment_claim_key)
            area_assignment_claim_value = area_assignment_claim_value.replace("\'", "\"")
            filtered_claims[area_assignment_claim_key] = json.loads(area_assignment_claim_value)

    if SUB in claims.keys():
        filtered_claims[SUB] = claims.get(SUB)

    return filtered_claims


def get_ip() -> str:
    return request.remote_addr


def get_user_name() -> str:
    """
    Gets user namefrom connexion context.

    :return: string user name
    """
    return connexion.context[USER_NAME]


def get_user_access_area_ids() -> Set[int]:
    """
    Gets user access area ids from connexion context.

    :return: set of user access area ids
    """
    return connexion.context[USER_ACCESS_AREA_IDS]


@decorator
def authenticate(func, *args, **kwargs):
    # print("\n\n\n\n####### request.headers ### [START]")
    # print(request.headers)
    # print("####### request.headers ### [END]\n\n\n")

    claims: Dict = get_claims()

    if SUB not in claims:
        UnauthorizedException("No valid user found.")
    else:
        user_name = claims.get(SUB)
        connexion.context[USER_NAME] = user_name
        return func(*args, **kwargs)


@decorator
@authenticate
def authorize(func, required_roles=None, *args, **kwargs):
    from orm.entities import Area
    from orm.enums import AreaTypeEnum

    if required_roles is None:
        return func(*args, **kwargs)

    claims: Dict = get_claims()

    claim_found = False
    user_access_area_ids = []

    for role in required_roles:
        claim = ROLE_CLAIM_PREFIX + role

        if claim not in claims.keys():
            continue

        claim_found = True
        user_access_area_ids.extend([x.get(AREA_ID) for x in claims.get(claim)])

        if role is DATA_EDITOR_ROLE:
            global_area_map = init_global_area_map()
            for electoral_district_id in user_access_area_ids:
                if electoral_district_id in global_area_map["electoral_district_counting_centre"]:
                    user_access_area_ids.extend(
                        global_area_map["electoral_district_counting_centre"][electoral_district_id]
                    )
        elif role is POLLING_DIVISION_REPORT_VIEWER_ROLE or role is POLLING_DIVISION_REPORT_GENERATOR_ROLE:
            global_area_map = init_global_area_map()
            for electoral_district_id in user_access_area_ids:
                if electoral_district_id in global_area_map["electoral_district_polling_division"]:
                    user_access_area_ids.extend(
                        global_area_map["electoral_district_polling_division"][electoral_district_id]
                    )

    if not claim_found:
        UnauthorizedException("No matching claim found.")
    else:
        connexion.context[USER_ACCESS_AREA_IDS] = set(user_access_area_ids)
        return func(*args, **kwargs)
