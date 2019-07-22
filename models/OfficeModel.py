from config import db
from sqlalchemy.orm import relationship
from models import OfficeTypeEnum


class OfficeModel(db.Model):
    __tablename__ = 'office'
    officeId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    officeName = db.Column(db.String(100), nullable=False)
    officeType = db.Column(db.Enum(OfficeTypeEnum), nullable=False)
    electionId = db.Column(db.Integer, db.ForeignKey("election.electionId"), nullable=False)
    parentOfficeId = db.Column(db.Integer, db.ForeignKey("office.officeId"), nullable=True)

    election = relationship("ElectionModel", foreign_keys=[electionId])
    parentOffice = relationship("OfficeModel", foreign_keys=[parentOfficeId])
    electorates = relationship("ElectionModel", foreign_keys=[electionId])
