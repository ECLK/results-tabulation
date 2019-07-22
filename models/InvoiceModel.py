from datetime import datetime
from config import db, ma
from sqlalchemy.orm import relationship


class InvoiceModel(db.Model):
    __tablename__ = 'invoice'
    invoiceId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    electionId = db.Column(db.Integer, db.ForeignKey("election.electionId"), nullable=False)
    issuingOfficeId = db.Column(db.Integer, db.ForeignKey("office.officeId"), nullable=False)
    receivingOfficeId = db.Column(db.Integer, db.ForeignKey("office.officeId"), nullable=False)
    confirmed = db.Column(db.Boolean, default=False, nullable=False)
    issuedBy = db.Column(db.Integer, nullable=False)
    issuedTo = db.Column(db.Integer, nullable=False)
    issuedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    delete = db.Column(db.Boolean, default=False)

    election = relationship("ElectionModel", foreign_keys=[electionId])
    issuingOffice = relationship("OfficeModel", foreign_keys=[issuingOfficeId])
    receivingOffice = relationship("OfficeModel", foreign_keys=[receivingOfficeId])
    stationaryItems = relationship("InvoiceStationaryItemModel")
