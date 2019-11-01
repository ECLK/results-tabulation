from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from app import db
from orm.entities import Area, Election, Candidate
from orm.entities.SubmissionVersion import TallySheetVersion


class TallySheetVersionRow_PRE_34_preference_Model(db.Model):
    __tablename__ = 'tallySheetVersionRow_PRE_34_Preference'
    tallySheetVersionRowId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tallySheetVersionId = db.Column(db.Integer, db.ForeignKey(TallySheetVersion.Model.__table__.c.tallySheetVersionId),
                                    nullable=False)
    electionId = db.Column(db.Integer, db.ForeignKey(Election.Model.__table__.c.electionId), nullable=False)
    candidateId = db.Column(db.Integer, db.ForeignKey(Candidate.Model.__table__.c.candidateId), nullable=True)
    preferenceNumber = db.Column(db.Integer, nullable=False)
    preferenceCount = db.Column(db.Integer, nullable=False)

    candidate = relationship(Candidate.Model, foreign_keys=[candidateId])
    election = relationship(Election.Model, foreign_keys=[electionId])

    areaName = association_proxy("area", "areaName")

    __table_args__ = (
        db.UniqueConstraint('tallySheetVersionId', 'preferenceNumber', 'candidateId',
                            name='TallySheetVersionRow_RejectedVoteCount_Model'),
    )

    def __init__(self, electionId, tallySheetVersionId, preferenceNumber, preferenceCount, candidateId):
        super(TallySheetVersionRow_PRE_34_preference_Model, self).__init__(
            electionId=electionId,
            tallySheetVersionId=tallySheetVersionId,
            preferenceNumber=preferenceNumber,
            preferenceCount=preferenceCount,
            candidateId=candidateId
        )
        db.session.add(self)
        db.session.flush()


Model = TallySheetVersionRow_PRE_34_preference_Model


def create(electionId, tallySheetVersionId, preferenceNumber, preferenceCount, candidateId):
    result = Model(
        electionId=electionId,
        tallySheetVersionId=tallySheetVersionId,
        preferenceNumber=preferenceNumber,
        preferenceCount=preferenceCount,
        candidateId=candidateId
    )

    return result
