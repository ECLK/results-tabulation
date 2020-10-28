from auth import AREA_CLAIM_PREFIX, ADMIN_ROLE, DATA_EDITOR_ROLE, POLLING_DIVISION_REPORT_VIEWER_ROLE, \
    POLLING_DIVISION_REPORT_VERIFIER_ROLE, ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE, \
    ELECTORAL_DISTRICT_REPORT_VERIFIER_ROLE, NATIONAL_REPORT_VIEWER_ROLE, NATIONAL_REPORT_VERIFIER_ROLE, \
    EC_LEADERSHIP_ROLE, SUB, ROLE_CLAIM, ROLE_PREFIX
from ext.ExtendedElection import get_extended_election
from orm.entities import Area, Election
from orm.enums import AreaTypeEnum
from jose import jwt


def get_root_token(election):
    electionId = election.electionId

    electoral_districts = Area.get_associated_areas_query(
        areas=[], areaType=AreaTypeEnum.ElectoralDistrict, electionId=electionId
    ).all()

    countries = Area.get_associated_areas_query(
        areas=[], areaType=AreaTypeEnum.Country, electionId=electionId
    ).all()

    jwt_payload = {
        ROLE_CLAIM: [
            ROLE_PREFIX + ADMIN_ROLE,
            ROLE_PREFIX + DATA_EDITOR_ROLE,
            ROLE_PREFIX + POLLING_DIVISION_REPORT_VIEWER_ROLE,
            ROLE_PREFIX + POLLING_DIVISION_REPORT_VERIFIER_ROLE,
            ROLE_PREFIX + ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE,
            ROLE_PREFIX + ELECTORAL_DISTRICT_REPORT_VERIFIER_ROLE,
            ROLE_PREFIX + NATIONAL_REPORT_VIEWER_ROLE,
            ROLE_PREFIX + NATIONAL_REPORT_VERIFIER_ROLE,
            ROLE_PREFIX + EC_LEADERSHIP_ROLE
        ],
        SUB: "janak@carbon.super", AREA_CLAIM_PREFIX + ADMIN_ROLE: str([]),
        AREA_CLAIM_PREFIX + DATA_EDITOR_ROLE: str([{
            "areaId": electoral_district.areaId,
            "areaName": electoral_district.areaName
        } for electoral_district in electoral_districts]),
        AREA_CLAIM_PREFIX + POLLING_DIVISION_REPORT_VIEWER_ROLE: str([{
            "areaId": electoral_district.areaId,
            "areaName": electoral_district.areaName
        } for electoral_district in electoral_districts]),
        AREA_CLAIM_PREFIX + POLLING_DIVISION_REPORT_VERIFIER_ROLE: str([{
            "areaId": electoral_district.areaId,
            "areaName": electoral_district.areaName
        } for electoral_district in electoral_districts]),
        AREA_CLAIM_PREFIX + ELECTORAL_DISTRICT_REPORT_VIEWER_ROLE: str([{
            "areaId": electoral_district.areaId,
            "areaName": electoral_district.areaName
        } for electoral_district in electoral_districts]),
        AREA_CLAIM_PREFIX + ELECTORAL_DISTRICT_REPORT_VERIFIER_ROLE: str([{
            "areaId": electoral_district.areaId,
            "areaName": electoral_district.areaName
        } for electoral_district in electoral_districts]),
        AREA_CLAIM_PREFIX + NATIONAL_REPORT_VIEWER_ROLE: str([{
            "areaId": country.areaId,
            "areaName": country.areaName
        } for country in countries]),
        AREA_CLAIM_PREFIX + NATIONAL_REPORT_VERIFIER_ROLE: str([{
            "areaId": country.areaId,
            "areaName": country.areaName
        } for country in countries]),
        AREA_CLAIM_PREFIX + EC_LEADERSHIP_ROLE: str([{
            "areaId": country.areaId,
            "areaName": country.areaName
        } for country in countries])
    }

    # Generate a token with claims for everything.
    key = "jwt_secret"
    encoded_jwt_token = jwt.encode(jwt_payload, key)

    return encoded_jwt_token
