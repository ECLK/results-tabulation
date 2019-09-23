from sqlalchemy.orm import relationship

from app import db

from orm.entities import Candidate, BallotBox
from orm.entities.Election import ElectionCandidate, InvalidVoteCategory
from exception import NotFoundException
from orm.entities.SubmissionVersion import TallySheetVersion


class TallySheetVersionRow_CE_201_PV_Model(db.Model):
    __tablename__ = 'tallySheetVersionRow_CE_201_PV'
    tallySheetVersionRowId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tallySheetVersionId = db.Column(db.Integer, db.ForeignKey(TallySheetVersion.Model.__table__.c.tallySheetVersionId))
    ballotBoxStationaryItemId = db.Column(db.Integer, nullable=False)
    numberOfPacketsInserted = db.Column(db.Integer, nullable=False)
    numberOfAPacketsFound = db.Column(db.Integer, nullable=False)

    tallySheetVersion = relationship(TallySheetVersion.Model, foreign_keys=[tallySheetVersionId])

    __table_args__ = (
        db.UniqueConstraint('tallySheetVersionId', 'ballotBoxStationaryItemId', name='BallotBoxPerCE201PV'),
    )

    def __init__(self, tallySheetVersionId, ballotBoxStationaryItemId, numberOfPacketsInserted, numberOfAPacketsFound):
        ballotBox = BallotBox.get_by_id(stationaryItemId=ballotBoxStationaryItemId)

        if ballotBox is not None:
            super(TallySheetVersionRow_CE_201_PV_Model, self).__init__(
                tallySheetVersionId=tallySheetVersionId,
                ballotBoxStationaryItemId=ballotBoxStationaryItemId,
                numberOfPacketsInserted=numberOfPacketsInserted,
                numberOfAPacketsFound=numberOfAPacketsFound
            )
            db.session.add(self)
            db.session.flush()
        else:
            raise NotFoundException("Ballot Box not found (ballotBoxStationaryItemId=%s)" % ballotBoxStationaryItemId)


Model = TallySheetVersionRow_CE_201_PV_Model


def create(tallySheetVersionId, ballotBoxStationaryItemId, numberOfPacketsInserted, numberOfAPacketsFound):
    result = Model(
        tallySheetVersionId=tallySheetVersionId,
        ballotBoxStationaryItemId=ballotBoxStationaryItemId,
        numberOfPacketsInserted=numberOfPacketsInserted,
        numberOfAPacketsFound=numberOfAPacketsFound
    )

    return result
