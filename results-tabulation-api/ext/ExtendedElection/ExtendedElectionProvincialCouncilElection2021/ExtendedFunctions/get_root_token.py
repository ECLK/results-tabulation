from jose import jwt
from constants.AUTH_CONSTANTS import DATA_EDITOR_ROLE, POLLING_DIVISION_REPORT_VIEWER_ROLE, \
    POLLING_DIVISION_REPORT_VERIFIER_ROLE, NATIONAL_REPORT_VIEWER_ROLE, NATIONAL_REPORT_VERIFIER_ROLE, ADMIN_ROLE, \
    ROLE_CLAIM, AREA_CLAIM_PREFIX, SUB, EC_LEADERSHIP_ROLE, ROLE_PREFIX, ADMINISTRATIVE_DISTRICT_REPORT_VIEWER_ROLE, \
    ADMINISTRATIVE_DISTRICT_REPORT_VERIFIER_ROLE, PROVINCIAL_REPORT_VERIFIER_ROLE, PROVINCIAL_REPORT_VIEWER_ROLE


def get_root_token(election):
    from orm.entities import Area
    from orm.enums import AreaTypeEnum

    provinces = Area.get_associated_areas_query(
        areas=[], areaType=AreaTypeEnum.Province, electionId=election.election.electionId
    ).all()
    administrative_districts = Area.get_associated_areas_query(
        areas=[], areaType=AreaTypeEnum.AdministrativeDistrict, electionId=election.election.electionId
    ).all()
    countries = Area.get_associated_areas_query(
        areas=[], areaType=AreaTypeEnum.Country, electionId=election.election.electionId
    ).all()

    jwt_payload = {
        ROLE_CLAIM: [
            ROLE_PREFIX + ADMIN_ROLE,
            ROLE_PREFIX + DATA_EDITOR_ROLE,
            ROLE_PREFIX + POLLING_DIVISION_REPORT_VIEWER_ROLE,
            ROLE_PREFIX + POLLING_DIVISION_REPORT_VERIFIER_ROLE,
            ROLE_PREFIX + ADMINISTRATIVE_DISTRICT_REPORT_VIEWER_ROLE,
            ROLE_PREFIX + ADMINISTRATIVE_DISTRICT_REPORT_VERIFIER_ROLE,
            ROLE_PREFIX + PROVINCIAL_REPORT_VIEWER_ROLE,
            ROLE_PREFIX + PROVINCIAL_REPORT_VERIFIER_ROLE,
            ROLE_PREFIX + NATIONAL_REPORT_VIEWER_ROLE,
            ROLE_PREFIX + NATIONAL_REPORT_VERIFIER_ROLE,
            ROLE_PREFIX + EC_LEADERSHIP_ROLE
        ],
        SUB: "janak@carbon.super", AREA_CLAIM_PREFIX + ADMIN_ROLE: str([]),
        AREA_CLAIM_PREFIX + DATA_EDITOR_ROLE: str([{
            "areaId": administrative_district.areaId,
            "areaName": administrative_district.areaName
        } for administrative_district in administrative_districts]),
        AREA_CLAIM_PREFIX + POLLING_DIVISION_REPORT_VIEWER_ROLE: str([{
            "areaId": administrative_district.areaId,
            "areaName": administrative_district.areaName
        } for administrative_district in administrative_districts]),
        AREA_CLAIM_PREFIX + POLLING_DIVISION_REPORT_VERIFIER_ROLE: str([{
            "areaId": administrative_district.areaId,
            "areaName": administrative_district.areaName
        } for administrative_district in administrative_districts]),
        AREA_CLAIM_PREFIX + ADMINISTRATIVE_DISTRICT_REPORT_VIEWER_ROLE: str([{
            "areaId": administrative_district.areaId,
            "areaName": administrative_district.areaName
        } for administrative_district in administrative_districts]),
        AREA_CLAIM_PREFIX + ADMINISTRATIVE_DISTRICT_REPORT_VERIFIER_ROLE: str([{
            "areaId": administrative_district.areaId,
            "areaName": administrative_district.areaName
        } for administrative_district in administrative_districts]),
        AREA_CLAIM_PREFIX + PROVINCIAL_REPORT_VIEWER_ROLE: str([{
            "areaId": province.areaId,
            "areaName": province.areaName
        } for province in provinces]),
        AREA_CLAIM_PREFIX + PROVINCIAL_REPORT_VERIFIER_ROLE: str([{
            "areaId": province.areaId,
            "areaName": province.areaName
        } for province in provinces]),
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
