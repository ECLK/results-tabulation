from config import db
from sqlalchemy.orm import relationship

from orm.entities import Party, TallySheetPRE41


class Model(db.Model):
    __tablename__ = 'tallySheet_PRE-41__party'
    tallySheetVersionId = db.Column(db.Integer, db.ForeignKey(TallySheetPRE41.Model.__table__.c.tallySheetVersionId),
                                    primary_key=True)
    partyId = db.Column(db.Integer, db.ForeignKey(Party.Model.__table__.c.partyId), primary_key=True)
    voteCount = db.Column(db.Integer)

    party = relationship(Party.Model, foreign_keys=[partyId])
    tallySheetVersion = relationship(TallySheetPRE41.Model, foreign_keys=[tallySheetVersionId])


TallySheetPRE41.party_wise_results = relationship(Model)