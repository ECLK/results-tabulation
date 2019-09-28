from typing import Dict, List

import connexion
from decorator import decorator
from jose import jwt

from orm.entities import Area
from orm.entities.Area import AreaModel
from orm.entities.Submission import TallySheet
from orm.entities.Submission.TallySheet import TallySheetModel
from orm.enums import AreaTypeEnum

JWT_SECRET = "jwt_secret"
CLAIM_PREFIX = "areaAssignment/"


def get_unauthorized_msg(detail):
    return connexion.problem(401, "Unauthorized", detail)


def decode_token(token):
    return jwt.decode(token, key=JWT_SECRET)


def get_role_claims() -> Dict[str, Dict]:
    claims: dict = connexion.context['token_info']
    role_claims = {}
    role_claim_keys = [x for x in claims.keys() if x.startswith(CLAIM_PREFIX)]
    for role_claim_key in role_claim_keys:
        role_claims[role_claim_key] = claims.get(role_claim_key)
    return role_claims


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

        claim_found = True

        claim_values = claims.get(claim)

        if not claim_values:
            return func(*args, **kwargs)

        if connexion.request.path.split("/")[1] == "tally-sheet":
            tally_sheet_id = connexion.request.view_args.get("tallySheetId")
            tally_sheet: TallySheetModel = TallySheet.get_by_id(tally_sheet_id)
            election_id = tally_sheet.electionId
            tally_sheet_area_id = tally_sheet.officeId
            areas = []
            tally_sheet_area: AreaModel = Area.get_by_id(tally_sheet_area_id)

            areas.append(tally_sheet_area)

            if tally_sheet_area.areaType == AreaTypeEnum.CountingCentre:
                areas.append(Area.get_all(election_id=election_id, associated_area_id=tally_sheet_area_id,
                                          area_type=AreaTypeEnum.PollingDivision)[0])
                areas.append(Area.get_all(election_id=election_id, associated_area_id=tally_sheet_area_id,
                                          area_type=AreaTypeEnum.ElectoralDistrict)[0])
            elif tally_sheet_area.areaType == AreaTypeEnum.PollingDivision:
                areas.append(Area.get_all(election_id=election_id, associated_area_id=tally_sheet_area_id,
                                          area_type=AreaTypeEnum.ElectoralDistrict)[0])

            claim_value_to_match = {}

            for area in areas:
                area_name = area.areaName
                area_type = area.areaType

                if area_type == AreaTypeEnum.CountingCentre:
                    claim_value_to_match["countingCenter"] = area_name
                elif area_type == AreaTypeEnum.PollingDivision:
                    claim_value_to_match["pollingDivision"] = area_name
                elif area_type == AreaTypeEnum.ElectoralDistrict:
                    claim_value_to_match["electoralDistrict"] = area_name

            matching_claim_value = [x for x in claim_values if x == claim_value_to_match]

            if len(matching_claim_value) > 0:
                return func(*args, **kwargs)

    if not claim_found:
        return get_unauthorized_msg("No matching claim found.")
    else:
        return get_unauthorized_msg("Failed to authorize based on area information.")
