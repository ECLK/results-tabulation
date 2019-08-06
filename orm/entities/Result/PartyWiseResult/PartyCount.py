from app import db
from sqlalchemy.orm import relationship

from orm.entities import Party, ElectionParty
from orm.entities.Result import PartyWiseResult
from exception import NotFoundException


class PartyCountModel(db.Model):
    __tablename__ = 'partyWiseResult_partyCount'
    partyWiseResultId = db.Column(db.Integer, db.ForeignKey(PartyWiseResult.Model.__table__.c.partyWiseResultId),
                                  primary_key=True)
    partyId = db.Column(db.Integer, db.ForeignKey(Party.Model.__table__.c.partyId), primary_key=True)
    # electionId = db.Column(db.Integer, db.ForeignKey(ElectionParty.Model.__table__.c.electionId), primary_key=True)
    count = db.Column(db.Integer)
    countInWords = db.Column(db.String(1000), nullable=True)


Model = PartyCountModel


def create(partyWiseResultId, partyId, count, countInWords=None, electionId=None):
    if electionId is not None:
        electionParty = ElectionParty.get_by_id(electionId=electionId, partyId=partyId)
        if electionParty is None:
            raise NotFoundException("Party is not registered for the given election. (partyId=%d)" % partyId)
    else:
        party = Party.get_by_id(partyId=partyId)
        if party is None:
            raise NotFoundException("Party not found. (partyId=%d)" % partyId)

    result = Model(
        partyWiseResultId=partyWiseResultId,
        partyId=partyId,
        count=count,
        countInWords=countInWords
    )
    db.session.add(result)
    db.session.commit()

    return result
