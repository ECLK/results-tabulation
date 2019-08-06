from sqlalchemy.orm import relationship

from app import db

from orm.entities import History


class PartyWiseResultModel(db.Model):
    __tablename__ = 'partyWiseResult'
    partyWiseResultId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    resultCounts = relationship("PartyCountModel")


Model = PartyWiseResultModel


def create():
    result = Model()
    db.session.add(result)
    db.session.commit()

    return result
