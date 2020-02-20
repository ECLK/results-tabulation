from typing import Dict, Set

import connexion
from decorator import decorator
from flask import request
from jose import jwt

from app import cache, db
from constants import VOTE_TYPES
from constants.AUTH_CONSTANTS import EC_LEADERSHIP_ROLE, NATIONAL_REPORT_VERIFIER_ROLE, NATIONAL_REPORT_VIEWER_ROLE, \
    SUB, DATA_EDITOR_ROLE, POLLING_DIVISION_REPORT_VIEWER_ROLE, POLLING_DIVISION_REPORT_VERIFIER_ROLE, \
    ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE, ELECTORAL_DISTRICT_REPORT_VERIFIER_ROLE, AREA_CLAIM_PREFIX, ADMIN_ROLE, \
    JWT_TOKEN_HEADER_KEY, ROLE_CLAIM, ROLE_PREFIX

from exception import UnauthorizedException

import json

from exception.messages import MESSAGE_CODE_USER_NOT_FOUND, MESSAGE_CODE_USER_NOT_AUTHENTICATED, \
    MESSAGE_CODE_USER_NOT_AUTHORIZED

JWT_SECRET = "jwt_secret"
AREA_ID = "areaId"
USER_ACCESS_AREA_IDS = "userAccessAreaIds"
USER_NAME = "userName"
USER_ROLES = "userRoles"

Countries = "Countries"
CountingCentres = "CountingCentres"
ElectoralDistricts = "ElectoralDistricts"
PollingDivisions = "CountingCentres"
Postal = "Postal"
NonPostal = "NonPostal"


#
# @cache.cached(key_prefix='global_area_map')
# def init_global_area_map():
#     # TODO Refactor
#
#     from orm.entities import Area
#     from orm.enums import AreaTypeEnum
#
#     global_area_map = {
#         ElectoralDistricts: {
#             PollingDivisions: {
#                 # list of polling divisions mapped to the electoral district id.
#             },
#             CountingCentres: {
#                 Postal: {
#                     # list of postal counting centres mapped to the electoral district id.
#                 },
#                 NonPostal: {
#                     # list of non postal counting centres mapped to the electoral district id.
#                 }
#             }
#         },
#         Countries: {
#             ElectoralDistricts: {
#                 # list of electoral districts mapped to the country id.
#             },
#             PollingDivisions: {
#                 # list of polling divisions mapped to the country id.
#             },
#             CountingCentres: {
#                 Postal: {
#                     # list of postal counting centres mapped to the country id.
#                 },
#                 NonPostal: {
#                     # list of non postal counting centres mapped to the country id.
#                 }
#             }
#         }
#     }
#
#     countries = Area.get_all(area_type=AreaTypeEnum.Country)
#     electoral_districts = Area.get_all(area_type=AreaTypeEnum.ElectoralDistrict)
#
#     for electoral_district in electoral_districts:
#
#         sub_elections = electoral_district.election.subElections
#         for sub_election in sub_elections:
#             if sub_election.voteType == Postal:
#                 global_area_map[ElectoralDistricts][CountingCentres][Postal][electoral_district.areaId] = [
#                     counting_centre.areaId for counting_centre in
#                     electoral_district.get_associated_areas(
#                         areaType=AreaTypeEnum.CountingCentre,
#                         electionId=sub_election.electionId
#                     )
#                 ]
#             elif sub_election.voteType == NonPostal:
#                 global_area_map[ElectoralDistricts][CountingCentres][NonPostal][electoral_district.areaId] = [
#                     counting_centre.areaId for counting_centre in
#                     electoral_district.get_associated_areas(
#                         areaType=AreaTypeEnum.CountingCentre,
#                         electionId=sub_election.electionId
#                     )
#                 ]
#
#         global_area_map[ElectoralDistricts][PollingDivisions][electoral_district.areaId] = [
#             counting_centre.areaId for counting_centre in
#             electoral_district.get_associated_areas(areaType=AreaTypeEnum.PollingDivision)
#         ]
#
#     for country in countries:
#
#         sub_elections = country.election.subElections
#         for sub_election in sub_elections:
#             if sub_election.voteType == Postal:
#                 global_area_map[Countries][CountingCentres][Postal][country.areaId] = [
#                     counting_centre.areaId for counting_centre in
#                     country.get_associated_areas(
#                         areaType=AreaTypeEnum.CountingCentre,
#                         electionId=sub_election.electionId
#                     )
#                 ]
#             elif sub_election.voteType == NonPostal:
#                 global_area_map[Countries][CountingCentres][NonPostal][country.areaId] = [
#                     counting_centre.areaId for counting_centre in
#                     country.get_associated_areas(
#                         areaType=AreaTypeEnum.CountingCentre,
#                         electionId=sub_election.electionId
#                     )
#                 ]
#
#         global_area_map[Countries][ElectoralDistricts][country.areaId] = [
#             counting_centre.areaId for counting_centre in
#             country.get_associated_areas(areaType=AreaTypeEnum.ElectoralDistrict)
#         ]
#
#         global_area_map[Countries][PollingDivisions][country.areaId] = [
#             counting_centre.areaId for counting_centre in
#             country.get_associated_areas(areaType=AreaTypeEnum.PollingDivision)
#         ]
#
#     return global_area_map


def decode_token(token):
    try:
        token = jwt.decode(
            token, key=JWT_SECRET,
            options={"verify_signature": False, "verify_exp": False}
        )

        return token
    except Exception as e:
        raise UnauthorizedException(
            message="Invalid authorization token.",
            code=MESSAGE_CODE_USER_NOT_AUTHENTICATED
        )


def get_jwt_token():
    if JWT_TOKEN_HEADER_KEY not in request.headers:
        raise UnauthorizedException(
            message="No authorization header found.",
            code=MESSAGE_CODE_USER_NOT_AUTHENTICATED
        )

    print("######### request.headers.get(JWT_TOKEN_HEADER_KEY) ###### ", request.headers.get(JWT_TOKEN_HEADER_KEY))

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
        AREA_CLAIM_PREFIX + ADMIN_ROLE,
        AREA_CLAIM_PREFIX + DATA_EDITOR_ROLE,
        AREA_CLAIM_PREFIX + POLLING_DIVISION_REPORT_VIEWER_ROLE,
        AREA_CLAIM_PREFIX + POLLING_DIVISION_REPORT_VERIFIER_ROLE,
        AREA_CLAIM_PREFIX + ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE,
        AREA_CLAIM_PREFIX + ELECTORAL_DISTRICT_REPORT_VERIFIER_ROLE,
        AREA_CLAIM_PREFIX + NATIONAL_REPORT_VIEWER_ROLE,
        AREA_CLAIM_PREFIX + NATIONAL_REPORT_VERIFIER_ROLE,
        AREA_CLAIM_PREFIX + EC_LEADERSHIP_ROLE
    ]
    for area_assignment_claim_key in area_assignment_claim_keys:
        if area_assignment_claim_key in claims.keys():
            area_assignment_claim_value = claims.get(area_assignment_claim_key)
            area_assignment_claim_value = area_assignment_claim_value.replace("\'", "\"")
            filtered_claims[area_assignment_claim_key] = json.loads(area_assignment_claim_value)

    if SUB in claims.keys():
        filtered_claims[SUB] = claims.get(SUB)

    if ROLE_CLAIM in claims.keys():
        filtered_claims[ROLE_CLAIM] = claims.get(ROLE_CLAIM)

    return filtered_claims


def get_ip() -> str:
    return request.remote_addr


def get_user_name() -> str:
    """
    Gets user namefrom connexion context.

    :return: string user name
    """
    return connexion.context[USER_NAME]


def get_user_roles():
    return connexion.context[USER_ROLES]


def get_user_access_area_ids() -> Set[int]:
    """
    Gets user access area ids from connexion context.

    :return: set of user access area ids
    """
    return connexion.context[USER_ACCESS_AREA_IDS]


def has_role_based_access(tally_sheet, access_type):
    from ext.ExtendedElection import get_extended_election

    election = tally_sheet.submission.election
    extended_election = get_extended_election(election=election)
    role_based_access_config = extended_election.role_based_access_config

    tally_sheet_code = tally_sheet.template.templateName
    vote_type = election.voteType

    for role in connexion.context[USER_ROLES]:
        if role in role_based_access_config:
            if tally_sheet_code in role_based_access_config[role]:
                if vote_type in role_based_access_config[role][tally_sheet_code]:
                    if access_type in role_based_access_config[role][tally_sheet_code][vote_type]:
                        return True

    return False


def has_role(role):
    user_roles = get_user_roles()
    if role in user_roles:
        return True
    else:
        return False


@decorator
def authenticate(func, *args, **kwargs):
    print("\n\n\n\n####### request.headers ### [START]")
    print(request.headers)
    print("####### request.headers ### [END]\n\n\n")

    claims: Dict = get_claims()

    if SUB not in claims:
        UnauthorizedException(
            message="No valid user found.",
            code=MESSAGE_CODE_USER_NOT_FOUND
        )

    if ROLE_CLAIM not in claims or claims.get(ROLE_CLAIM) == []:
        UnauthorizedException(
            message="No valid user role found.",
            code=MESSAGE_CODE_USER_NOT_AUTHORIZED
        )

    user_name = claims.get(SUB)

    connexion.context[USER_NAME] = user_name
    connexion.context[USER_ROLES] = [role.replace(ROLE_PREFIX, "") for role in claims.get(ROLE_CLAIM) if
                                     role.startswith(ROLE_PREFIX)]

    return func(*args, **kwargs)


def _get_role_area_ids(parentAreaIds, areaType, voteTypes=[]):
    from orm.entities import Area, Election

    parentAreas = db.session.query(Area.Model).filter(Area.Model.areaId.in_(parentAreaIds)).all()
    associated_areas_subquery = Area.get_associated_areas_query(
        areas=parentAreas,
        areaType=areaType
    ).subquery()

    query = db.session.query(
        associated_areas_subquery.c.areaId
    ).filter(
        Election.Model.electionId == associated_areas_subquery.c.electionId
    )

    if len(voteTypes) > 0:
        query = query.filter(Election.Model.voteType.in_(voteTypes))

    return query.all()


@decorator
@authenticate
def authorize(func, required_roles=None, *args, **kwargs):
    from orm.enums import AreaTypeEnum

    if required_roles is None:
        return func(*args, **kwargs)

    claims: Dict = get_claims()

    claim_found = False
    user_access_area_ids = []

    for role in required_roles:
        claim = AREA_CLAIM_PREFIX + role

        if claim not in claims.keys():
            continue

        if not has_role(role):
            continue

        claim_found = True

        claim_area_ids = [x.get(AREA_ID) for x in claims.get(claim)]

        if role is DATA_EDITOR_ROLE:
            # To list, view, submit and lock data entry tally sheets.
            user_access_area_ids.extend([
                area.areaId for area in _get_role_area_ids(
                    parentAreaIds=claim_area_ids,
                    areaType=AreaTypeEnum.CountingCentre,
                    voteTypes=[VOTE_TYPES.Postal, VOTE_TYPES.NonPostal]
                )
            ])

        elif role is POLLING_DIVISION_REPORT_VIEWER_ROLE:
            # To list and view polling division wise reports.
            user_access_area_ids.extend([
                area.areaId for area in _get_role_area_ids(
                    parentAreaIds=claim_area_ids,
                    areaType=AreaTypeEnum.PollingDivision
                )
            ])

        elif role is POLLING_DIVISION_REPORT_VERIFIER_ROLE:
            # To list, view and lock polling division wise reports.
            user_access_area_ids.extend([
                area.areaId for area in _get_role_area_ids(
                    parentAreaIds=claim_area_ids,
                    areaType=AreaTypeEnum.PollingDivision
                )
            ])

            # To list, view and unlock counting wise reports.
            user_access_area_ids.extend([
                area.areaId for area in _get_role_area_ids(
                    parentAreaIds=claim_area_ids,
                    areaType=AreaTypeEnum.CountingCentre,
                    voteTypes=[VOTE_TYPES.NonPostal]
                )
            ])

        elif role is ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE:
            # To list, view and lock PRE-30-ED and PRE-30-PV.
            user_access_area_ids.extend(claim_area_ids)

        elif role is ELECTORAL_DISTRICT_REPORT_VERIFIER_ROLE:
            # To list, view and lock PRE-30-ED and PRE-30-PV.
            user_access_area_ids.extend(claim_area_ids)

            # To list, view and unlock polling division reports.
            user_access_area_ids.extend([
                area.areaId for area in _get_role_area_ids(
                    parentAreaIds=claim_area_ids,
                    areaType=AreaTypeEnum.PollingDivision
                )
            ])

            # To list, view and unlock postal vote counting wise reports.
            user_access_area_ids.extend([
                area.areaId for area in _get_role_area_ids(
                    parentAreaIds=claim_area_ids,
                    areaType=AreaTypeEnum.CountingCentre,
                    voteTypes=[VOTE_TYPES.Postal]
                )
            ])

        elif role is NATIONAL_REPORT_VIEWER_ROLE:
            # To list, view and lock All Island Reports.
            user_access_area_ids.extend(claim_area_ids)

        elif role is NATIONAL_REPORT_VERIFIER_ROLE:
            # To list, view and lock All Island Reports.
            user_access_area_ids.extend(claim_area_ids)

            # To list, view and unlock PR-30-PV and PRE-30-ED.
            user_access_area_ids.extend([
                area.areaId for area in _get_role_area_ids(
                    parentAreaIds=claim_area_ids,
                    areaType=AreaTypeEnum.ElectoralDistrict
                )
            ])

        elif role is EC_LEADERSHIP_ROLE:

            for country_id in claim_area_ids:
                # To list, view and unlock All Island Reports
                user_access_area_ids.extend(claim_area_ids)

                user_access_area_ids.extend([
                    area.areaId for area in _get_role_area_ids(
                        parentAreaIds=claim_area_ids,
                        areaType=AreaTypeEnum.ElectoralDistrict
                    )
                ])

                user_access_area_ids.extend([
                    area.areaId for area in _get_role_area_ids(
                        parentAreaIds=claim_area_ids,
                        areaType=AreaTypeEnum.PollingDivision
                    )
                ])

                user_access_area_ids.extend([
                    area.areaId for area in _get_role_area_ids(
                        parentAreaIds=claim_area_ids,
                        areaType=AreaTypeEnum.CountingCentre
                    )
                ])

    if not claim_found:
        UnauthorizedException(
            message="No matching claim found.",
            code=MESSAGE_CODE_USER_NOT_AUTHORIZED
        )
    else:
        connexion.context[USER_ACCESS_AREA_IDS] = set(user_access_area_ids)
        return func(*args, **kwargs)
