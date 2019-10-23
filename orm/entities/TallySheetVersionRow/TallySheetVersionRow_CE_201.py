from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy import and_, select, func

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
    # ballotBoxesIssued = relationship("TallySheetVersionRow_CE_201_IssuedBallotBox_Model")
    # ballotBoxesReceived = relationship("TallySheetVersionRow_CE_201_ReceivedBallotBox_Model")
    ballotsIssued = db.Column(db.Integer, nullable=False)
    ballotsReceived = db.Column(db.Integer, nullable=False)
    ballotsSpoilt = db.Column(db.Integer, nullable=False)
    ballotsUnused = db.Column(db.Integer, nullable=False)
    ordinaryBallotCountFromBoxCount = db.Column(db.Integer, nullable=False)
    tenderedBallotCountFromBoxCount = db.Column(db.Integer, nullable=False)
    ordinaryBallotCountFromBallotPaperAccount = db.Column(db.Integer, nullable=False)
    tenderedBallotCountFromBallotPaperAccount = db.Column(db.Integer, nullable=False)

    area = relationship(Area.Model, foreign_keys=[areaId])
    tallySheetVersion = relationship(TallySheetVersion.Model, foreign_keys=[tallySheetVersionId])

    areaName = association_proxy("area", "areaName")
    electionId = association_proxy("tallySheetVersion", "electionId")

    @hybrid_property
    def ballotBoxesIssued(self):
        ballot_boxes = db.session.query(
            TallySheetVersionRow_CE_201_IssuedBallotBox_Model.ballotBoxId
        ).filter(
            TallySheetVersionRow_CE_201_IssuedBallotBox_Model.tallySheetVersionRowId == self.tallySheetVersionRowId
        ).all()

        return [ballot_box.ballotBoxId for ballot_box in ballot_boxes]

    @hybrid_property
    def ballotBoxesReceived(self):
        ballot_boxes = db.session.query(
            TallySheetVersionRow_CE_201_ReceivedBallotBox_Model.ballotBoxId
        ).filter(
            TallySheetVersionRow_CE_201_ReceivedBallotBox_Model.tallySheetVersionRowId == self.tallySheetVersionRowId
        ).all()

        return [ballot_box.ballotBoxId for ballot_box in ballot_boxes]

    __table_args__ = (
        db.UniqueConstraint('tallySheetVersionId', 'areaId', name='PollingStationPerBallotPaperAccount'),
    )

    def add_received_ballot_box(self, ballotBoxId):
        TallySheetVersionRow_CE_201_ReceivedBallotBox_Model(
            tallySheetVersionRow=self,
            ballotBoxId=ballotBoxId
        )

    def add_issued_ballot_box(self, ballotBoxId):
        TallySheetVersionRow_CE_201_IssuedBallotBox_Model(
            tallySheetVersionRow=self,
            ballotBoxId=ballotBoxId
        )

    def __init__(self, tallySheetVersion, areaId, ballotsIssued, ballotsReceived, ballotsSpoilt, ballotsUnused,
                 ordinaryBallotCountFromBoxCount, tenderedBallotCountFromBoxCount,
                 ordinaryBallotCountFromBallotPaperAccount, tenderedBallotCountFromBallotPaperAccount):

        area = Area.get_by_id(areaId=areaId)

        if area is None:
            raise NotFoundException("Area not found. (areaId=%d)" % areaId)

        if area.electionId not in tallySheetVersion.submission.election.mappedElectionIds:
            raise NotFoundException("Area is not registered for the given election. (areaId=%d)" % areaId)

        super(TallySheetVersionRow_CE_201_Model, self).__init__(
            tallySheetVersionId=tallySheetVersion.tallySheetVersionId,
            areaId=areaId,
            ballotsIssued=ballotsIssued,
            ballotsReceived=ballotsReceived,
            ballotsSpoilt=ballotsSpoilt,
            ballotsUnused=ballotsUnused,
            ordinaryBallotCountFromBoxCount=ordinaryBallotCountFromBoxCount,
            tenderedBallotCountFromBoxCount=tenderedBallotCountFromBoxCount,
            ordinaryBallotCountFromBallotPaperAccount=ordinaryBallotCountFromBallotPaperAccount,
            tenderedBallotCountFromBallotPaperAccount=tenderedBallotCountFromBallotPaperAccount
        )

        db.session.add(self)
        db.session.flush()


Model = TallySheetVersionRow_CE_201_Model


class TallySheetVersionRow_CE_201_BallotBox_Model(db.Model):
    __tablename__ = 'tallySheetVersionRow_CE_201_ballotBox'
    tallySheetVersionRowId = db.Column(db.Integer, db.ForeignKey(
        TallySheetVersionRow_CE_201_Model.__table__.c.tallySheetVersionRowId), primary_key=True)
    ballotBoxId = db.Column(db.String(100), primary_key=True)
    invoiceStage = db.Column(db.Enum(InvoiceStageEnum), primary_key=True)

    __mapper_args__ = {
        'polymorphic_on': invoiceStage
    }

    def __init__(self, tallySheetVersionRow, ballotBoxId):
        # ballotBox = BallotBox.get_by_id(stationaryItemId=ballotBoxStationaryItemId)
        #
        # if ballotBox is None:
        #     raise NotFoundException("Ballot Box not found. (stationaryItemId=%d)" % ballotBoxStationaryItemId)
        #
        # if ballotBox.electionId not in tallySheetVersionRow.tallySheetVersion.submission.election.mappedElectionIds:
        #     raise NotFoundException(
        #         "Ballot Box is not registered for the given election. (stationaryItemId=%d)" % ballotBoxStationaryItemId
        #     )

        super(TallySheetVersionRow_CE_201_BallotBox_Model, self).__init__(
            tallySheetVersionRowId=tallySheetVersionRow.tallySheetVersionRowId,
            ballotBoxId=ballotBoxId
        )
        db.session.add(self)
        db.session.flush()


class TallySheetVersionRow_CE_201_IssuedBallotBox_Model(TallySheetVersionRow_CE_201_BallotBox_Model):
    __mapper_args__ = {
        'polymorphic_identity': InvoiceStageEnum.Issued
    }


class TallySheetVersionRow_CE_201_ReceivedBallotBox_Model(TallySheetVersionRow_CE_201_BallotBox_Model):
    __mapper_args__ = {
        'polymorphic_identity': InvoiceStageEnum.Received
    }


def create(tallySheetVersion, areaId, ballotsIssued, ballotsReceived,
           ballotsSpoilt, ballotsUnused,
           ordinaryBallotCountFromBoxCount, tenderedBallotCountFromBoxCount, ordinaryBallotCountFromBallotPaperAccount,
           tenderedBallotCountFromBallotPaperAccount):
    result = Model(
        tallySheetVersion=tallySheetVersion,
        areaId=areaId,
        ballotsIssued=ballotsIssued,
        ballotsReceived=ballotsReceived,
        ballotsSpoilt=ballotsSpoilt,
        ballotsUnused=ballotsUnused,
        ordinaryBallotCountFromBoxCount=ordinaryBallotCountFromBoxCount,
        tenderedBallotCountFromBoxCount=tenderedBallotCountFromBoxCount,
        ordinaryBallotCountFromBallotPaperAccount=ordinaryBallotCountFromBallotPaperAccount,
        tenderedBallotCountFromBallotPaperAccount=tenderedBallotCountFromBallotPaperAccount
    )

    return result
