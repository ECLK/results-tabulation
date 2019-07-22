from config import db
from sqlalchemy.orm import relationship
from orm.entities import Election


class Model(db.Model):
    __tablename__ = 'party'
    partyId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    electionId = db.Column(db.Integer, db.ForeignKey(Election.Model.__table__.c.electionId), primary_key=True)

    election = relationship(Election.Model, foreign_keys=[electionId])


Model = Model
