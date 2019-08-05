from util import get_paginated_query
from app import db
from sqlalchemy.orm import relationship
from orm.enums import StationaryItemTypeEnum
from orm.entities import StationaryItem, Election


class BallotBoxModel(db.Model):
    __tablename__ = 'ballotBox'
    ballotBoxId = db.Column(db.String(20), primary_key=True)
    electionId = db.Column(db.Integer, db.ForeignKey(Election.Model.__table__.c.electionId), primary_key=True)
    stationaryItemId = db.Column(db.Integer, db.ForeignKey(StationaryItem.Model.__table__.c.stationaryItemId),
                                 nullable=False, unique=True)

    stationaryItem = relationship(StationaryItem.Model, foreign_keys=[stationaryItemId])
    election = relationship(Election.Model, foreign_keys=[electionId])

    # locked = association_proxy("stationaryItem", "locked")

    def __init__(self, ballotBoxId, electionId):
        stationary_item = StationaryItem.create(
            electionId=electionId,
            stationaryItemType=StationaryItemTypeEnum.BallotBox
        )

        self.ballotBoxId = ballotBoxId
        self.electionId = electionId
        self.stationaryItemId = stationary_item.stationaryItemId


Model = BallotBoxModel


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
    db.session.add(result)
    db.session.commit()

    return result
