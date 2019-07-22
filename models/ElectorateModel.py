from config import db
from sqlalchemy.orm import relationship
from models import ElectorateTypeEnum


class ElectorateModel(db.Model):
    __tablename__ = 'electorate'
    electorateId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    electorateName = db.Column(db.String(100), nullable=False)
    electorateType = db.Column(db.Enum(ElectorateTypeEnum), nullable=False)
    electionId = db.Column(db.Integer, db.ForeignKey("election.electionId"), nullable=False)
    parentElectorateId = db.Column(db.Integer, db.ForeignKey("electorate.electorateId"), nullable=True)

    election = relationship("ElectionModel", foreign_keys=[electionId])
    parentElectorate = relationship("ElectorateModel", foreign_keys=[parentElectorateId])
