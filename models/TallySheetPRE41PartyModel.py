from datetime import datetime
from config import db, ma
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

import enum


class TallySheetPRE41PartyModel(db.Model):
    __tablename__ = 'tallySheet_PRE-41__party'
    tallySheetVersionId = db.Column(db.Integer, db.ForeignKey("tallySheet_PRE-41.tallySheetVersionId"),
                                    primary_key=True)
    partyId = db.Column(db.Integer, db.ForeignKey("party.partyId"), primary_key=True)
    voteCount = db.Column(db.Integer)

    party = relationship("PartyModel", foreign_keys=[partyId])
    tallySheetVersion = relationship("TallySheetPRE41Model", foreign_keys=[tallySheetVersionId])
