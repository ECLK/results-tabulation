from datetime import datetime
from config import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from util import Auth
from orm.entities import FileCollection, Office, Invoice, StationaryItem
from exception import NotFoundException, ForbiddenException


class Model(db.Model):
    __tablename__ = 'invoice_stationaryItem'
    invoiceId = db.Column(db.Integer, db.ForeignKey(Invoice.Model.__table__.c.invoiceId), primary_key=True)
    stationaryItemId = db.Column(db.Integer, db.ForeignKey(StationaryItem.Model.__table__.c.stationaryItemId),
                                 primary_key=True)
    received = db.Column(db.Boolean, default=False, nullable=False)
    receivedBy = db.Column(db.Integer, nullable=True)
    receivedFrom = db.Column(db.Integer, nullable=True)
    receivedAt = db.Column(db.DateTime, default=None, onupdate=datetime.utcnow, nullable=True)
    receivedOfficeId = db.Column(db.Integer, db.ForeignKey(Office.Model.__table__.c.officeId), nullable=True)
    receivedScannedFilesCollectionId = db.Column(db.Integer,
                                                 db.ForeignKey(FileCollection.Model.__table__.c.fileCollectionId),
                                                 nullable=True)

    receivedScannedFilesCollection = relationship(FileCollection.Model,
                                                  foreign_keys=[receivedScannedFilesCollectionId])
    receivedOffice = relationship(Office.Model, foreign_keys=[receivedOfficeId])
    stationaryItem = relationship(StationaryItem.Model, foreign_keys=[stationaryItemId])
    invoice = relationship(Invoice.Model, foreign_keys=[invoiceId])

    delete = association_proxy('invoice', 'delete')
    receivedScannedFiles = association_proxy("receivedScannedFilesCollection", "files")


StationaryItem.invoiceStationaryItems = relationship(Model)


def get_all(invoiceId=None, stationaryItemId=None, limit=20, offset=0, received=None, receivedFrom=None,
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

    result = query.limit(limit).offset(offset).all()

    return result


def create(invoiceId, stationaryItemId):
    if Invoice.has_confirmed(invoiceId):
        raise ForbiddenException("Stationary items cannot be added to confirmed invoices (%d)" % invoiceId)
    elif StationaryItem.is_locked(stationaryItemId):
        raise ForbiddenException("Stationary item is not available (%d)" % stationaryItemId)
    else:
        received_scanned_files_collection = FileCollection.create()

        result = Model(
            invoiceId=invoiceId,
            stationaryItemId=stationaryItemId,
            receivedScannedFilesCollectionId=received_scanned_files_collection.fileCollectionId
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
