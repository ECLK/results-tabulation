from sqlalchemy.orm import relationship

from app import db
from orm.entities import Candidate
from orm.entities.Area.Electorate import ElectoralDistrict
from orm.entities.SubmissionVersion import TallySheetVersion


class TallySheetVersionRow_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS_Model(db.Model):
    __tablename__ = 'tallySheetVersionRow_ALL_ISLAND_RESULTS_BY_ED'
    tallySheetVersionRowId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tallySheetVersionId = db.Column(db.Integer, db.ForeignKey(TallySheetVersion.Model.__table__.c.tallySheetVersionId),
                                    nullable=False)
    electoralDistrictId = db.Column(db.Integer, db.ForeignKey(ElectoralDistrict.Model.__table__.c.areaId),
                                    nullable=False)
    candidateId = db.Column(db.Integer, db.ForeignKey(Candidate.Model.__table__.c.candidateId), nullable=False)
    count = db.Column(db.Integer, nullable=False)

    candidate = relationship(Candidate.Model, foreign_keys=[candidateId])

    tallySheetVersion = relationship(TallySheetVersion.Model, foreign_keys=[tallySheetVersionId])

    __table_args__ = (
        db.UniqueConstraint('tallySheetVersionId', 'candidateId', 'electoralDistrictId',
                            name='tallySheetVersionRow_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS'),
    )

    def __init__(self, tallySheetVersionId, candidateId, electoralDistrictId, count):
        super(TallySheetVersionRow_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS_Model, self).__init__(
            tallySheetVersionId=tallySheetVersionId,
            candidateId=candidateId,
            electoralDistrictId=electoralDistrictId,
            count=count
        )
        db.session.add(self)
        db.session.flush()


Model = TallySheetVersionRow_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS_Model


def create(tallySheetVersionId, candidateId, electoralDistrictId, count):
    result = Model(
        tallySheetVersionId=tallySheetVersionId,
        candidateId=candidateId,
        electoralDistrictId=electoralDistrictId,
        count=count
    )

    return result
