from sqlalchemy.orm import relationship

from app import db
from orm.entities import Candidate
from orm.entities.SubmissionVersion import TallySheetVersion


class TallySheetVersionRow_PRE_41_Model(db.Model):
    __tablename__ = 'tallySheetVersionRow_PRE_41'
    tallySheetVersionRowId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tallySheetVersionId = db.Column(db.Integer, db.ForeignKey(TallySheetVersion.Model.__table__.c.tallySheetVersionId),
                                    nullable=False)
    candidateId = db.Column(db.Integer, db.ForeignKey(Candidate.Model.__table__.c.candidateId), nullable=False)
    count = db.Column(db.Integer, nullable=False)
    countInWords = db.Column(db.String(1000), nullable=True)

    candidate = relationship(Candidate.Model, foreign_keys=[candidateId])

    tallySheetVersion = relationship(TallySheetVersion.Model, foreign_keys=[tallySheetVersionId])

    __table_args__ = (
        db.UniqueConstraint('tallySheetVersionId', 'candidateId', name='CandidatePerPRE41'),
    )

    def __init__(self, tallySheetVersionId, candidateId, count, countInWords=None):
        super(TallySheetVersionRow_PRE_41_Model, self).__init__(
            tallySheetVersionId=tallySheetVersionId,
            candidateId=candidateId,
            count=count,
            countInWords=countInWords
        )
        db.session.add(self)
        db.session.commit()


Model = TallySheetVersionRow_PRE_41_Model


def create(tallySheetVersionId, candidateId, count, countInWords=None):
    result = Model(
        tallySheetVersionId=tallySheetVersionId,
        candidateId=candidateId,
        count=count,
        countInWords=countInWords
    )

    return result
