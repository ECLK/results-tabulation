from typing import Dict, Set

from flask import request
import connexion
from decorator import decorator
from jose import jwt

from auth.AuthConstants import EC_LEADERSHIP_ROLE, NATIONAL_REPORT_GENERATOR_ROLE, NATIONAL_REPORT_VIEWER_ROLE, \
    SUB, DATA_EDITOR_ROLE, POLLING_DIVISION_REPORT_VIEWER_ROLE, POLLING_DIVISION_REPORT_GENERATOR_ROLE, \
    ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE, ELECTORAL_DISTRICT_REPORT_GENERATOR_ROLE, ROLE_CLAIM_PREFIX
from exception import UnauthorizedException

JWT_SECRET = "jwt_secret"
AREA_ID = "areaId"
USER_ACCESS_AREA_IDS = "userAccessAreaIds"
USER_NAME = "userName"


def decode_token(token):
    return jwt.decode(token, key=JWT_SECRET)


def get_claims() -> Dict[str, Dict]:
    """
    Gets all user role related claims from all the claims in token_info.

    Decoded JWT information are set to connexion.context['token_info'] by the security decorators in connexion.

    :return: dict of claim id to claim value.
    """

    if 'token_info' not in connexion.context.keys():
        UnauthorizedException("No claims found.")

    claims: dict = connexion.context['token_info']
    filtered_claims = {}
    filtered_claim_keys = [
        ROLE_CLAIM_PREFIX + DATA_EDITOR_ROLE,
        ROLE_CLAIM_PREFIX + POLLING_DIVISION_REPORT_VIEWER_ROLE,
        ROLE_CLAIM_PREFIX + POLLING_DIVISION_REPORT_GENERATOR_ROLE,
        ROLE_CLAIM_PREFIX + ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE,
        ROLE_CLAIM_PREFIX + ELECTORAL_DISTRICT_REPORT_GENERATOR_ROLE,
        ROLE_CLAIM_PREFIX + NATIONAL_REPORT_VIEWER_ROLE,
        ROLE_CLAIM_PREFIX + NATIONAL_REPORT_GENERATOR_ROLE,
        ROLE_CLAIM_PREFIX + EC_LEADERSHIP_ROLE,
        SUB
    ]
    for role_claim_key in filtered_claim_keys:
        if role_claim_key in claims.keys():
            filtered_claims[role_claim_key] = claims.get(role_claim_key)

    return filtered_claims


def get_ip() -> str:
    return request.remote_addr


def get_user_name() -> Set[int]:
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

    if not claim_found:
        UnauthorizedException("No matching claim found.")
    else:
        connexion.context[USER_ACCESS_AREA_IDS] = set(user_access_area_ids)
        return func(*args, **kwargs)
