from sqlalchemy.orm import relationship

from app import db
from orm.entities import Candidate
from orm.entities.SubmissionVersion import TallySheetVersion


class TallySheetVersionRow_ALL_ISLAND_RESULT_Model(db.Model):
    __tablename__ = 'tallySheetVersionRow_ALL_ISLAND_RESULT'
    tallySheetVersionRowId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tallySheetVersionId = db.Column(db.Integer, db.ForeignKey(TallySheetVersion.Model.__table__.c.tallySheetVersionId),
                                    nullable=False)
    candidateId = db.Column(db.Integer, db.ForeignKey(Candidate.Model.__table__.c.candidateId), nullable=False)
    count = db.Column(db.Integer, nullable=False)

    candidate = relationship(Candidate.Model, foreign_keys=[candidateId])

    tallySheetVersion = relationship(TallySheetVersion.Model, foreign_keys=[tallySheetVersionId])

    __table_args__ = (
        db.UniqueConstraint('tallySheetVersionId', 'candidateId', name='CandidatePerALL_ISLAND_RESULT'),
    )

    def __init__(self, tallySheetVersionId, candidateId, count):
        super(TallySheetVersionRow_ALL_ISLAND_RESULT_Model, self).__init__(
            tallySheetVersionId=tallySheetVersionId,
            candidateId=candidateId,
            count=count
        )
        db.session.add(self)
        db.session.flush()


Model = TallySheetVersionRow_ALL_ISLAND_RESULT_Model


def create(tallySheetVersionId, candidateId, count):
    result = Model(
        tallySheetVersionId=tallySheetVersionId,
        candidateId=candidateId,
        count=count
    )

    return result
