from sqlalchemy.orm import relationship
from app import db
from orm.entities.SubmissionVersion import TallySheetVersion


class TallySheetVersionRow_CE_201_PV_Model(db.Model):
    __tablename__ = 'tallySheetVersionRow_CE_201_PV'
    tallySheetVersionRowId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tallySheetVersionId = db.Column(db.Integer, db.ForeignKey(TallySheetVersion.Model.__table__.c.tallySheetVersionId))
    ballotBoxId = db.Column(db.String(20), nullable=True, default="")
    numberOfPacketsInserted = db.Column(db.Integer, nullable=True, default=0)
    numberOfAPacketsFound = db.Column(db.Integer, nullable=True, default=0)

    tallySheetVersion = relationship(TallySheetVersion.Model, foreign_keys=[tallySheetVersionId])

    def __init__(self, tallySheetVersionId, ballotBoxId, numberOfPacketsInserted, numberOfAPacketsFound):
        super(TallySheetVersionRow_CE_201_PV_Model, self).__init__(
            tallySheetVersionId=tallySheetVersionId,
            ballotBoxId=ballotBoxId,
            numberOfPacketsInserted=numberOfPacketsInserted,
            numberOfAPacketsFound=numberOfAPacketsFound
        )
        db.session.add(self)
        db.session.flush()


Model = TallySheetVersionRow_CE_201_PV_Model


def create(tallySheetVersionId, ballotBoxId, numberOfPacketsInserted, numberOfAPacketsFound):
    result = Model(
        tallySheetVersionId=tallySheetVersionId,
        ballotBoxId=ballotBoxId,
        numberOfPacketsInserted=numberOfPacketsInserted,
        numberOfAPacketsFound=numberOfAPacketsFound
    )

    return result
