from config import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

from orm.entities import Office, TallySheetVersion


class TallySheetPRE41Model(db.Model):
    __tablename__ = 'tallySheet_PRE-41'
    tallySheetVersionId = db.Column(db.Integer, db.ForeignKey(TallySheetVersion.Model.__table__.c.tallySheetVersionId),
                                    primary_key=True)
    electoralDistrictId = db.Column(db.Integer, db.ForeignKey(Office.Model.__table__.c.officeId))
    pollingDivisionId = db.Column(db.Integer, db.ForeignKey(Office.Model.__table__.c.officeId))
    countingCentreId = db.Column(db.Integer, db.ForeignKey(Office.Model.__table__.c.officeId))

    tallySheetVersion = relationship(TallySheetVersion.Model, foreign_keys=[tallySheetVersionId])
    electoralDistrict = relationship(Office.Model, foreign_keys=[electoralDistrictId])
    pollingDivision = relationship(Office.Model, foreign_keys=[pollingDivisionId])
    countingCentre = relationship(Office.Model, foreign_keys=[countingCentreId])
    party_wise_results = relationship('TallySheetPRE41PartyModel')

    tallySheet = association_proxy('tallySheetVersion', 'tallySheet')
    tallySheetId = association_proxy('tallySheet', 'tallySheetId')
    code = association_proxy('tallySheetVersion', 'code')
    electionId = association_proxy('tallySheetVersion', 'electionId')
    officeId = association_proxy('tallySheetVersion', 'officeId')
    createdBy = association_proxy('tallySheetVersion', 'createdBy')
    createdAt = association_proxy('tallySheetVersion', 'createdAt')
    latestVersionId = association_proxy('tallySheetVersion', 'latestVersionId')


Model = TallySheetPRE41Model
