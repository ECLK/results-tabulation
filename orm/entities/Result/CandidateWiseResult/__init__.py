from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from app import db

from orm.entities import History, Election


class CandidateWiseResultModel(db.Model):
    __tablename__ = 'candidateWiseResult'
    candidateWiseResultId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    resultCounts = relationship("CandidateCountModel")


Model = CandidateWiseResultModel


def create():
    result = Model()
    db.session.add(result)
    db.session.commit()

    return result
