from sqlalchemy.orm import relationship

from app import db

from orm.entities import Candidate
from orm.entities.Election import ElectionCandidate, InvalidVoteCategory
from exception import NotFoundException
from orm.entities.SubmissionVersion import TallySheetVersion


class TallySheetVersionRow_PRE_34_CO_PREFERENCES_Model(db.Model):
    __tablename__ = 'tallySheetVersionRow_PRE_34_CO_PREFERENCES'
    preferenceRowId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tallySheetPre34RowId = db.Column(db.Integer, db.ForeignKey('tallySheetVersionRow_PRE_34_CO.tallySheetVersionRowId'))

    candidateId = db.Column(db.Integer, db.ForeignKey(Candidate.Model.__table__.c.candidateId))
    no2ndPreferences = db.Column(db.Integer, nullable=False)
    no3rdPreferences = db.Column(db.Integer, nullable=False)

    #tallySheetVersion = relationship(TallySheetVersion.Model, foreign_keys=[tallySheetVersionId])
    candidate = relationship(Candidate.Model, foreign_keys=[candidateId])

    __table_args__ = (
        db.UniqueConstraint('preferenceRowId', name='PRE_34_CO_PREFERENCES_row'),
    )

    def __init__(self, tallySheetVersionRowId, candidateId, no2ndPreferences, no3rdPreferences):
        super(TallySheetVersionRow_PRE_34_CO_PREFERENCES_Model, self).__init__(
            tallySheetPre34RowId=tallySheetVersionRowId,
            candidateId=candidateId,
            no2ndPreferences=no2ndPreferences,
            no3rdPreferences=no3rdPreferences
        )
        db.session.add(self)
        db.session.flush()


Model = TallySheetVersionRow_PRE_34_CO_PREFERENCES_Model


def create(tallySheetVersionRowId, candidateId, no2ndPreferences, no3rdPreferences):
    result = Model(
        tallySheetVersionRowId=tallySheetVersionRowId,
        candidateId=candidateId,
        no2ndPreferences=no2ndPreferences,
        no3rdPreferences=no3rdPreferences
    )

    return result


rest apis in microservices
patterns 


