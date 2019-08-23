from sqlalchemy.orm import relationship

from app import db

from orm.entities import Area
from orm.entities.Result import BallotPaperAccountResult
from exception import NotFoundException


class BallotPaperAccountModel(db.Model):
    __tablename__ = 'ballotPaperAccountResult_ballotPaperAccount'
    ballotPaperAccountResultId = db.Column(db.Integer, db.ForeignKey(
        BallotPaperAccountResult.Model.__table__.c.ballotPaperAccountResultId), primary_key=True)
    areaId = db.Column(db.Integer, db.ForeignKey(Area.Model.__table__.c.areaId), primary_key=True)
    issuedBallotCount = db.Column(db.Integer, nullable=False)
    issuedTenderBallotCount = db.Column(db.Integer, nullable=False)
    receivedBallotCount = db.Column(db.Integer, nullable=False)
    receivedTenderBallotCount = db.Column(db.Integer, nullable=False)

    area = relationship(Area.Model, foreign_keys=[areaId])

    def __init__(self, ballotPaperAccountResultId, areaId, issuedBallotCount, issuedTenderBallotCount,
                 receivedBallotCount, receivedTenderBallotCount, electionId=None):

        area = Area.get_by_id(areaId=areaId)

        if area is None:
            raise NotFoundException("Area not found. (areaId=%d)" % areaId)

        if electionId is not None:
            if area.electionId != electionId:
                raise NotFoundException("Area is not registered for the given election. (areaId=%d)" % areaId)

        super(BallotPaperAccountModel, self).__init__(
            ballotPaperAccountResultId=ballotPaperAccountResultId,
            areaId=areaId,
            issuedBallotCount=issuedBallotCount,
            issuedTenderBallotCount=issuedTenderBallotCount,
            receivedBallotCount=receivedBallotCount,
            receivedTenderBallotCount=receivedTenderBallotCount
        )
        db.session.add(self)
        db.session.commit()


Model = BallotPaperAccountModel


def create(ballotPaperAccountResultId, areaId, issuedBallotCount, issuedTenderBallotCount, receivedBallotCount,
           receivedTenderBallotCount, electionId=None):
    result = Model(
        ballotPaperAccountResultId=ballotPaperAccountResultId,
        areaId=areaId,
        issuedBallotCount=issuedBallotCount,
        issuedTenderBallotCount=issuedTenderBallotCount,
        receivedBallotCount=receivedBallotCount,
        receivedTenderBallotCount=receivedTenderBallotCount,
        electionId=electionId
    )

    return result
