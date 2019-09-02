from sqlalchemy.orm import relationship

from app import db

from orm.entities import Candidate
from orm.entities.Election import ElectionCandidate, InvalidVoteCategory
from exception import NotFoundException
from orm.entities.SubmissionVersion import TallySheetVersion


class TallySheetVersionRow_PRE_21_Model(db.Model):
    __tablename__ = 'tallySheetVersionRow_PRE_21'
    tallySheetVersionRowId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tallySheetVersionId = db.Column(db.Integer, db.ForeignKey(TallySheetVersion.Model.__table__.c.tallySheetVersionId))
    count = db.Column(db.Integer, nullable=False)
    invalidVoteCategoryId = db.Column(db.Integer,
                                      db.ForeignKey(InvalidVoteCategory.Model.__table__.c.invalidVoteCategoryId),
                                      nullable=False)

    tallySheetVersion = relationship(TallySheetVersion.Model, foreign_keys=[tallySheetVersionId])

    __table_args__ = (
        db.UniqueConstraint('tallySheetVersionId'),
    )

    def __init__(self, tallySheetVersionId, count, invalidVoteCategoryId):
        super(TallySheetVersionRow_PRE_21_Model, self).__init__(
            tallySheetVersionId=tallySheetVersionId,
            count=count,
            invalidVoteCategoryId=invalidVoteCategoryId
        )
        db.session.add(self)
        db.session.flush()


Model = TallySheetVersionRow_PRE_21_Model


def create(tallySheetVersionId, count, invalidVoteCategoryId):
    result = Model(
        tallySheetVersionId=tallySheetVersionId,
        count=count,
        invalidVoteCategoryId=invalidVoteCategoryId
    )

    return result
