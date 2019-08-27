from util import get_paginated_query
from app import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from orm.enums import StationaryItemTypeEnum
from orm.entities import StationaryItem, Election


class BallotModel(db.Model):
    __tablename__ = 'ballot'
    stationaryItemId = db.Column(db.Integer, db.ForeignKey(StationaryItem.Model.__table__.c.stationaryItemId),
                                 primary_key=True, nullable=False)
    ballotId = db.Column(db.String(20), nullable=False, primary_key=True)
    electionId = db.Column(db.Integer, db.ForeignKey(Election.Model.__table__.c.electionId), nullable=False)

    stationaryItem = relationship(StationaryItem.Model, foreign_keys=[stationaryItemId])
    election = relationship(Election.Model, foreign_keys=[electionId])

    locked = association_proxy("stationaryItem", "locked")

    __table_args__ = (
        db.UniqueConstraint('ballotId', 'electionId', name='BallotPerElection'),
    )

    def __init__(self, ballotId, electionId):
        stationary_item = StationaryItem.create(
            electionId=electionId,
            stationaryItemType=StationaryItemTypeEnum.Ballot
        )

        super(BallotModel, self).__init__(
            ballotId=ballotId,
            electionId=electionId,
            stationaryItemId=stationary_item.stationaryItemId
        )

        db.session.add(self)
        db.session.commit()


Model = BallotModel


def get_by_id(stationaryItemId):
    result = Model.query.filter(
        Model.stationaryItemId == stationaryItemId
    ).one_or_none()

    return result


def get_all(ballotId=None):
    query = Model.query
    if ballotId is not None:
        query = query.filter(
            Model.ballotId.like(ballotId)
        )

    result = get_paginated_query(query).all()

    return result


def create(ballotId, electionId):
    result = Model(
        electionId=electionId,
        ballotId=ballotId,
    )

    return result
