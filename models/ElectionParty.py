from config import db
from sqlalchemy.orm import relationship
from orm.entities import Election, Party


class ElectionPartyModel(db.Model):
    __tablename__ = 'election_party'
    electionId = db.Column(db.Integer, db.ForeignKey(Election.Model.__table__.c.electionId), primary_key=True)
    partyId = db.Column(db.Integer, db.ForeignKey(Party.Model.__table__.c.partyId), primary_key=True)

    election = relationship(Election.Model, foreign_keys=[electionId])
    party = relationship(Party.Model, foreign_keys=[partyId])


Model = ElectionPartyModel


def create(electionId, partyId):
    result = Model(
        electionId=electionId,
        partyId=partyId
    )
    db.session.add(result)
    db.session.commit()

    return result
