from sqlalchemy.orm import relationship

from app import db

from orm.entities import Candidate
from orm.entities.Election import ElectionCandidate, InvalidVoteCategory
from exception import NotFoundException
from orm.entities.SubmissionVersion import TallySheetVersion


class TallySheetVersionRow_PRE_34_CO_Model(db.Model):
    __tablename__ = 'tallySheetVersionRow_PRE_34_CO'
    tallySheetVersionRowId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tallySheetVersionId = db.Column(db.Integer, db.ForeignKey(TallySheetVersion.Model.__table__.c.tallySheetVersionId))

    candidateId = db.Column(db.Integer, db.ForeignKey(Candidate.Model.__table__.c.candidateId))
    notCountedBallotPapers = db.Column(db.Integer, nullable=False)
    remainingBallotPapers = db.Column(db.Integer, nullable=False)

    tallySheetVersion = relationship(TallySheetVersion.Model, foreign_keys=[tallySheetVersionId])
    candidate = relationship(Candidate.Model, foreign_keys=[candidateId])

    __table_args__ = (
        db.UniqueConstraint('tallySheetVersionId', 'candidateId', name='PRE_34_CO_row'),
    )

    def __init__(self, tallySheetVersionId, candidateId, notCountedBallotPapers, remainingBallotPapers):
        super(TallySheetVersionRow_PRE_34_CO_Model, self).__init__(
            candidateId=candidateId,
            tallySheetVersionId=tallySheetVersionId,
            notCountedBallotPapers=notCountedBallotPapers,
            remainingBallotPapers=remainingBallotPapers
        )
        db.session.add(self)
        db.session.flush()


Model = TallySheetVersionRow_PRE_34_CO_Model


def create(tallySheetVersionId, candidateId, notCountedBallotPapers, remainingBallotPapers):
    result = Model(
        candidateId=candidateId,
        tallySheetVersionId=tallySheetVersionId,
        notCountedBallotPapers=notCountedBallotPapers,
        remainingBallotPapers=remainingBallotPapers
    )

    return result
