from datetime import datetime
from config import db, ma
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

import enum


class TallySheetPRE41Model(db.Model):
    __tablename__ = 'tallySheet_PRE-41'
    tallySheetVersionId = db.Column(db.Integer, db.ForeignKey("tallySheet_version.tallySheetVersionId"),
                                    primary_key=True)
    tallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet_version.tallySheetId"))
    electoralDistrictId = db.Column(db.Integer, db.ForeignKey("office.officeId"))
    pollingDivisionId = db.Column(db.Integer, db.ForeignKey("office.officeId"))
    countingCentreId = db.Column(db.Integer, db.ForeignKey("office.officeId"))

    party_wise_results = relationship("TallySheetPRE41PartyModel")

    tallySheetVersion = relationship("TallySheetVersionModel", foreign_keys=[tallySheetVersionId])
    electoralDistrict = relationship("OfficeModel", foreign_keys=[electoralDistrictId])
    pollingDivision = relationship("OfficeModel", foreign_keys=[pollingDivisionId])
    countingCentre = relationship("OfficeModel", foreign_keys=[countingCentreId])

    tallySheet = association_proxy('tallySheetVersion', 'tallySheet')
    code = association_proxy('tallySheetVersion', 'code')
    electionId = association_proxy('tallySheetVersion', 'electionId')
    officeId = association_proxy('tallySheetVersion', 'officeId')
    createdBy = association_proxy('tallySheetVersion', 'createdBy')
    createdAt = association_proxy('tallySheetVersion', 'createdAt')
    latestVersionId = association_proxy('tallySheetVersion', 'latestVersionId')
