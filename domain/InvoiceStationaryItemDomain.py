from config import db
from util import Auth
from datetime import datetime

from models import InvoiceStationaryItemModel as Model
from domain import InvoiceDomain, StationaryItemDomain
from exception import NotFoundException, ForbiddenException


def get_all(invoiceId=None, stationaryItemId=None, limit=20, offset=0, received=None, receivedFrom=None,
            receivedBy=None, receivedOffice=None):
    query = Model.query

    if invoiceId is not None:
        query = query.filter(Model.invoiceId == invoiceId)
    if stationaryItemId is not None:
        query = query.filter(Model.stationaryItemId == stationaryItemId)
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
    invoice = InvoiceDomain.get_by_id(invoiceId)

    if invoice is None:
        raise NotFoundException("Invoice not found associated with the given invoiceId (%d)" % invoiceId)
    elif StationaryItemDomain.is_locked(stationaryItemId=stationaryItemId):
        raise ForbiddenException("Stationary item is not available (%d)" % stationaryItemId)
    else:
        if invoice.confirmed:
            raise ForbiddenException("Stationary items cannot be added to confirmed invoices (%d)" % invoiceId)
        else:
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
        raise NotFoundException("Invoice Stationary Item not found associated with the given invoiceId (%d, %d)"
                                % (invoiceId, stationaryItemId))
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
