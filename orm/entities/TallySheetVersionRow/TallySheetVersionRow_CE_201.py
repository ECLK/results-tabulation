from sqlalchemy.orm import relationship

from app import db

from orm.entities import Area
from exception import NotFoundException
from orm.entities.SubmissionVersion import TallySheetVersion


class TallySheetVersionRow_CE_201_Model(db.Model):
    __tablename__ = 'tallySheetVersionRow_CE_201'
    tallySheetVersionRowId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tallySheetVersionId = db.Column(db.Integer, db.ForeignKey(TallySheetVersion.Model.__table__.c.tallySheetVersionId))
    areaId = db.Column(db.Integer, db.ForeignKey(Area.Model.__table__.c.areaId))
    issuedBallotCount = db.Column(db.Integer, nullable=False)
    issuedTenderBallotCount = db.Column(db.Integer, nullable=False)
    receivedBallotCount = db.Column(db.Integer, nullable=False)
    receivedTenderBallotCount = db.Column(db.Integer, nullable=False)

    area = relationship(Area.Model, foreign_keys=[areaId])

    tallySheetVersion = relationship(TallySheetVersion.Model, foreign_keys=[tallySheetVersionId])

    __table_args__ = (
        db.UniqueConstraint('tallySheetVersionId', 'areaId', name='PollingStationPerBallotPaperAccount'),
    )

    def __init__(self, tallySheetVersionId, areaId, issuedBallotCount, issuedTenderBallotCount, receivedBallotCount,
                 receivedTenderBallotCount):

        area = Area.get_by_id(areaId=areaId)

        if area is None:
            raise NotFoundException("Area not found. (areaId=%d)" % areaId)

        if area.electionId != self.tallySheetVersion.electionId:
            raise NotFoundException("Area is not registered for the given election. (areaId=%d)" % areaId)

        super(TallySheetVersionRow_CE_201_Model, self).__init__(
            tallySheetVersionId=tallySheetVersionId,
            areaId=areaId,
            issuedBallotCount=issuedBallotCount,
            issuedTenderBallotCount=issuedTenderBallotCount,
            receivedBallotCount=receivedBallotCount,
            receivedTenderBallotCount=receivedTenderBallotCount
        )
        db.session.add(self)
        db.session.commit()


Model = TallySheetVersionRow_CE_201_Model


def create(tallySheetVersionId, areaId, issuedBallotCount, issuedTenderBallotCount, receivedBallotCount,
           receivedTenderBallotCount):
    result = Model(
        tallySheetVersionId=tallySheetVersionId,
        areaId=areaId,
        issuedBallotCount=issuedBallotCount,
        issuedTenderBallotCount=issuedTenderBallotCount,
        receivedBallotCount=receivedBallotCount,
        receivedTenderBallotCount=receivedTenderBallotCount
    )

    return result
