from sqlalchemy.orm import relationship

from app import db

from orm.entities import Candidate
from orm.entities import Candidate
from orm.entities.Election import ElectionCandidate
from orm.entities.Result import CandidateWiseResult
from exception import NotFoundException


class CandidateCountModel(db.Model):
    __tablename__ = 'CandidateWiseResult_CandidateCount'
    candidateWiseResultId = db.Column(db.Integer, db.ForeignKey(CandidateWiseResult.Model.__table__.c.candidateWiseResultId),
                                  primary_key=True)
    candidateId = db.Column(db.Integer, db.ForeignKey(Candidate.Model.__table__.c.candidateId), primary_key=True)
    count = db.Column(db.Integer)
    countInWords = db.Column(db.String(1000), nullable=True)

    candidate = relationship(Candidate.Model, foreign_keys=[candidateId])

    def __init__(self, candidateWiseResultId, candidateId, count, countInWords=None, electionId=None):
        if electionId is not None:
            electionCandidate = ElectionCandidate.get_by_id(candidateId=candidateId, electionId=electionId)
            if electionCandidate is None:
                raise NotFoundException("Candidate is not registered for the given election. (candidateId=%d)" % candidateId)
        else:
            candidate = Candidate.get_by_id(candidateId=candidateId)
            if candidate is None:
                raise NotFoundException("Candidate not found. (candidateId=%d)" % candidateId)

        super(CandidateCountModel, self).__init__(
            candidateWiseResultId=candidateWiseResultId,
            candidateId=candidateId,
            count=count,
            countInWords=countInWords
        )
        db.session.add(self)
        db.session.commit()


Model = CandidateCountModel


def create(candidateWiseResultId, candidateId, count, countInWords=None, electionId=None):
    result = Model(
        candidateWiseResultId=candidateWiseResultId,
        candidateId=candidateId,
        count=count,
        countInWords=countInWords,
        electionId=electionId
    )

    return result
