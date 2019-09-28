from typing import Dict, Set

import connexion
from decorator import decorator
from jose import jwt

from auth.AuthConstants import EC_LEADERSHIP_ROLE, NATIONAL_REPORT_GENERATOR_ROLE, NATIONAL_REPORT_VIEWER_ROLE
from orm.entities.Submission import TallySheet
from orm.entities.Submission.TallySheet import TallySheetModel

JWT_SECRET = "jwt_secret"
CLAIM_PREFIX = "areaAssignment/"
AREA_ID = "areaID"


def get_unauthorized_msg(detail):
    return connexion.problem(401, "Unauthorized", detail)


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


def get_user_access_area_ids(claim_id: str = None) -> Set[int]:
    """
    Gets all area ids the user has access to.

    :param claim_id: optional, if provided, area ids are limited to the ones in this claim only.
    :return:
    """
    claims: Dict = get_role_claims()
    if claim_id:
        return set([x.get(AREA_ID) for x in claims.get(claim_id)])

    user_area_ids = []
    for claim_value in claims.values():
        user_area_ids.extend([x.get(AREA_ID) for x in claim_value])
    return set(user_area_ids)


@decorator
def authorize(func, required_roles=None, *args, **kwargs):
    if required_roles is None:
        return func(*args, **kwargs)

    if 'token_info' not in connexion.context.keys():
        return get_unauthorized_msg("No claims found.")

    claims: Dict = get_role_claims()

    claim_found = False

    for role in required_roles:
        claim = CLAIM_PREFIX + role

        if claim not in claims.keys():
            continue

        if role in [EC_LEADERSHIP_ROLE, NATIONAL_REPORT_GENERATOR_ROLE, NATIONAL_REPORT_VIEWER_ROLE]:
            return func(*args, **kwargs)

        claim_found = True

        claim_values = claims.get(claim)

        if not claim_values:
            return func(*args, **kwargs)

        if connexion.request.path.split("/")[1] == "tally-sheet":
            tally_sheet_id = connexion.request.view_args.get("tallySheetId")

            # tally sheet get all
            if not tally_sheet_id:
                return func(*args, **kwargs)

            tally_sheet: TallySheetModel = TallySheet.get_by_id(tally_sheet_id)
            tally_sheet_area_id = tally_sheet.officeId

            for claim_value in claim_values:
                if tally_sheet_area_id == claim_value.get(AREA_ID):
                    return func(*args, **kwargs)

    if not claim_found:
        return get_unauthorized_msg("No matching claim found.")
    else:
        return get_unauthorized_msg("Failed to authorize based on user access area information.")
