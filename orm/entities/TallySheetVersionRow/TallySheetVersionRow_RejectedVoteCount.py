from sqlalchemy.orm import relationship

from app import db
from orm.entities import Area, Election, Candidate
from orm.entities.SubmissionVersion import TallySheetVersion


class TallySheetVersionRow_RejectedVoteCount_Model(db.Model):
    __tablename__ = 'tallySheetVersionRow_RejectedVoteCount'
    tallySheetVersionRowId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tallySheetVersionId = db.Column(db.Integer, db.ForeignKey(TallySheetVersion.Model.__table__.c.tallySheetVersionId),
                                    nullable=False)
    electionId = db.Column(db.Integer, db.ForeignKey(Election.Model.__table__.c.electionId), nullable=False)
    areaId = db.Column(db.Integer, db.ForeignKey(Area.Model.__table__.c.areaId), nullable=True)
    candidateId = db.Column(db.Integer, db.ForeignKey(Candidate.Model.__table__.c.candidateId), nullable=True)
    rejectedVoteCount = db.Column(db.Integer, nullable=False)

    candidate = relationship(Candidate.Model, foreign_keys=[candidateId])
    area = relationship(Area.Model, foreign_keys=[areaId])
    election = relationship(Election.Model, foreign_keys=[electionId])

    __table_args__ = (
        db.UniqueConstraint('tallySheetVersionId', 'areaId', 'candidateId',
                            name='TallySheetVersionRow_RejectedVoteCount_Model'),
    )

    def __init__(self, electionId, tallySheetVersionId, rejectedVoteCount, areaId=None, candidateId=None):
        super(TallySheetVersionRow_RejectedVoteCount_Model, self).__init__(
            electionId=electionId,
            tallySheetVersionId=tallySheetVersionId,
            rejectedVoteCount=rejectedVoteCount,
            areaId=areaId,
            candidateId=candidateId
        )
        db.session.add(self)
        db.session.flush()


Model = TallySheetVersionRow_RejectedVoteCount_Model


def createCandidateAndAreaWiseCount(electionId, tallySheetVersionId, candidateId, areaId, rejectedVoteCount):
    # TODO validate candidateId and areaId

    result = Model(
        electionId=electionId,
        tallySheetVersionId=tallySheetVersionId,
        rejectedVoteCount=rejectedVoteCount,
        candidateId=candidateId,
        areaId=areaId
    )

    return result


def createCandidateWiseCount(electionId, tallySheetVersionId, candidateId, rejectedVoteCount):
    # TODO validate candidateId

    result = Model(
        electionId=electionId,
        tallySheetVersionId=tallySheetVersionId,
        rejectedVoteCount=rejectedVoteCount,
        candidateId=candidateId
    )

    return result


def createAreaWiseCount(electionId, tallySheetVersionId, areaId, rejectedVoteCount):
    # TODO validate areaId

    result = Model(
        electionId=electionId,
        tallySheetVersionId=tallySheetVersionId,
        rejectedVoteCount=rejectedVoteCount,
        areaId=areaId
    )

    return result


def create(electionId, tallySheetVersionId, rejectedVoteCount):
    result = Model(
        electionId=electionId,
        tallySheetVersionId=tallySheetVersionId,
        rejectedVoteCount=rejectedVoteCount
    )

    return result
