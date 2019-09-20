from sqlalchemy.orm import relationship

from app import db
from orm.entities import Candidate, Election
from orm.entities.Area.Electorate import ElectoralDistrict, PollingDivision
from orm.entities.SubmissionVersion import TallySheetVersion


class TallySheetVersionRow_PRE_30_ED_Model(db.Model):
    __tablename__ = 'tallySheetVersionRow_PRE_30_ED'
    tallySheetVersionRowId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tallySheetVersionId = db.Column(db.Integer, db.ForeignKey(TallySheetVersion.Model.__table__.c.tallySheetVersionId),
                                    nullable=False)
    candidateId = db.Column(db.Integer, db.ForeignKey(Candidate.Model.__table__.c.candidateId), nullable=False)
    electionId = db.Column(db.Integer, db.ForeignKey(Election.Model.__table__.c.electionId), nullable=False)
    pollingDivisionId = db.Column(db.Integer, db.ForeignKey(PollingDivision.Model.__table__.c.areaId), nullable=False)
    count = db.Column(db.Integer, nullable=False)

    candidate = relationship(Candidate.Model, foreign_keys=[candidateId])
    pollingDivision = relationship(PollingDivision.Model, foreign_keys=[pollingDivisionId])
    tallySheetVersion = relationship(TallySheetVersion.Model, foreign_keys=[tallySheetVersionId])

    __table_args__ = (
        db.UniqueConstraint(
            'tallySheetVersionId', 'electionId', 'candidateId', 'pollingDivisionId',
            name='TallySheetVersionRow_PRE_30_ED_Model'
        ),
    )

    def __init__(self, tallySheetVersionId, pollingDivisionId, candidateId, count, electionId):
        super(TallySheetVersionRow_PRE_30_ED_Model, self).__init__(
            tallySheetVersionId=tallySheetVersionId,
            pollingDivisionId=pollingDivisionId,
            candidateId=candidateId,
            count=count,
            electionId=electionId
        )
        db.session.add(self)
        db.session.flush()


Model = TallySheetVersionRow_PRE_30_ED_Model


def create(tallySheetVersionId, pollingDivisionId, candidateId, count, electionId):
    result = Model(
        tallySheetVersionId=tallySheetVersionId,
        pollingDivisionId=pollingDivisionId,
        candidateId=candidateId,
        count=count,
        electionId=electionId
    )

    return result
