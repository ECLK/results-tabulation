from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from app import db
from orm.entities import Election
from orm.entities.SubmissionVersion import TallySheetVersion


class TallySheetVersionRow_PRE_34_summary_Model(db.Model):
    __tablename__ = 'tallySheetVersionRow_PRE_34_summary'
    tallySheetVersionRowId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tallySheetVersionId = db.Column(db.Integer, db.ForeignKey(TallySheetVersion.Model.__table__.c.tallySheetVersionId),
                                    nullable=False)
    electionId = db.Column(db.Integer, db.ForeignKey(Election.Model.__table__.c.electionId), nullable=False)
    ballotPapersNotCounted = db.Column(db.Integer, nullable=False)
    remainingBallotPapers = db.Column(db.Integer, nullable=False)

    election = relationship(Election.Model, foreign_keys=[electionId])

    __table_args__ = (
        db.UniqueConstraint('tallySheetVersionId', 'electionId',
                            name='TallySheetVersion_PRE_34_summary_Model'),
    )

    def __init__(self, electionId, tallySheetVersionId, ballotPapersNotCounted, remainingBallotPapers):
        super(TallySheetVersionRow_PRE_34_summary_Model, self).__init__(
            electionId=electionId,
            tallySheetVersionId=tallySheetVersionId,
            ballotPapersNotCounted=ballotPapersNotCounted,
            remainingBallotPapers=remainingBallotPapers
        )
        db.session.add(self)
        db.session.flush()


Model = TallySheetVersionRow_PRE_34_summary_Model


def create(electionId, tallySheetVersionId, ballotPapersNotCounted, remainingBallotPapers):
    result = Model(
        electionId=electionId,
        tallySheetVersionId=tallySheetVersionId,
        ballotPapersNotCounted=ballotPapersNotCounted,
        remainingBallotPapers=remainingBallotPapers
    )

    return result
