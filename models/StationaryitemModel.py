from config import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from models import StationaryItemTypeEnum


class StationaryItemModel(db.Model):
    __tablename__ = 'stationaryItem'
    stationaryItemId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    stationaryItemType = db.Column(db.Enum(StationaryItemTypeEnum), nullable=False)
    electionId = db.Column(db.Integer, db.ForeignKey("election.electionId"), nullable=False)

    election = relationship("ElectionModel", foreign_keys=[electionId])
    invoiceStationaryItems = relationship("InvoiceStationaryItemModel")

    @hybrid_property
    def lockedInvoices(self):
        return [i for i in self.invoiceStationaryItems if i.delete == False]

    @hybrid_property
    def locked(self):
        return len([i for i in self.invoiceStationaryItems if i.delete == False]) > 0
