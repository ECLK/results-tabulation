from typing import Dict, Set

import connexion
from decorator import decorator
from jose import jwt

from auth.AuthConstants import EC_LEADERSHIP_ROLE, NATIONAL_REPORT_GENERATOR_ROLE, NATIONAL_REPORT_VIEWER_ROLE
from exception import UnauthorizedException

JWT_SECRET = "jwt_secret"
CLAIM_PREFIX = "areaAssignment/"
AREA_ID = "areaId"
USER_ACCESS_AREA_IDS = "userAccessAreaIds"


def decode_token(token):
    return jwt.decode(token, key=JWT_SECRET)


def get_role_claims() -> Dict[str, Dict]:
    """
    Gets all user role related claims from all the claims in token_info.

    Decoded JWT information are set to connexion.context['token_info'] by the security decorators in connexion.

    :return: dict of claim id to claim value.
    """
    claims: dict = connexion.context['token_info']
    role_claims = {}
    role_claim_keys = [x for x in claims.keys() if x.startswith(CLAIM_PREFIX)]
    for role_claim_key in role_claim_keys:
        role_claims[role_claim_key] = claims.get(role_claim_key)
    return role_claims


def get_user_access_area_ids() -> Set[int]:
    """
    Gets user access area ids from connexion context.

    :return: set of user access area ids
    """
    return connexion.context[USER_ACCESS_AREA_IDS]


@decorator
def authorize(func, required_roles=None, *args, **kwargs):
    if required_roles is None:
        return func(*args, **kwargs)

    if 'token_info' not in connexion.context.keys():
        UnauthorizedException("No claims found.")

    claims: Dict = get_role_claims()

    claim_found = False
    user_access_area_ids = []

    for role in required_roles:
        claim = CLAIM_PREFIX + role

        if claim not in claims.keys():
            continue

        claim_found = True
        user_access_area_ids.extend([x.get(AREA_ID) for x in claims.get(claim)])

    if not claim_found:
        UnauthorizedException("No matching claim found.")
    else:
        connexion.context[USER_ACCESS_AREA_IDS] = set(user_access_area_ids)
        return func(*args, **kwargs)
