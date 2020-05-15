from sqlalchemy.ext.associationproxy import association_proxy

from app import db
from sqlalchemy.orm import relationship
from orm.entities import Candidate, Party


class ElectionCandidateModel(db.Model):
    __tablename__ = 'election_candidate'
    electionCandidateId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    electionId = db.Column(db.Integer, db.ForeignKey("election.electionId"), nullable=False)
    partyId = db.Column(db.Integer, db.ForeignKey(Party.Model.__table__.c.partyId), nullable=False)
    candidateId = db.Column(db.Integer, db.ForeignKey(Candidate.Model.__table__.c.candidateId), nullable=False)
    qualifiedForPreferences = db.Column(db.Boolean, default=False, nullable=False)

    election = relationship("ElectionModel", foreign_keys=[electionId])
    party = relationship(Party.Model, foreign_keys=[partyId])
    candidate = relationship(Candidate.Model, foreign_keys=[candidateId])

    candidateName = association_proxy("candidate", "candidateName")
    candidateNumber = association_proxy("candidate", "candidateNumber")

    __table_args__ = (
        db.UniqueConstraint('electionId', 'candidateId', name='CandidatePerElection'),
    )

    def __init__(self, electionId, candidateId, partyId):
        super(ElectionCandidateModel, self).__init__(
            electionId=electionId,
            candidateId=candidateId,
            partyId=partyId
        )

        db.session.add(self)
        db.session.flush()


Model = ElectionCandidateModel


def get_all(electionId=None, candidateId=None):
    query = Model.query

    if electionId is not None:
        query = query.filter(Model.electionId == electionId)

    if candidateId is not None:
        query = query.filter(Model.candidateId == candidateId)

    return query


def get_by_id(electionId, candidateId):
    result = Model.query.filter(
        Model.electionId == electionId,
        Model.candidateId == candidateId
    ).one_or_none()

    return result


def create(electionId, candidateId, partyId):
    result = Model(
        electionId=electionId,
        candidateId=candidateId,
        partyId=partyId
    )

    return result
