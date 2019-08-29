from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy import and_

from app import db

from orm.entities import Area, BallotBox
from exception import NotFoundException
from orm.entities.SubmissionVersion import TallySheetVersion
from orm.enums import InvoiceStageEnum


class TallySheetVersionRow_CE_201_Model(db.Model):
    __tablename__ = 'tallySheetVersionRow_CE_201'
    tallySheetVersionRowId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tallySheetVersionId = db.Column(db.Integer, db.ForeignKey(TallySheetVersion.Model.__table__.c.tallySheetVersionId),
                                    nullable=False)
    areaId = db.Column(db.Integer, db.ForeignKey(Area.Model.__table__.c.areaId), nullable=False)
    ballotsIssued = db.Column(db.Integer, nullable=False)
    ballotsReceived = db.Column(db.Integer, nullable=False)
    ballotsSpoilt = db.Column(db.Integer, nullable=False)
    ballotsUnused = db.Column(db.Integer, nullable=False)
    boxCountOrdinary = db.Column(db.Integer, nullable=False)
    boxCountTendered = db.Column(db.Integer, nullable=False)
    ballotPaperAccountOrdinary = db.Column(db.Integer, nullable=False)
    ballotPaperAccountTendered = db.Column(db.Integer, nullable=False)

    area = relationship(Area.Model, foreign_keys=[areaId])
    tallySheetVersion = relationship(TallySheetVersion.Model, foreign_keys=[tallySheetVersionId])

    @hybrid_property
    def issuedBallots(self):
        return db.session.query(
            BallotBox.Model.stationaryItemId,
            BallotBox.Model.ballotBoxId
        ).join(
            TallySheetVersionRow_CE_201_IssuedBallotBox_Model,
            and_(
                TallySheetVersionRow_CE_201_IssuedBallotBox_Model.tallySheetVersionRowId == self.tallySheetVersionRowId,
                TallySheetVersionRow_CE_201_IssuedBallotBox_Model.ballotBoxStationaryItemId == BallotBox.Model.stationaryItemId
            )
        ).all()

    @hybrid_property
    def receivedBallots(self):
        return db.session.query(
            BallotBox.Model.stationaryItemId,
            BallotBox.Model.ballotBoxId
        ).join(
            TallySheetVersionRow_CE_201_ReceivedBallotBox_Model,
            and_(
                TallySheetVersionRow_CE_201_ReceivedBallotBox_Model.tallySheetVersionRowId == self.tallySheetVersionRowId,
                TallySheetVersionRow_CE_201_ReceivedBallotBox_Model.ballotBoxStationaryItemId == BallotBox.Model.stationaryItemId
            )
        ).all()

    __table_args__ = (
        db.UniqueConstraint('tallySheetVersionId', 'areaId', name='PollingStationPerBallotPaperAccount'),
    )

    def add_received_ballot_box(self, stationaryItemId):
        TallySheetVersionRow_CE_201_ReceivedBallotBox_Model(
            tallySheetVersionRow=self,
            ballotBoxStationaryItemId=stationaryItemId
        )

    def add_issued_ballot_box(self, stationaryItemId):
        TallySheetVersionRow_CE_201_IssuedBallotBox_Model(
            tallySheetVersionRow=self,
            ballotBoxStationaryItemId=stationaryItemId
        )

    def __init__(self, tallySheetVersion, areaId, ballotsIssued, ballotsReceived, ballotsSpoilt, ballotsUnused,
                 boxCountOrdinary, boxCountTendered, ballotPaperAccountOrdinary, ballotPaperAccountTendered):

        area = Area.get_by_id(areaId=areaId)

        if area is None:
            raise NotFoundException("Area not found. (areaId=%d)" % areaId)

        if area.electionId != tallySheetVersion.submission.electionId:
            raise NotFoundException("Area is not registered for the given election. (areaId=%d)" % areaId)

        super(TallySheetVersionRow_CE_201_Model, self).__init__(
            tallySheetVersionId=tallySheetVersion.tallySheetVersionId,
            areaId=areaId,
            ballotsIssued=ballotsIssued,
            ballotsReceived=ballotsReceived,
            ballotsSpoilt=ballotsSpoilt,
            ballotsUnused=ballotsUnused,
            boxCountOrdinary=boxCountOrdinary,
            boxCountTendered=boxCountTendered,
            ballotPaperAccountOrdinary=ballotPaperAccountOrdinary,
            ballotPaperAccountTendered=ballotPaperAccountTendered
        )

        db.session.add(self)
        db.session.commit()


Model = TallySheetVersionRow_CE_201_Model


class TallySheetVersionRow_CE_201_BallotBox_Model(db.Model):
    __tablename__ = 'tallySheetVersionRow_CE_201_ballotBox'
    tallySheetVersionRowId = db.Column(db.Integer, db.ForeignKey(
        TallySheetVersionRow_CE_201_Model.__table__.c.tallySheetVersionRowId), primary_key=True)
    ballotBoxStationaryItemId = db.Column(db.Integer, db.ForeignKey(BallotBox.Model.__table__.c.stationaryItemId),
                                          primary_key=True)
    invoiceStage = db.Column(db.Enum(InvoiceStageEnum), nullable=False)

    __mapper_args__ = {
        'polymorphic_on': invoiceStage
    }

    def __init__(self, tallySheetVersionRow, ballotBoxStationaryItemId):
        ballotBox = BallotBox.get_by_id(stationaryItemId=ballotBoxStationaryItemId)

        if ballotBox is None:
            raise NotFoundException("Ballot Box not found. (stationaryItemId=%d)" % ballotBoxStationaryItemId)

        if ballotBox.electionId != tallySheetVersionRow.tallySheetVersion.submission.electionId:
            raise NotFoundException(
                "Ballot Box is not registered for the given election. (stationaryItemId=%d)" % ballotBoxStationaryItemId
            )

        super(TallySheetVersionRow_CE_201_BallotBox_Model, self).__init__(
            tallySheetVersionRowId=tallySheetVersionRow.tallySheetVersionRowId,
            ballotBoxStationaryItemId=ballotBoxStationaryItemId
        )
        db.session.add(self)
        db.session.commit()


class TallySheetVersionRow_CE_201_IssuedBallotBox_Model(TallySheetVersionRow_CE_201_BallotBox_Model):
    __mapper_args__ = {
        'polymorphic_identity': InvoiceStageEnum.Issued
    }


class TallySheetVersionRow_CE_201_ReceivedBallotBox_Model(TallySheetVersionRow_CE_201_BallotBox_Model):
    __mapper_args__ = {
        'polymorphic_identity': InvoiceStageEnum.Received
    }


def create(tallySheetVersion, areaId, ballotsIssued, ballotsReceived, ballotsSpoilt, ballotsUnused,
           boxCountOrdinary, boxCountTendered, ballotPaperAccountOrdinary, ballotPaperAccountTendered):
    result = Model(
        tallySheetVersion=tallySheetVersion,
        areaId=areaId,
        ballotsIssued=ballotsIssued,
        ballotsReceived=ballotsReceived,
        ballotsSpoilt=ballotsSpoilt,
        ballotsUnused=ballotsUnused,
        boxCountOrdinary=boxCountOrdinary,
        boxCountTendered=boxCountTendered,
        ballotPaperAccountOrdinary=ballotPaperAccountOrdinary,
        ballotPaperAccountTendered=ballotPaperAccountTendered
    )

    return result
