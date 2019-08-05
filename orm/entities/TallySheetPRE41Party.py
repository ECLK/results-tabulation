from app import db
from sqlalchemy.orm import relationship

from orm.entities import TallySheetPRE41, ElectionParty, Party


class TallySheetPRE41PartyModel(db.Model):
    __tablename__ = 'tallySheet_PRE-41__party'
    tallySheetVersionId = db.Column(db.Integer, db.ForeignKey(TallySheetPRE41.Model.__table__.c.tallySheetVersionId),
                                    primary_key=True)
    partyId = db.Column(db.Integer, db.ForeignKey(Party.Model.__table__.c.partyId), primary_key=True)
    # electionId = db.Column(db.Integer, db.ForeignKey(ElectionParty.Model.__table__.c.electionId), primary_key=True)
    voteCount = db.Column(db.Integer)

    tallySheetVersion = relationship(TallySheetPRE41.Model, foreign_keys=[tallySheetVersionId])


Model = TallySheetPRE41PartyModel
