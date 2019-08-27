from sqlalchemy.ext.associationproxy import association_proxy

from util import get_paginated_query
from app import db
from sqlalchemy.orm import relationship
from orm.enums import StationaryItemTypeEnum
from orm.entities import StationaryItem, Election


class BallotBoxModel(db.Model):
    __tablename__ = 'ballotBox'

    stationaryItemId = db.Column(db.Integer, db.ForeignKey(StationaryItem.Model.__table__.c.stationaryItemId),
                                 primary_key=True, nullable=False)

    ballotBoxId = db.Column(db.String(20), nullable=False, primary_key=True)
    electionId = db.Column(db.Integer, db.ForeignKey(Election.Model.__table__.c.electionId), nullable=False)

    stationaryItem = relationship(StationaryItem.Model, foreign_keys=[stationaryItemId])
    election = relationship(Election.Model, foreign_keys=[electionId])

    locked = association_proxy("stationaryItem", "locked")

    def __init__(self, ballotBoxId, electionId):
        stationary_item = StationaryItem.create(
            electionId=electionId,
            stationaryItemType=StationaryItemTypeEnum.BallotBox
        )

        super(BallotBoxModel, self).__init__(
            ballotBoxId=ballotBoxId,
            electionId=electionId,
            stationaryItemId=stationary_item.stationaryItemId
        )

        db.session.add(self)
        db.session.commit()


Model = BallotBoxModel


def get_by_id(stationaryItemId):
    result = Model.query.filter(
        Model.stationaryItemId == stationaryItemId
    ).one_or_none()

    return result


def get_all(ballotBoxId=None):
    query = Model.query
    if ballotBoxId is not None:
        query = query.filter(
            Model.ballotBoxId.like(ballotBoxId)
        )

    result = get_paginated_query(query).all()

    return result


def create(ballotBoxId, electionId):
    result = Model(
        electionId=electionId,
        ballotBoxId=ballotBoxId,
    )

    return result
