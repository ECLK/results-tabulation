from config import db
from sqlalchemy.orm import relationship


class BallotBoxModel(db.Model):
    __tablename__ = 'ballotBox'
    ballotBoxId = db.Column(db.String(20), primary_key=True)
    electionId = db.Column(db.Integer, db.ForeignKey("election.electionId"), primary_key=True)
    stationaryItemId = db.Column(db.Integer, db.ForeignKey("stationaryItem.stationaryItemId"), nullable=False,
                                 unique=True)

    stationaryItem = relationship("StationaryItemModel", foreign_keys=[stationaryItemId])
    election = relationship("ElectionModel", foreign_keys=[electionId])

    # locked = association_proxy("stationaryItem", "locked")
