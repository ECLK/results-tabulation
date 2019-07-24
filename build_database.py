from config import db
from orm.entities import *
from orm.entities import *
from orm.enums import ElectorateTypeEnum, StationaryItemTypeEnum, OfficeTypeEnum, FileTypeEnum

# db.engine.execute("create database election")


# Create the database
db.create_all()

# OFFICES = [
#     {"officeId": 0, "officeName": "Colombo", "officeType": OfficeTypeEnum.DistrictCenter, "parentOfficeId": None},
#     {"officeId": 1, "officeName": "", "Moratuwa": OfficeTypeEnum.CountingCenter, "parentOfficeId": 0},
#     {"officeId": 1, "officeName": "", "officeType": OfficeTypeEnum.CountingCenter, "parentOfficeId": 0},
#     {"officeId": 1, "officeName": "", "officeType": OfficeTypeEnum.CountingCenter, "parentOfficeId": 0},
#     {"officeId": 1, "officeName": "", "officeType": OfficeTypeEnum.CountingCenter, "parentOfficeId": 0},
#     {"officeId": 1, "officeName": "Gampaha", "officeType": OfficeTypeEnum.DistrictCenter, "parentOfficeId": None},
#     {"officeId": 2, "officeName": "Kalutara South", "officeType": OfficeTypeEnum.DistrictCenter, "parentOfficeId": None},
#     {"officeId": 3, "officeName": "Kalutara North", "officeType": OfficeTypeEnum.DistrictCenter, "parentOfficeId": None}
# ]

for i in range(1, 2):
    election = Election.create()
    db.session.add(election)
    db.session.commit()

    for i in range(1, 6):
        db.session.add(Party.create(
            partyName="Party-%d" % i
        ))
        db.session.commit()

    for j in range(1, 20):
        db.session.add(Office.create(
            electionId=election.electionId,
            officeType=OfficeTypeEnum.DistrictCenter,
            officeName="Office %d" % j
        ))
        db.session.add(Electorate.create(
            electionId=election.electionId,
            electorateType=ElectorateTypeEnum.AdministrativeDistrict,
            electorateName="Electorate %d" % j
        ))

    for i in range(1, 10):
        db.session.add(Ballot.create(
            electionId=election.electionId,
            ballotId="pre-ballot-%d-%d" % (election.electionId, i)
        ))

    for i in range(1, 50):
        db.session.add(BallotBox.create(
            electionId=election.electionId,
            ballotBoxId="pre-ballot-box-%d-%d" % (election.electionId, i)
        ))

db.session.commit()
