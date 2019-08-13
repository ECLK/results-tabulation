from util import get_paginated_query
from datetime import datetime
from app import db
from sqlalchemy.orm import relationship
from util import Auth
from exception import NotFoundException, ForbiddenException
from orm.entities import Election
from orm.entities.Area import Office
from sqlalchemy.ext.associationproxy import association_proxy


class InvoiceModel(db.Model):
    __tablename__ = 'invoice'
    invoiceId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    electionId = db.Column(db.Integer, db.ForeignKey(Election.Model.__table__.c.electionId), nullable=False)
    issuingOfficeId = db.Column(db.Integer, db.ForeignKey(Office.Model.__table__.c.areaId), nullable=False)
    receivingOfficeId = db.Column(db.Integer, db.ForeignKey(Office.Model.__table__.c.areaId), nullable=False)
    confirmed = db.Column(db.Boolean, default=False, nullable=False)
    issuedBy = db.Column(db.Integer, nullable=False)
    issuedTo = db.Column(db.Integer, nullable=False)
    issuedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    delete = db.Column(db.Boolean, default=False)

    election = relationship(Election.Model, foreign_keys=[electionId])
    issuingOffice = relationship(Office.Model, foreign_keys=[issuingOfficeId])
    receivingOffice = relationship(Office.Model, foreign_keys=[receivingOfficeId])
    invoiceStationaryItems = relationship("InvoiceStationaryItemModel")

    stationaryItems = association_proxy("invoiceStationaryItems", "stationaryItem")

    def __init__(self, electionId, issuingOfficeId, receivingOfficeId, issuedTo):
        super(InvoiceModel, self).__init__(
            electionId=electionId,
            issuingOfficeId=issuingOfficeId,
            receivingOfficeId=receivingOfficeId,
            issuedTo=issuedTo,
            issuedBy=Auth().get_user_id(),
            issuedAt=datetime.utcnow()
        )

        db.session.add(self)
        db.session.commit()


Model = InvoiceModel


def get_all(electionId=None, issuingOfficeId=None, receivingOfficeId=None, issuedBy=None,
            issuedTo=None):
    query = Model.query.filter(Model.delete == False)

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

    result = get_paginated_query(query).all()

    return result


def get_by_id(invoiceId):
    result = Model.query.filter(
        Model.invoiceId == invoiceId,
        Model.delete == False
    ).one_or_none()

    return result


def create(electionId, issuingOfficeId, receivingOfficeId, issuedTo):
    result = Model(
        electionId=electionId,
        issuingOfficeId=issuingOfficeId,
        receivingOfficeId=receivingOfficeId,
        issuedTo=issuedTo
    )

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


def has_confirmed(invoiceId):
    entry = get_by_id(invoiceId)

    if entry is None:
        raise NotFoundException("Invoice Not Found (invoiceId=%d) " % invoiceId)
    else:
        return entry.confirmed


def delete(invoiceId):
    instance = get_by_id(invoiceId)

    if instance is None:
        raise NotFoundException("Invoice not found associated with the given invoiceId (invoiceId=%d)" % invoiceId)
    elif instance.confirmed:
        raise ForbiddenException("Confirmed invoices cannot be deleted (invoiceId=%d)" % invoiceId)
    else:
        instance.delete = True

        db.session.commit()

        return 1
