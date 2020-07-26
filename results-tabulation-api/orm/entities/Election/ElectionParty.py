from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property

from app import db
from sqlalchemy.orm import relationship
from orm.entities import Party
from orm.entities.Election import ElectionCandidate


class ElectionPartyModel(db.Model):
    __tablename__ = 'election_party'
    electionPartyId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    electionId = db.Column(db.Integer, db.ForeignKey("election.electionId"))
    partyId = db.Column(db.Integer, db.ForeignKey(Party.Model.__table__.c.partyId))

    election = relationship("ElectionModel", foreign_keys=[electionId])
    party = relationship(Party.Model, foreign_keys=[partyId], lazy='subquery')
    candidates = relationship("ElectionCandidateModel", order_by="ElectionCandidateModel.electionCandidateId",
                              lazy='subquery',
                              primaryjoin="and_(ElectionCandidateModel.electionId==ElectionPartyModel.electionId, "
                                          "foreign(ElectionCandidateModel.partyId)==ElectionPartyModel.partyId)")

    partyName = association_proxy("party", "partyName")
    partySymbolFileId = association_proxy("party", "partySymbolFileId")
    partySymbolFile = association_proxy("party", "partySymbolFile")
    partySymbol = association_proxy("party", "partySymbol")
    partyAbbreviation = association_proxy("party", "partyAbbreviation")

    __table_args__ = (
        db.UniqueConstraint('electionId', 'partyId', name='PartyPerElection'),
    )

    def __init__(self, electionId, partyId):
        super(ElectionPartyModel, self).__init__(
            electionId=electionId,
            partyId=partyId
        )

        db.session.add(self)
        db.session.flush()

    def add_candidate(self, candidateId):
        return ElectionCandidate.create(
            electionId=self.electionId,
            partyId=self.partyId,
            candidateId=candidateId
        )


Model = ElectionPartyModel


def get_all(electionId=None, partyId=None):
    query = Model.query

    if electionId is not None:
        query = query.filter(Model.electionId == electionId)

    if partyId is not None:
        query = query.filter(Model.partyId == partyId)

    return query


def get_by_id(electionId, partyId):
    result = Model.query.filter(
        Model.electionId == electionId,
        Model.partyId == partyId
    ).one_or_none()

    return result


def create(electionId, partyId):
    result = Model(
        electionId=electionId,
        partyId=partyId
    )

    return result
