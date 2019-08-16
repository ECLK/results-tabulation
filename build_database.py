from app import db
from orm.entities import *
from orm.entities.Submission.Report import Report_PRE_41, Report_PRE_30_PD, Report_PRE_30_ED

from orm.enums import ReportCodeEnum, AreaTypeEnum, TallySheetCodeEnum
from api.TallySheetVersionApi import TallySheetVersionPRE41Api

from sqlalchemy.sql import func

# db.engine.execute("create database election")


# Create the database
db.create_all()

ELECTORATES_DATA = {
    "electoralDistricts": [
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
        {"id": 22, "parent": None, "name": "Colombo", "tallySheetCodes": ["PRE_30_PD", "PRE_30_ED"]},
        {"id": 23, "parent": None, "name": "Kalutara", "tallySheetCodes": ["PRE_30_PD", "PRE_30_ED"]},
        {"id": 24, "parent": None, "name": "Gampaha", "tallySheetCodes": ["PRE_30_PD", "PRE_30_ED"]},
    ],
    "countingCentres": [
        {
            "id": 25, "parent": 22, "name": "Colombo South", "tallySheetCodes": ["PRE_41"],
            "submissions": [
                {"id": 22, "type": "tallySheet", "code": "PRE_41"},
                {"id": 23, "type": "report", "code": "PRE_41", "parent": 22}
            ]
        },
        {"id": 26, "parent": 22, "name": "Colombo West", "tallySheetCodes": ["PRE_41"]},
        {"id": 27, "parent": 23, "name": "Kalutara South", "tallySheetCodes": ["PRE_41"]},
        {"id": 28, "parent": 23, "name": "Kalutara West", "tallySheetCodes": ["PRE_41"]},
        {"id": 29, "parent": 24, "name": "Gampaha South", "tallySheetCodes": ["PRE_41"]},
        {"id": 30, "parent": 24, "name": "Gampaha West", "tallySheetCodes": ["PRE_41"]},
    ]
}

POLLING_STATION_DATA = [
    {"id": 10, "pollingDistrict": 10, "countingCentre": 25, "name": "St. Thomas College, Hall 1"},
    {"id": 11, "pollingDistrict": 11, "countingCentre": 25, "name": "St. Thomas College, Hall 2"},
    {"id": 12, "pollingDistrict": 12, "countingCentre": 26, "name": "Science College, Hall 1"},
    {"id": 13, "pollingDistrict": 13, "countingCentre": 26, "name": "Science College, Hall 2"},
    {"id": 14, "pollingDistrict": 14, "countingCentre": 27, "name": "Science College, Hall 3"},
    {"id": 15, "pollingDistrict": 15, "countingCentre": 27, "name": "Hill Street Community Centre, Hall 1"},
    {"id": 16, "pollingDistrict": 16, "countingCentre": 28, "name": "Hill Street Community Centre, Hall 2"},
    {"id": 8, "pollingDistrict": 17, "countingCentre": 28, "name": "Hill Street Community Centre, Hall 3"},
    {"id": 9, "pollingDistrict": 18, "countingCentre": 29, "name": "Hill Street Community Centre, Hall 4"},
    {"id": 10, "pollingDistrict": 19, "countingCentre": 29, "name": "Muslim Girls College, Hall 1"},
    {"id": 11, "pollingDistrict": 20, "countingCentre": 30, "name": "Muslim Girls College, Hall 2"},
    {"id": 12, "pollingDistrict": 21, "countingCentre": 30, "name": "Muslim Girls College, Hall 3"},
    {"id": 13, "pollingDistrict": 21, "countingCentre": 30, "name": "Muslim Girls College, Hall 4"}
]


def get_column_max(column):
    query_result = db.session.query(func.max(column).label("max")).one_or_none()

    return 0 if query_result.max is None else query_result.max


for i in range(1, 6):
    Party.create(partyName="Party-%d" % i, partySymbol="Cat")

for i in range(1, 50):
    Candidate.create(candidateName="Candidate-%d" % i)

for i in range(1, 2):
    election = Election.create(electionName="Test Election")

    for i in range(1, 6):
        electionParty = election.add_party(i)
        for j in range(1, 6):
            electionParty.add_candidate((i * 5) + j)

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

    electorateIdOffset = get_column_max(Electorate.Model.electorateId)

    for row in ELECTORATES_DATA["electoralDistricts"]:
        ElectoralDistrict.create(
            electorateName=row["name"],
            electionId=election.electionId
        )

        report = Report_PRE_30_ED.create(
            electionId=election.electionId,
            areaId=electorateIdOffset + row["id"]
        )

    for row in ELECTORATES_DATA["pollingDivisions"]:
        pollingDivision = PollingDivision.create(
            electorateName=row["name"],
            electionId=election.electionId
        )
        pollingDivision.add_parent(parentId=electorateIdOffset + row["parent"])

        report = Report_PRE_30_PD.create(
            electionId=election.electionId,
            areaId=electorateIdOffset + row["id"]
        )

    for row in ELECTORATES_DATA["pollingDistricts"]:
        PollingDistrict.create(
            electorateName=row["name"],
            electionId=election.electionId,
        ).add_parent(parentId=electorateIdOffset + row["parent"])

    officeIdOffset = get_column_max(Office.Model.officeId)
    for row in OFFICE_DATA["districtCentres"]:
        DistrictCentre.create(
            officeName=row["name"],
            electionId=election.electionId
        )

    for row in OFFICE_DATA["countingCentres"]:
        CountingCentre.create(
            officeName=row["name"],
            electionId=election.electionId
        ).add_parent(officeIdOffset + row["parent"])

        tallySheet = TallySheet.create(
            tallySheetCode=TallySheetCodeEnum.PRE_41,
            electionId=election.electionId,
            officeId=officeIdOffset + row["id"]
        )
        report = Report_PRE_41.create(
            electionId=election.electionId,
            areaId=officeIdOffset + row["id"],
            tallySheetId=tallySheet.tallySheetId,
        )
        tallySheetVersion = TallySheetVersionPRE41Api.create(
            tallySheetId=tallySheet.tallySheetId,
            body={
                "tallySheetId": tallySheet.tallySheetId,
                "tallySheetContent": [
                    {"partyId": 1, "count": 23, "countInWords": "Twenty three"},
                    {"partyId": 2, "count": 45, "countInWords": "Forty five"},
                    {"partyId": 3, "count": 60, "countInWords": "Sixty"}
                ]
            }
        )
        tallySheetVersion = TallySheetVersionPRE41Api.create(
            tallySheetId=tallySheet.tallySheetId,
            body={
                "tallySheetId": tallySheet.tallySheetId,
                "tallySheetContent": [
                    {"partyId": 1, "count": 23, "countInWords": "Twenty three"},
                    {"partyId": 2, "count": 45, "countInWords": "Forty five"},
                    {"partyId": 3, "count": 60, "countInWords": "Sixty"}
                ]
            }
        )

    for row in POLLING_STATION_DATA:
        pollingStation = PollingStation.create(
            officeName=row["name"],
            electionId=election.electionId
        )
        pollingStation.add_parent(officeIdOffset + row["countingCentre"])
        pollingStation.add_parent(electorateIdOffset + row["pollingDistrict"])
