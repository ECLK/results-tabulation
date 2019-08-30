from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import and_, cast, Integer

from orm.entities.Invoice import InvoiceStationaryItem
from util import get_paginated_query
from app import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from orm.enums import StationaryItemTypeEnum, BallotTypeEnum
from orm.entities import StationaryItem, Election, Invoice


class BallotModel(db.Model):
    __tablename__ = 'ballot'
    stationaryItemId = db.Column(db.Integer, db.ForeignKey(StationaryItem.Model.__table__.c.stationaryItemId),
                                 primary_key=True, nullable=False)
    ballotId = db.Column(db.String(20), nullable=False, primary_key=True)
    electionId = db.Column(db.Integer, db.ForeignKey(Election.Model.__table__.c.electionId), nullable=False)
    ballotType = db.Column(db.Enum(BallotTypeEnum), nullable=False, default=BallotTypeEnum.Ordinary)

    stationaryItem = relationship(StationaryItem.Model, foreign_keys=[stationaryItemId])
    election = relationship(Election.Model, foreign_keys=[electionId])

    __table_args__ = (
        db.UniqueConstraint('ballotId', 'electionId', name='BallotPerElection'),
    )

    def __init__(self, ballotId, electionId, ballotType=BallotTypeEnum.Ordinary):
        stationary_item = StationaryItem.create(
            electionId=electionId,
            stationaryItemType=StationaryItemTypeEnum.Ballot
        )

        super(BallotModel, self).__init__(
            ballotId=ballotId,
            electionId=electionId,
            stationaryItemId=stationary_item.stationaryItemId,
            ballotType=ballotType
        )

    @hybrid_property
    def available(self):
        locked_invoices = db.session.query(
            Invoice.Model.invoiceId
        ).join(
            InvoiceStationaryItem.Model,
            and_(
                InvoiceStationaryItem.Model.invoiceId == Invoice.Model.invoiceId
            )
        ).filter(
            InvoiceStationaryItem.Model.stationaryItemId == self.stationaryItemId,
            Invoice.Model.delete == False
        ).group_by(
            Invoice.Model.invoiceId
        ).all()

        return len(locked_invoices) == 0


Model = BallotModel


def get_by_id(stationaryItemId):
    result = Model.query.filter(
        Model.stationaryItemId == stationaryItemId
    ).one_or_none()

    return result


def get_all(ballotId=None, stationaryItemId=None, electionId=None, ballotType=None):
    query = Model.query
    if ballotId is not None:
        query = query.filter(
            Model.ballotId.like(ballotId)
        )

    if stationaryItemId is not None:
        query = query.filter(
            Model.stationaryItemId == stationaryItemId
        )

    if ballotType is not None:
        query = query.filter(
            Model.ballotType == ballotType
        )

    if electionId is not None:
        query = query.filter(
            Model.electionId == electionId
        )

    query = query.order_by(cast(Model.ballotId, Integer))

    result = get_paginated_query(query).all()
    return result


def create(ballotId, electionId, ballotType=None):
    result = Model(
        electionId=electionId,
        ballotId=ballotId,
        ballotType=ballotType
    )

    db.session.add(result)
    db.session.commit()

    return result
