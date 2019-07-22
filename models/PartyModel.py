from config import db
from sqlalchemy.orm import relationship


class PartyModel(db.Model):
    __tablename__ = 'party'
    partyId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    electionId = db.Column(db.Integer, db.ForeignKey("election.electionId"), primary_key=True)

    election = relationship("ElectionModel", foreign_keys=[electionId])
