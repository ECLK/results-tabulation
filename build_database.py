import os
from config import db
from models import PartyModel, OfficeModel, ElectorateModel, ElectionModel, BallotModel, BallotBoxModel, \
    StationaryItemModel, InvoiceModel, ElectorateTypeEnum, OfficeTypeEnum, StationaryItemTypeEnum

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
    election = ElectionModel()
    db.session.add(election)
    db.session.commit()

    for i in range(1, 6):
        db.session.add(PartyModel(electionId=election.electionId))
        db.session.commit()

    for j in range(1, 20):
        db.session.add(OfficeModel(
            electionId=election.electionId,
            officeType=OfficeTypeEnum.DistrictCenter,
            officeName="Office %d" % j
        ))
        db.session.add(ElectorateModel(
            electionId=election.electionId,
            electorateType=ElectorateTypeEnum.AdministrativeDistrict,
            electorateName="Electorate %d" % j
        ))

    for i in range(1, 10):
        stationary_item = StationaryItemModel(stationaryItemType=StationaryItemTypeEnum.Ballot,
                                              electionId=election.electionId)

        db.session.add(stationary_item)
        db.session.commit()

        db.session.add(BallotModel(
            ballotId="pre-ballot-%d-%d" % (election.electionId, i),
            stationaryItemId=stationary_item.stationaryItemId
        ))

    for i in range(1, 50):
        stationary_item = StationaryItemModel(stationaryItemType=StationaryItemTypeEnum.BallotBox,
                                              electionId=election.electionId)

        db.session.add(stationary_item)
        db.session.commit()

        db.session.add(BallotBoxModel(
            ballotBoxId="pre-ballot-box-%d-%d" % (election.electionId, i),
            stationaryItemId=stationary_item.stationaryItemId
        ))

db.session.commit()
