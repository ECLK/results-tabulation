from sqlalchemy.orm import relationship

from app import db
from orm.entities import Candidate
from orm.entities.Area.Office import CountingCentre
from orm.entities.SubmissionVersion import TallySheetVersion


class TallySheetVersionRow_PRE_30_PD_Model(db.Model):
    __tablename__ = 'tallySheetVersionRow_PRE_30_PD'
    tallySheetVersionRowId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tallySheetVersionId = db.Column(db.Integer, db.ForeignKey(TallySheetVersion.Model.__table__.c.tallySheetVersionId),
                                    nullable=False)
    candidateId = db.Column(db.Integer, db.ForeignKey(Candidate.Model.__table__.c.candidateId), nullable=False)
    countingCentreId = db.Column(db.Integer, db.ForeignKey(CountingCentre.Model.__table__.c.areaId), nullable=False)
    count = db.Column(db.Integer, nullable=False)

    candidate = relationship(Candidate.Model, foreign_keys=[candidateId])
    countingCentre = relationship(CountingCentre.Model, foreign_keys=[countingCentreId])
    tallySheetVersion = relationship(TallySheetVersion.Model, foreign_keys=[tallySheetVersionId])

    __table_args__ = (
        db.UniqueConstraint(
            'tallySheetVersionId', 'candidateId', 'countingCentreId', name='CandidateAndCountingCentrePerPRE30PD'
        ),
    )

    def __init__(self, tallySheetVersionId, countingCentreId, candidateId, count):
        super(TallySheetVersionRow_PRE_30_PD_Model, self).__init__(
            tallySheetVersionId=tallySheetVersionId,
            countingCentreId=countingCentreId,
            candidateId=candidateId,
            count=count
        )
        db.session.add(self)
        db.session.flush()



Model = TallySheetVersionRow_PRE_30_PD_Model


def create(tallySheetVersionId, countingCentreId, candidateId, count):
    result = Model(
        tallySheetVersionId=tallySheetVersionId,
        countingCentreId=countingCentreId,
        candidateId=candidateId,
        count=count
    )

    return result
