from datetime import datetime
from config import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

from orm.entities import TallySheet


class Model(db.Model):
    __tablename__ = 'tallySheet_version'
    tallySheetVersionId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tallySheetId = db.Column(db.Integer, db.ForeignKey(TallySheet.Model.__table__.c.tallySheetId), nullable=False)

    createdBy = db.Column(db.Integer, nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    tallySheet = relationship(TallySheet.Model, foreign_keys=[tallySheetId])

    code = association_proxy('tallySheet', 'code')
    electionId = association_proxy('tallySheet', 'electionId')
    officeId = association_proxy('tallySheet', 'officeId')
    latestVersionId = association_proxy('tallySheet', 'latestVersionId')


TallySheet.latestVersionId = db.Column(db.Integer, db.ForeignKey(Model.__table__.c.tallySheetVersionId), nullable=True)
TallySheet.latestVersion = relationship(Model, foreign_keys=[Model.latestVersionId])
