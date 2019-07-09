import os
from config import db
from models import PartyModel, OfficeModel, ElectorateModel, ElectionModel, BallotModel, BallotBoxModel, StationaryItemModel

# db.engine.execute("create database election")


# Create the database
db.create_all()

for i in range(1, 6):
    election = ElectionModel()
    db.session.add(election)
    db.session.commit()

    for i in range(1, 6):
        db.session.add(PartyModel(electionId=election.electionId))
        db.session.commit()

    for j in range(1, 20):
        db.session.add(OfficeModel(electionId=election.electionId))
        db.session.add(ElectorateModel(electionId=election.electionId))

for i in range(1, 20):
    stationary_item = StationaryItemModel()

    db.session.add(stationary_item)
    db.session.commit()

    db.session.add(BallotModel(
        ballotId="pre-ballot-%d" % i,
        stationaryItemId=stationary_item.stationaryItemId
    ))

for i in range(1, 200):
    stationary_item = StationaryItemModel()

    db.session.add(stationary_item)
    db.session.commit()

    db.session.add(BallotBoxModel(
        ballotBoxId="pre-ballot-box-%d" % i,
        stationaryItemId=stationary_item.stationaryItemId
    ))

db.session.commit()
