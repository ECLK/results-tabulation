from util import get_paginated_query
from datetime import datetime
from app import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from util import Auth
from orm.entities import Invoice, StationaryItem, Proof
from orm.entities.Area import Office
from orm.enums import ProofTypeEnum
from exception import NotFoundException, ForbiddenException


class InvoiceStationaryItemModel(db.Model):
    __tablename__ = 'invoice_stationaryItem'
    invoiceId = db.Column(db.Integer, db.ForeignKey("invoice.invoiceId"), primary_key=True)
    stationaryItemId = db.Column(db.Integer, db.ForeignKey("stationaryItem.stationaryItemId"),
                                 primary_key=True)
    received = db.Column(db.Boolean, default=False, nullable=False)
    receivedBy = db.Column(db.Integer, nullable=True)
    receivedFrom = db.Column(db.Integer, nullable=True)
    receivedAt = db.Column(db.DateTime, default=None, onupdate=datetime.utcnow, nullable=True)
    receivedOfficeId = db.Column(db.Integer, db.ForeignKey(Office.Model.__table__.c.areaId), nullable=True)
    receivedProofId = db.Column(db.Integer, db.ForeignKey(Proof.Model.__table__.c.proofId),
                                nullable=True)

    receivedProof = relationship(Proof.Model, foreign_keys=[receivedProofId])
    receivedOffice = relationship(Office.Model, foreign_keys=[receivedOfficeId])
    stationaryItem = relationship("StationaryItemModel", foreign_keys=[stationaryItemId])
    invoice = relationship("InvoiceModel", foreign_keys=[invoiceId])

    delete = association_proxy('invoice', 'delete')
    receivedScannedFiles = association_proxy("receivedProof", "scannedFiles")

    def __init__(self, invoiceId, stationaryItemId):
        if Invoice.has_confirmed(invoiceId):
            raise ForbiddenException("Stationary items cannot be added to confirmed invoices (%d)" % invoiceId)
        elif StationaryItem.is_locked(stationaryItemId):
            raise ForbiddenException("Stationary item is not available (%d)" % stationaryItemId)
        else:
            received_proof = Proof.create(
                proofType=ProofTypeEnum.InvoiceStationaryItemReceive
            )

            super(InvoiceStationaryItemModel, self).__init__(
                invoiceId=invoiceId,
                stationaryItemId=stationaryItemId,
                receivedProofId=received_proof.proofId
            )


Model = InvoiceStationaryItemModel


def get_all(invoiceId=None, stationaryItemId=None, received=None, receivedFrom=None,
            receivedBy=None, receivedOffice=None):
    query = Model.query.filter(Model.delete == False)

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

    result = get_paginated_query(query).all()

    return result


def create(invoiceId, stationaryItemId):
    result = Model(
        invoiceId=invoiceId,
        stationaryItemId=stationaryItemId,
    )

    db.session.add(result)
    db.session.commit()

    return result


def get_by_id(invoiceId, stationaryItemId):
    result = Model.query.filter(
        Model.invoiceId == invoiceId,
        Model.stationaryItemId == stationaryItemId,
        Model.delete == False
    ).one_or_none()

    return result


def update(invoiceId, stationaryItemId, received=False, receivedFrom=None, receivedOfficeId=None, scannedImages=None):
    instance = get_by_id(invoiceId, stationaryItemId)

    # if scannedImages is not None:
    #     file = Image.create(fileSource=scannedImages)
    #     FolderFile.create(folderId=instance.receivedScannedFilesFolderId, fileId=file.fileId)

    # TODO support muliple images
    # https://github.com/zalando/connexion/issues/510

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

        if instance.received is True:
            Proof.update(
                proofId=instance.receivedProofId,
                finished=True
            )

        instance.receivedBy = Auth().get_user_id()
        instance.receivedAt = datetime.utcnow()

        db.session.commit()

        return instance


def delete(invoiceId, stationaryItemId):
    if Invoice.has_confirmed(invoiceId):
        raise ForbiddenException("Stationary items cannot be deleted from confirmed invoices (%d)" % invoiceId)
    else:
        result = Model.query.filter(
            Model.invoiceId == invoiceId,
            Model.stationaryItemId == stationaryItemId
        ).delete()

        db.session.commit()

        return result
