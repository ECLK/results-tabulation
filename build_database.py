from app import db
from orm.entities import *

from orm.enums import ElectorateTypeEnum, OfficeTypeEnum

from sqlalchemy.sql import func

# db.engine.execute("create database election")


# Create the database
db.create_all()

ELECTORATES_DATA = {
    "administrativeDistricts": [
        {"id": 1, "parent": None, "name": "Colombo"},
        {"id": 2, "parent": None, "name": "Kalutara"},
        {"id": 3, "parent": None, "name": "Gampaha"}
    ],
    "pollingDivisions": [
        {"id": 4, "parent": 1, "name": "Colombo South"},
        {"id": 5, "parent": 1, "name": "Colombo North"},
        {"id": 6, "parent": 2, "name": "Kalutara South"},
        {"id": 7, "parent": 2, "name": "Kalutara North"},
        {"id": 8, "parent": 3, "name": "Gampaha South"},
        {"id": 9, "parent": 3, "name": "Gampaha North"}
    ],
    "pollingDistricts": [
        {"id": 10, "parent": 4, "name": "1"},
        {"id": 11, "parent": 4, "name": "2"},
        {"id": 12, "parent": 5, "name": "1"},
        {"id": 13, "parent": 5, "name": "2"},
        {"id": 14, "parent": 6, "name": "1"},
        {"id": 15, "parent": 6, "name": "2"},
        {"id": 16, "parent": 7, "name": "1"},
        {"id": 17, "parent": 7, "name": "2"},
        {"id": 18, "parent": 8, "name": "1"},
        {"id": 19, "parent": 8, "name": "2"},
        {"id": 20, "parent": 9, "name": "1"},
        {"id": 21, "parent": 9, "name": "2"}
    ]
}

OFFICE_DATA = {
    "districtCentres": [
        {"id": 1, "parent": None, "name": "Colombo", "tallySheetCodes": ["PRE_30_PD", "PRE_30_ED"]},
        {"id": 2, "parent": None, "name": "Kalutara", "tallySheetCodes": ["PRE_30_PD", "PRE_30_ED"]},
        {"id": 3, "parent": None, "name": "Gampaha", "tallySheetCodes": ["PRE_30_PD", "PRE_30_ED"]},
    ],
    "countingCentres": [
        {"id": 4, "parent": 1, "name": "Colombo South", "tallySheetCodes": ["PRE_41"]},
        {"id": 5, "parent": 1, "name": "Colombo West", "tallySheetCodes": ["PRE_41"]},
        {"id": 6, "parent": 2, "name": "Kalutara South", "tallySheetCodes": ["PRE_41"]},
        {"id": 7, "parent": 2, "name": "Kalutara West", "tallySheetCodes": ["PRE_41"]},
        {"id": 8, "parent": 3, "name": "Gampaha South", "tallySheetCodes": ["PRE_41"]},
        {"id": 9, "parent": 3, "name": "Gampaha West", "tallySheetCodes": ["PRE_41"]},
    ]
}

POLLING_STATION_DATA = [
    {"id": 1, "pollingDistrict": 10, "countingCentre": 4, "name": "St. Thomas College, Hall 1"},
    {"id": 2, "pollingDistrict": 11, "countingCentre": 4, "name": "St. Thomas College, Hall 2"},
    {"id": 3, "pollingDistrict": 12, "countingCentre": 5, "name": "Science College, Hall 1"},
    {"id": 4, "pollingDistrict": 13, "countingCentre": 5, "name": "Science College, Hall 2"},
    {"id": 5, "pollingDistrict": 14, "countingCentre": 6, "name": "Science College, Hall 3"},
    {"id": 6, "pollingDistrict": 15, "countingCentre": 6, "name": "Hill Street Community Centre, Hall 1"},
    {"id": 7, "pollingDistrict": 16, "countingCentre": 7, "name": "Hill Street Community Centre, Hall 2"},
    {"id": 8, "pollingDistrict": 17, "countingCentre": 7, "name": "Hill Street Community Centre, Hall 3"},
    {"id": 9, "pollingDistrict": 18, "countingCentre": 8, "name": "Hill Street Community Centre, Hall 4"},
    {"id": 10, "pollingDistrict": 19, "countingCentre": 8, "name": "Muslim Girls College, Hall 1"},
    {"id": 11, "pollingDistrict": 20, "countingCentre": 9, "name": "Muslim Girls College, Hall 2"},
    {"id": 12, "pollingDistrict": 21, "countingCentre": 9, "name": "Muslim Girls College, Hall 3"},
    {"id": 13, "pollingDistrict": 21, "countingCentre": 9, "name": "Muslim Girls College, Hall 4"}
]


def get_column_max(column):
    query_result = db.session.query(func.max(column).label("max")).one_or_none()

    return 0 if query_result.max is None else query_result.max


for i in range(1, 2):
    election = Election.create()

    electorateIdOffset = get_column_max(Electorate.Model.electorateId)

    for row in ELECTORATES_DATA["administrativeDistricts"]:
        Electorate.create(
            electorateName=row["name"],
            electorateType=ElectorateTypeEnum.AdministrativeDistrict,
            electionId=election.electionId,
            parentElectorateId=None
        )
    for row in ELECTORATES_DATA["pollingDivisions"]:
        Electorate.create(
            electorateName=row["name"],
            electorateType=ElectorateTypeEnum.PollingDivision,
            electionId=election.electionId,
            parentElectorateId=electorateIdOffset + row["parent"]
        )
    for row in ELECTORATES_DATA["pollingDistricts"]:
        Electorate.create(
            electorateName=row["name"],
            electorateType=ElectorateTypeEnum.PollingDistrict,
            electionId=election.electionId,
            parentElectorateId=electorateIdOffset + row["parent"]
        )

    officeIdOffset = get_column_max(Office.Model.officeId)
    for row in OFFICE_DATA["districtCentres"]:
        Office.create(
            officeName=row["name"],
            electionId=election.electionId,
            officeType=OfficeTypeEnum.DistrictCentre,
            parentOfficeId=None
        )
        for tallySheetCode in row["tallySheetCodes"]:
            TallySheet.create(
                code=tallySheetCode,
                electionId=election.electionId,
                officeId=officeIdOffset + row["id"]
            )
    for row in OFFICE_DATA["countingCentres"]:
        Office.create(
            officeName=row["name"],
            electionId=election.electionId,
            officeType=OfficeTypeEnum.CountingCentre,
            parentOfficeId=officeIdOffset + row["parent"]
        )
        for tallySheetCode in row["tallySheetCodes"]:
            TallySheet.create(
                code=tallySheetCode,
                electionId=election.electionId,
                officeId=officeIdOffset + row["id"]
            )

    for row in POLLING_STATION_DATA:
        PollingStation.create(
            officeName=row["name"],
            electionId=election.electionId,
            electorateId=electorateIdOffset + row["pollingDistrict"],
            parentOfficeId=officeIdOffset + row["countingCentre"],
        )

    for i in range(1, 6):
        Party.create(partyName="Party-%d" % i)

    for i in range(1, 10):
        Ballot.create(
            electionId=election.electionId,
            ballotId="pre-ballot-%d-%d" % (election.electionId, i)
        )

    for i in range(1, 50):
        BallotBox.create(
            electionId=election.electionId,
            ballotBoxId="pre-ballot-box-%d-%d" % (election.electionId, i)
        )
