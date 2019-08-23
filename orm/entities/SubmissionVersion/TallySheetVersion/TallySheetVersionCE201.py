from sqlalchemy.ext.hybrid import hybrid_property

from sqlalchemy import and_
from app import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

from exception import NotFoundException
from orm.entities.Result.BallotPaperAccountResult import BallotPaperAccount
from util import get_paginated_query

from orm.entities import SubmissionVersion, Area
from orm.entities.Submission import TallySheet
from orm.entities.Result import BallotPaperAccountResult
from orm.enums import TallySheetCodeEnum, AreaTypeEnum


class TallySheetVersionCE201Model(db.Model):
    __tablename__ = 'tallySheetVersion_CE_201'
    tallySheetVersionId = db.Column(db.Integer, db.ForeignKey(SubmissionVersion.Model.__table__.c.submissionVersionId),
                                    primary_key=True)
    ballotPaperAccountResultId = db.Column(db.Integer, db.ForeignKey(
        BallotPaperAccountResult.Model.__table__.c.ballotPaperAccountResultId))

    submissionVersion = relationship(SubmissionVersion.Model, foreign_keys=[tallySheetVersionId])

    submission = association_proxy("submissionVersion", "submission")
    tallySheetId = association_proxy("submissionVersion", "submissionId")
    createdBy = association_proxy("submissionVersion", "createdBy")
    createdAt = association_proxy("submissionVersion", "createdAt")

    @hybrid_property
    def tallySheetContent(self):
        pollingStations = self.submission.area.get_associated_areas(AreaTypeEnum.PollingStation)

        result = db.session.query(
            Area.Model.areaId,
            BallotPaperAccount.Model.issuedBallotCount,
            BallotPaperAccount.Model.issuedTenderBallotCount,
            BallotPaperAccount.Model.receivedBallotCount,
            BallotPaperAccount.Model.receivedTenderBallotCount,
        ).join(
            BallotPaperAccount.Model,
            and_(
                BallotPaperAccount.Model.ballotPaperAccountResultId == self.ballotPaperAccountResultId,
                BallotPaperAccount.Model.areaId == Area.Model.areaId
            ),
            isouter=True
        ).filter(
            Area.Model.areaId.in_([pollingStation.areaId for pollingStation in pollingStations])
        ).group_by(
            Area.Model.areaId
        ).all()

        return result


Model = TallySheetVersionCE201Model


def get_all(tallySheetId):
    query = Model.query.filter(Model.tallySheetId == tallySheetId)

    result = get_paginated_query(query).all()

    return result


def get_by_id(tallySheetId, tallySheetVersionId):
    tallySheet = TallySheet.get_by_id(tallySheetId=tallySheetId)
    if tallySheet is None:
        raise NotFoundException("Tally sheet not found. (tallySheetId=%d)" % tallySheetId)
    elif tallySheet.tallySheetCode is not TallySheetCodeEnum.CE_201:
        raise NotFoundException("Requested version not found. (tallySheetId=%d)" % tallySheetId)

    result = Model.query.filter(
        Model.tallySheetVersionId == tallySheetVersionId
    ).one_or_none()

    return result


def create(tallySheetId):
    tallySheet = TallySheet.get_by_id(tallySheetId=tallySheetId)
    if tallySheet is None:
        raise NotFoundException("Tally sheet not found. (tallySheetId=%d)" % tallySheetId)

    submissionVersion = SubmissionVersion.create(submissionId=tallySheetId)
    ballotPaperAccountResult = BallotPaperAccountResult.create()

    result = Model(
        tallySheetVersionId=submissionVersion.submissionVersionId,
        ballotPaperAccountResultId=ballotPaperAccountResult.ballotPaperAccountResultId
    )

    db.session.add(result)
    db.session.commit()

    return result
