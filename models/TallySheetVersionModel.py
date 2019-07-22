from datetime import datetime
from config import db, ma
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

import enum


class TallySheetVersionModel(db.Model):
    __tablename__ = 'tallySheet_version'
    tallySheetVersionId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), nullable=False)

    createdBy = db.Column(db.Integer, nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    tallySheet = relationship("TallySheetModel", foreign_keys=[tallySheetId])

    code = association_proxy('tallySheet', 'code')
    electionId = association_proxy('tallySheet', 'electionId')
    officeId = association_proxy('tallySheet', 'officeId')
    latestVersionId = association_proxy('tallySheet', 'latestVersionId')
