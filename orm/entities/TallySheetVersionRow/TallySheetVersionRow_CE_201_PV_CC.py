from sqlalchemy.orm import relationship

from app import db

from orm.entities.Area.Office import CountingCentre
from orm.entities.SubmissionVersion import TallySheetVersion


class TallySheetVersionRow_CE_201_PV_CC_Model(db.Model):
    __tablename__ = 'tallySheetVersionRow_CE_201_PV_CC'
    tallySheetVersionRowId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tallySheetVersionId = db.Column(db.Integer, db.ForeignKey(TallySheetVersion.Model.__table__.c.tallySheetVersionId))

    countingCentreId = db.Column(db.Integer, db.ForeignKey(CountingCentre.Model.__table__.c.areaId))
    situation = db.Column(db.String(100), nullable=False)
    timeOfCommencementOfCount = db.Column(db.DateTime, nullable=False)
    numberOfAPacketsFound = db.Column(db.Integer, nullable=False)
    numberOfACoversRejected = db.Column(db.Integer, nullable=False)
    numberOfBCoversRejected = db.Column(db.Integer, nullable=False)
    numberOfValidBallotPapers = db.Column(db.Integer, nullable=False)

    tallySheetVersion = relationship(TallySheetVersion.Model, foreign_keys=[tallySheetVersionId])

    __table_args__ = (
        db.UniqueConstraint('tallySheetVersionId', 'countingCentreId', name='CountingCenterPerCE201PVCC'),
    )

    def __init__(self, tallySheetVersionId, countingCentreId, situation, timeOfCommencementOfCount,
                 numberOfAPacketsFound, numberOfACoversRejected, numberOfBCoversRejected, numberOfValidBallotPapers):
        super(TallySheetVersionRow_CE_201_PV_CC_Model, self).__init__(
            tallySheetVersionId=tallySheetVersionId,
            countingCentreId=countingCentreId,
            situation=situation,
            timeOfCommencementOfCount=timeOfCommencementOfCount,
            numberOfAPacketsFound=numberOfAPacketsFound,
            numberOfACoversRejected=numberOfACoversRejected,
            numberOfBCoversRejected=numberOfBCoversRejected,
            numberOfValidBallotPapers=numberOfValidBallotPapers
        )
        db.session.add(self)
        db.session.flush()


Model = TallySheetVersionRow_CE_201_PV_CC_Model


def create(tallySheetVersionId, countingCentreId, situation, timeOfCommencementOfCount, numberOfAPacketsFound,
           numberOfACoversRejected, numberOfBCoversRejected, numberOfValidBallotPapers):
    result = Model(
        tallySheetVersionId=tallySheetVersionId,
        countingCentreId=countingCentreId,
        situation=situation,
        timeOfCommencementOfCount=timeOfCommencementOfCount,
        numberOfAPacketsFound=numberOfAPacketsFound,
        numberOfACoversRejected=numberOfACoversRejected,
        numberOfBCoversRejected=numberOfBCoversRejected,
        numberOfValidBallotPapers=numberOfValidBallotPapers
    )

    return result
