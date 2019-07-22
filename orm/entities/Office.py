from config import db
from sqlalchemy.orm import relationship
from orm.enums import OfficeTypeEnum
from orm.entities import Election


class Model(db.Model):
    __tablename__ = 'office'
    officeId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    officeName = db.Column(db.String(100), nullable=False)
    officeType = db.Column(db.Enum(OfficeTypeEnum), nullable=False)
    electionId = db.Column(db.Integer, db.ForeignKey(Election.Model.__table__.c.electionId), nullable=False)
    parentOfficeId = db.Column(db.Integer, db.ForeignKey(officeId), nullable=True)

    election = relationship(Election.Model, foreign_keys=[electionId])
    electorates = relationship(Election.Model, foreign_keys=[electionId])


Model = Model

Model.parentOffice = relationship(Model, foreign_keys=[Model.parentOfficeId])
