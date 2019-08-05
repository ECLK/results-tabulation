from app import db
from sqlalchemy.orm import relationship

from orm.entities import Party
from orm.entities.Result import PartyWiseResult

class PartyCountModel(db.Model):
    __tablename__ = 'partyWiseResult_partyCount'
    partyWiseResultId = db.Column(db.Integer, db.ForeignKey(PartyWiseResult.Model.__table__.c.partyWiseResultId), primary_key=True)
    partyId = db.Column(db.Integer, db.ForeignKey(Party.Model.__table__.c.partyId), primary_key=True)
    # electionId = db.Column(db.Integer, db.ForeignKey(ElectionParty.Model.__table__.c.electionId), primary_key=True)
    count = db.Column(db.Integer)


Model = PartyCountModel
