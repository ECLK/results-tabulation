from config import db
from models import InvoiceStationaryItemModel as Model
from util import Auth
from datetime import datetime


def get_all(invoiceId, limit, offset, received=None, receivedFrom=None, receivedBy=None, receivedOffice=None):
    query = Model.query.filter(Model.invoiceId == invoiceId)

    if received is not None:
        query = query.filter(Model.received == received)
    if receivedFrom is not None:
        query = query.filter(Model.receivedFrom == receivedFrom)
    if receivedBy is not None:
        query = query.filter(Model.receivedBy == receivedBy)
    if receivedOffice is not None:
        query = query.filter(Model.receivedOffice == receivedOffice)

    result = query.limit(limit).offset(offset).all()

    return result


def create(invoiceId, stationaryItemId):
    result = Model(
        invoiceId=invoiceId,
        stationaryItemId=stationaryItemId
    )

    db.session.add(result)
    db.session.commit()

    return result


def get_by_id(invoiceId, stationaryItemId):
    result = Model.query.filter(
        Model.invoiceId == invoiceId,
        Model.stationaryItemId == stationaryItemId
    ).one_or_none()

    return result


def update(invoiceId, stationaryItemId, received=False, receivedFrom=None):
    entry = Model.query.filter(
        Model.invoiceId == invoiceId,
        Model.stationaryItemId == stationaryItemId
    ).one_or_none()

    if entry is None:
        return {}
    else:
        entry.receivedFrom = receivedFrom
        entry.received = received

        entry.receivedAt = datetime.utcnow()
        entry.receivedBy = Auth().get_user_id()

        db.session.add(entry)
        db.session.commit()

        return entry
