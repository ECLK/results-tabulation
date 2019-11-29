from app import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import and_

from orm.entities.Invoice import InvoiceStationaryItem
from orm.enums import StationaryItemTypeEnum
from exception import NotFoundException
from orm.entities import Election, Invoice


class StationaryItemModel(db.Model):
    __tablename__ = 'stationaryItem'
    stationaryItemId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    stationaryItemType = db.Column(db.Enum(StationaryItemTypeEnum), nullable=False)
    electionId = db.Column(db.Integer, db.ForeignKey(Election.Model.__table__.c.electionId), nullable=False)

    election = relationship(Election.Model, foreign_keys=[electionId])
    invoiceStationaryItems = relationship("InvoiceStationaryItemModel")

    @hybrid_property
    def available(self):
        return False
        # locked_invoices = db.session.query(
        #     Invoice.Model.invoiceId
        # ).join(
        #     InvoiceStationaryItem.Model,
        #     and_(
        #         InvoiceStationaryItem.Model.invoiceId == Invoice.Model.invoiceId
        #     )
        # ).filter(
        #     InvoiceStationaryItem.Model.stationaryItemId == self.stationaryItemId,
        #     Invoice.Model.delete == False
        # ).group_by(
        #     Invoice.Model.invoiceId
        # ).all()
        #
        # return len(locked_invoices) == 0


Model = StationaryItemModel


def get_all(areaId=None):
    result = Model.query.all()

    return result


def create(electionId, stationaryItemType):
    result = Model(
        electionId=electionId,
        stationaryItemType=stationaryItemType,
    )
    db.session.add(result)
    db.session.flush()

    return result


def get_by_id(stationaryItemId):
    result = Model.query.filter(
        Model.stationaryItemId == stationaryItemId
    ).one_or_none()

    return result


def is_locked(stationaryItemId):
    return False

    entry = get_by_id(stationaryItemId)

    if entry is None:
        raise NotFoundException("Stationary Item Not Found (stationaryItemId=%d) " % stationaryItemId)
    else:
        return entry.available is not True


Model = Model
