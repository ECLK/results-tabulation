from sqlalchemy.orm import relationship

from app import db

from orm.entities import Candidate
from orm.entities.Election import ElectionCandidate, InvalidVoteCategory
from exception import NotFoundException
from orm.entities.SubmissionVersion import TallySheetVersion


class TallySheetVersionRow_CE_201_PV_Model(db.Model):
    __tablename__ = 'tallySheetVersionRow_CE_201_PV'
    tallySheetVersionRowId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tallySheetVersionId = db.Column(db.Integer, db.ForeignKey(TallySheetVersion.Model.__table__.c.tallySheetVersionId))

    tallySheetVersion = relationship(TallySheetVersion.Model, foreign_keys=[tallySheetVersionId])

    __table_args__ = (
        db.UniqueConstraint('tallySheetVersionId'),
    )

    serialNumber = db.Column(db.Integer, nullable=False)
    numberOfBPacketsInserted = db.Column(db.Integer, nullable=False)
    numberOfAPacketsFound = db.Column(db.Integer, nullable=False)

    def __init__(self, tallySheetVersionId, serialNumber, numberOfBPacketsInserted, numberOfAPacketsFound):
        super(TallySheetVersionRow_CE_201_PV_Model, self).__init__(
            tallySheetVersionId=tallySheetVersionId,
            serialNumber=serialNumber,
            numberOfBPacketsInserted=numberOfBPacketsInserted,
            numberOfAPacketsFound=numberOfAPacketsFound
        )
        db.session.add(self)
        db.session.flush()


Model = TallySheetVersionRow_CE_201_PV_Model


def create(tallySheetVersionId, serialNumber, numberOfBPacketsInserted, numberOfAPacketsFound):
    result = Model(
        tallySheetVersionId=tallySheetVersionId,
        serialNumber=serialNumber,
        numberOfBPacketsInserted=numberOfBPacketsInserted,
        numberOfAPacketsFound=numberOfAPacketsFound
    )

    return result
