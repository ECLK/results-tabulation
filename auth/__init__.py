from typing import Dict, Set

from flask import request
import connexion
from decorator import decorator
from jose import jwt

from app import db
from auth.AuthConstants import EC_LEADERSHIP_ROLE, NATIONAL_REPORT_VERIFIER_ROLE, NATIONAL_REPORT_VIEWER_ROLE, \
    SUB, DATA_EDITOR_ROLE, POLLING_DIVISION_REPORT_VIEWER_ROLE, POLLING_DIVISION_REPORT_VERIFIER_ROLE, \
    ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE, ELECTORAL_DISTRICT_REPORT_VERIFIER_ROLE, ROLE_CLAIM_PREFIX, ADMIN_ROLE, \
    JWT_TOKEN_HEADER_KEY
from exception import UnauthorizedException
import json

JWT_SECRET = "jwt_secret"
AREA_ID = "areaId"
USER_ACCESS_AREA_IDS = "userAccessAreaIds"
USER_NAME = "userName"

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
        ROLE_CLAIM_PREFIX + POLLING_DIVISION_REPORT_VERIFIER_ROLE,
        ROLE_CLAIM_PREFIX + ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE,
        ROLE_CLAIM_PREFIX + ELECTORAL_DISTRICT_REPORT_VERIFIER_ROLE,
        ROLE_CLAIM_PREFIX + NATIONAL_REPORT_VIEWER_ROLE,
        ROLE_CLAIM_PREFIX + NATIONAL_REPORT_VERIFIER_ROLE,
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
    print("\n\n\n\n####### request.headers ### [START]")
    print(request.headers)
    print("####### request.headers ### [END]\n\n\n")

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

        if role is NATIONAL_REPORT_VIEWER_ROLE or role is NATIONAL_REPORT_VERIFIER_ROLE:
            areas = db.session.query(Area.Model.areaId).filter(Area.Model.areaType == AreaTypeEnum.Country).all()
            user_access_area_ids.extend([area.areaId for area in areas])
        elif role is EC_LEADERSHIP_ROLE:
            areas = db.session.query(Area.Model.areaId).filter(
                Area.Model.areaType == AreaTypeEnum.ElectionCommission).all()
            user_access_area_ids.extend([area.areaId for area in areas])

    if not claim_found:
        UnauthorizedException("No matching claim found.")
    else:
        connexion.context[USER_ACCESS_AREA_IDS] = set(user_access_area_ids)
        return func(*args, **kwargs)
