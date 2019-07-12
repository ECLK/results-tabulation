from config import db
from util import Auth
from datetime import datetime

from models import InvoiceModel as Model
from exception import NotFoundException


def get_all(limit, offset, electionId=None, issuingOfficeId=None, receivingOfficeId=None, issuedBy=None,
            issuedTo=None):
    query = Model.query

    if electionId is not None:
        query = query.filter(Model.electionId == electionId)

    if issuingOfficeId is not None:
        query = query.filter(Model.issuingOfficeId == issuingOfficeId)

    if receivingOfficeId is not None:
        query = query.filter(Model.receivingOfficeId == receivingOfficeId)

    if issuedBy is not None:
        query = query.filter(Model.issuedBy == issuedBy)

    if issuedTo is not None:
        query = query.filter(Model.issuedTo == issuedTo)

    result = query.limit(limit).offset(offset).all()

    return result


def get_by_id(invoiceId):
    result = Model.query.filter(
        Model.invoiceId == invoiceId
    ).one_or_none()

    return result


def create(electionId, issuingOfficeId, receivingOfficeId, issuedTo):
    result = Model(
        electionId=electionId,
        issuingOfficeId=issuingOfficeId,
        receivingOfficeId=receivingOfficeId,
        issuedTo=issuedTo,
        issuedBy=Auth().get_user_id(),
        issuedAt=datetime.utcnow()
    )

    db.session.add(result)
    db.session.commit()

    return result


def update(invoiceId, issuingOfficeId=None, receivingOfficeId=None, issuedTo=None, confirmed=None):
    instance = get_by_id(invoiceId)

    if instance is None:
        raise NotFoundException("Invoice not found associated with the given invoiceId (%d)" % invoiceId)
    else:
        if issuingOfficeId is not None:
            instance.issuingOfficeId = issuingOfficeId
        if receivingOfficeId is not None:
            instance.receivingOfficeId = receivingOfficeId
        if issuedTo is not None:
            instance.issuedTo = issuedTo
        if confirmed is not None:
            instance.confirmed = confirmed

        db.session.commit()

        return instance
