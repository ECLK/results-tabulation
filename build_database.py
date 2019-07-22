from config import db
from orm.entities import Party, StationaryItem, Ballot, Electorate, Office, BallotBox, Election
from orm.enums import ElectorateTypeEnum, StationaryItemTypeEnum, OfficeTypeEnum

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
    election = Election()
    db.session.add(election)
    db.session.commit()

    for i in range(1, 6):
        db.session.add(Party(electionId=election.electionId))
        db.session.commit()

    for j in range(1, 20):
        db.session.add(Office(
            electionId=election.electionId,
            officeType=OfficeTypeEnum.DistrictCenter,
            officeName="Office %d" % j
        ))
        db.session.add(Electorate(
            electionId=election.electionId,
            electorateType=ElectorateTypeEnum.AdministrativeDistrict,
            electorateName="Electorate %d" % j
        ))

    for i in range(1, 10):
        stationary_item = StationaryItem(stationaryItemType=StationaryItemTypeEnum.Ballot,
                                         electionId=election.electionId)

        db.session.add(stationary_item)
        db.session.commit()

        db.session.add(Ballot(
            electionId=election.electionId,
            ballotId="pre-ballot-%d-%d" % (election.electionId, i),
            stationaryItemId=stationary_item.stationaryItemId
        ))

    for i in range(1, 50):
        stationary_item = StationaryItem(stationaryItemType=StationaryItemTypeEnum.BallotBox,
                                         electionId=election.electionId)

        db.session.add(stationary_item)
        db.session.commit()

        db.session.add(BallotBox(
            electionId=election.electionId,
            ballotBoxId="pre-ballot-box-%d-%d" % (election.electionId, i),
            stationaryItemId=stationary_item.stationaryItemId
        ))

db.session.commit()
