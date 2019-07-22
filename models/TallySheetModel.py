from config import db, ma
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

import enum


class TallySheetModel(db.Model):
    __tablename__ = 'tallySheet'
    tallySheetId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(10), index=True, nullable=False)
    electionId = db.Column(db.Integer, db.ForeignKey("election.electionId"), nullable=False)
    officeId = db.Column(db.Integer, db.ForeignKey("office.officeId"), nullable=False)
    latestVersionId = db.Column(db.Integer, db.ForeignKey("tallySheet_version.tallySheetVersionId"), nullable=True)

    election = relationship("ElectionModel", foreign_keys=[electionId])
    office = relationship("OfficeModel", foreign_keys=[officeId])
    latestVersion = relationship("TallySheetVersionModel", foreign_keys=[latestVersionId])
