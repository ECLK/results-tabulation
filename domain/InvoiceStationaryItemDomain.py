from config import db
from util import Auth
from datetime import datetime

from models import InvoiceStationaryItemModel as Model


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


def update(invoiceId, stationaryItemId, received=False, receivedFrom=None, receivedOfficeId=None):
    instance = get_by_id(invoiceId, stationaryItemId)

    if instance is None:
        # TODO
        return {}
    else:

        if received is not None:
            instance.received = received
        if receivedFrom is not None:
            instance.receivedFrom = receivedFrom
        if receivedOfficeId is not None:
            instance.receivedOfficeId = receivedOfficeId

        instance.receivedBy = Auth().get_user_id()
        instance.receivedAt = datetime.utcnow()

        db.session.commit()

        return instance
