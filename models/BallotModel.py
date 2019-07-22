from config import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy


class BallotModel(db.Model):
    __tablename__ = 'ballot'
    ballotId = db.Column(db.String(20), primary_key=True)
    electionId = db.Column(db.Integer, db.ForeignKey("election.electionId"), primary_key=True)
    stationaryItemId = db.Column(db.Integer, db.ForeignKey("stationaryItem.stationaryItemId"), nullable=False,
                                 unique=True)

    stationaryItem = relationship("StationaryItemModel", foreign_keys=[stationaryItemId])
    election = relationship("ElectionModel", foreign_keys=[electionId])

    locked = association_proxy("stationaryItem", "locked")
