from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from app import db
from orm.entities import Area, Election, Candidate, Party
from orm.entities.Election import InvalidVoteCategory


class TallySheetVersionRow_Model(db.Model):
    __tablename__ = 'tallySheetVersionRow'
    tallySheetVersionRowId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    templateRowId = db.Column(db.Integer, db.ForeignKey("templateRow.templateRowId"), nullable=False)
    tallySheetVersionId = db.Column(db.Integer, db.ForeignKey("tallySheetVersion.tallySheetVersionId"),
                                    nullable=False)
    electionId = db.Column(db.Integer, db.ForeignKey(Election.Model.__table__.c.electionId), nullable=False)
    areaId = db.Column(db.Integer, db.ForeignKey(Area.Model.__table__.c.areaId), nullable=True)
    candidateId = db.Column(db.Integer, db.ForeignKey(Candidate.Model.__table__.c.candidateId), nullable=True)
    partyId = db.Column(db.Integer, db.ForeignKey(Party.Model.__table__.c.partyId), nullable=True)
    invalidVoteCategoryId = db.Column(db.Integer,
                                      db.ForeignKey(InvalidVoteCategory.Model.__table__.c.invalidVoteCategoryId),
                                      nullable=True)
    ballotBoxId = db.Column(db.String(100), nullable=True)
    numValue = db.Column(db.FLOAT, nullable=True)
    strValue = db.Column(db.String(100), nullable=True)
    dateValue = db.Column(db.DateTime, nullable=True)

    election = relationship(Election.Model, foreign_keys=[electionId])
    area = relationship(Area.Model, foreign_keys=[areaId])
    candidate = relationship(Candidate.Model, foreign_keys=[candidateId])
    party = relationship(Party.Model, foreign_keys=[partyId])
    invalidVoteCategory = relationship(InvalidVoteCategory.Model, foreign_keys=[invalidVoteCategoryId])

    areaName = association_proxy("area", "areaName")

    def __init__(self, templateRow, electionId, tallySheetVersion, numValue=None, strValue=None,
                 areaId=None, candidateId=None,
                 partyId=None, ballotBoxId=None, invalidVoteCategoryId=None):
        super(TallySheetVersionRow_Model, self).__init__(
            templateRowId=templateRow.templateRowId,
            electionId=electionId,
            tallySheetVersionId=tallySheetVersion.tallySheetVersionId,
            numValue=numValue,
            strValue=strValue,
            areaId=areaId,
            candidateId=candidateId,
            partyId=partyId,
            ballotBoxId=ballotBoxId,
            invalidVoteCategoryId=invalidVoteCategoryId
        )
        db.session.add(self)
        db.session.flush()


Model = TallySheetVersionRow_Model


def create(templateRow, electionId, tallySheetVersion, numValue=None, strValue=None, areaId=None,
           candidateId=None, partyId=None, ballotBoxId=None, invalidVoteCategoryId=None):
    result = Model(
        templateRow=templateRow,
        electionId=electionId,
        tallySheetVersion=tallySheetVersion,
        numValue=numValue,
        strValue=strValue,
        areaId=areaId,
        candidateId=candidateId,
        partyId=partyId,
        ballotBoxId=ballotBoxId,
        invalidVoteCategoryId=invalidVoteCategoryId
    )

    return result
