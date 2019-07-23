from config import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from orm.enums import StationaryItemTypeEnum
from orm.entities import StationaryItem, Election


class BallotModel(db.Model):
    __tablename__ = 'ballot'
    ballotId = db.Column(db.String(20), primary_key=True)
    electionId = db.Column(db.Integer, db.ForeignKey(Election.Model.__table__.c.electionId), primary_key=True)
    stationaryItemId = db.Column(db.Integer, db.ForeignKey(StationaryItem.Model.__table__.c.stationaryItemId),
                                 nullable=False, unique=True)

    stationaryItem = relationship(StationaryItem.Model, foreign_keys=[stationaryItemId])
    election = relationship(Election.Model, foreign_keys=[electionId])

    locked = association_proxy("stationaryItem", "locked")

    def __init__(self, ballotId, electionId):
        stationary_item = StationaryItem.create(
            electionId=electionId,
            stationaryItemType=StationaryItemTypeEnum.Ballot
        )

        self.ballotId = ballotId
        self.electionId = electionId
        self.stationaryItemId = stationary_item.stationaryItemId


Model = BallotModel


def get_all():
    result = Model.query.all()

    return result


def create(ballotId, electionId):
    result = Model(
        electionId=electionId,
        ballotId=ballotId,
    )
    db.session.add(result)
    db.session.commit()

    return result
