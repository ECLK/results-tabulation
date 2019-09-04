from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import and_, Integer, func
from sqlalchemy.sql.expression import cast

from exception import NotFoundException
from orm.entities.Invoice import InvoiceStationaryItem
from util import get_paginated_query
from app import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from orm.enums import StationaryItemTypeEnum
from orm.entities import StationaryItem, Election, Ballot, Invoice


class BallotBookModel(db.Model):
    __tablename__ = 'ballotBook'
    stationaryItemId = db.Column(db.Integer, db.ForeignKey(StationaryItem.Model.__table__.c.stationaryItemId),
                                 primary_key=True, nullable=False)
    fromBallotStationaryItemId = db.Column(db.Integer, db.ForeignKey(Ballot.Model.__table__.c.stationaryItemId),
                                           nullable=False)
    toBallotStationaryItemId = db.Column(db.Integer, db.ForeignKey(Ballot.Model.__table__.c.stationaryItemId),
                                         nullable=False)

    stationaryItem = relationship(StationaryItem.Model, foreign_keys=[stationaryItemId])
    fromBallot = relationship(Ballot.Model, foreign_keys=[fromBallotStationaryItemId])
    toBallot = relationship(Ballot.Model, foreign_keys=[toBallotStationaryItemId])

    electionId = association_proxy("stationaryItem", "electionId")
    election = association_proxy("stationaryItem", "election")
    fromBallotId = association_proxy("fromBallot", "ballotId")
    toBallotId = association_proxy("toBallot", "ballotId")

    @hybrid_property
    def ballots(self):
        return Ballot.Model.query.filter(
            and_(
                cast(Ballot.Model.ballotId, Integer) >= cast(self.fromBallotId, Integer),
                cast(Ballot.Model.ballotId, Integer) <= cast(self.toBallotId, Integer)
            )
        ).filter(
            Ballot.Model.electionId == self.electionId
        ).all()

    @hybrid_property
    def available(self):
        locked_invoices = db.session.query(
            Invoice.Model.invoiceId
        ).join(
            InvoiceStationaryItem.Model,
            and_(
                InvoiceStationaryItem.Model.invoiceId == Invoice.Model.invoiceId
            )
        ).join(
            Ballot.Model,
            and_(
                Ballot.Model.stationaryItemId == InvoiceStationaryItem.Model.stationaryItemId,
                cast(Ballot.Model.ballotId, Integer) >= cast(self.fromBallotId, Integer),
                cast(Ballot.Model.ballotId, Integer) <= cast(self.toBallotId, Integer)
            )
        ).filter(
            Invoice.Model.delete == False
        ).group_by(
            Invoice.Model.invoiceId
        ).all()

        return len(locked_invoices) == 0

    def __init__(self, electionId, fromBallotId, toBallotId):
        fromBallot = Ballot.get_all(ballotId=fromBallotId, electionId=electionId)
        toBallot = Ballot.get_all(ballotId=toBallotId, electionId=electionId)

        if len(fromBallot) is 0:
            raise NotFoundException("Ballot not found (ballotId=%s)" % fromBallotId)
        else:
            fromBallot = fromBallot[0]

        if len(toBallot) is 0:
            raise NotFoundException("Ballot not found (ballotId=%s)" % toBallotId)
        else:
            toBallot = toBallot[0]

        stationary_item = StationaryItem.create(
            electionId=electionId,
            stationaryItemType=StationaryItemTypeEnum.Ballot
        )

        super(BallotBookModel, self).__init__(
            fromBallotStationaryItemId=fromBallot.stationaryItemId,
            toBallotStationaryItemId=toBallot.stationaryItemId,
            stationaryItemId=stationary_item.stationaryItemId
        )

        db.session.add(self)
        db.session.flush()


Model = BallotBookModel


def get_by_id(stationaryItemId):
    result = Model.query.filter(
        Model.stationaryItemId == stationaryItemId
    ).one_or_none()

    return result


def get_all(ballotId=None):
    query = Model.query
    # if ballotId is not None:
    #     query = query.filter(
    #         Model.ballotId.like(ballotId)
    #     )

    result = get_paginated_query(query).all()

    return result


def create(electionId, fromBallotId, toBallotId):
    result = Model(
        electionId=electionId,
        fromBallotId=fromBallotId,
        toBallotId=toBallotId,
    )

    return result
