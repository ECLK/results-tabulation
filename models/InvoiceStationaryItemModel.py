from datetime import datetime
from config import db, ma
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy


class InvoiceStationaryItemModel(db.Model):
    __tablename__ = 'invoice_stationaryItem'
    invoiceId = db.Column(db.Integer, db.ForeignKey("invoice.invoiceId"), primary_key=True)
    stationaryItemId = db.Column(db.Integer, db.ForeignKey("stationaryItem.stationaryItemId"), primary_key=True)
    received = db.Column(db.Boolean, default=False, nullable=False)
    receivedBy = db.Column(db.Integer, nullable=True)
    receivedFrom = db.Column(db.Integer, nullable=True)
    receivedAt = db.Column(db.DateTime, default=None, onupdate=datetime.utcnow, nullable=True)
    receivedOfficeId = db.Column(db.Integer, db.ForeignKey("office.officeId"), nullable=True)
    receivedScannedFilesCollectionId = db.Column(db.Integer, db.ForeignKey("file_collection.fileCollectionId"),
                                                 nullable=True)

    receivedScannedFilesCollection = relationship("FileCollectionModel",
                                                  foreign_keys=[receivedScannedFilesCollectionId])
    receivedOffice = relationship("OfficeModel", foreign_keys=[receivedOfficeId])
    stationaryItem = relationship("StationaryItemModel", foreign_keys=[stationaryItemId])
    invoice = relationship("InvoiceModel", foreign_keys=[invoiceId])

    delete = association_proxy('invoice', 'delete')

    receivedScannedFiles = association_proxy("receivedScannedFilesCollection", "files")
