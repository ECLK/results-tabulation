from app import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.schema import UniqueConstraint

from exception import NotFoundException
from util import get_paginated_query

from orm.entities import HistoryVersion, TallySheetVersion, TallySheet, SubmissionVersion
from orm.entities.Result import PartyWiseResult
from orm.enums import TallySheetCodeEnum


class TallySheetVersionPRE41Model(db.Model):
    __tablename__ = 'tallySheetVersion_PRE41'
    tallySheetVersionId = db.Column(db.Integer, db.ForeignKey(SubmissionVersion.Model.__table__.c.submissionVersionId),
                                    primary_key=True)
    partyWiseResultId = db.Column(db.Integer, db.ForeignKey(PartyWiseResult.Model.__table__.c.partyWiseResultId))

    partyWiseResult = relationship(PartyWiseResult.Model, foreign_keys=[partyWiseResultId])
    submissionVersion = relationship(SubmissionVersion.Model, foreign_keys=[tallySheetVersionId])

    tallySheetId = association_proxy("submissionVersion", "submissionId")
    createdBy = association_proxy("submissionVersion", "createdBy")
    createdAt = association_proxy("submissionVersion", "createdAt")
    tallySheetContent = association_proxy("partyWiseResult", "resultCounts")


Model = TallySheetVersionPRE41Model


def get_all(tallySheetId):
    query = Model.query.filter(Model.tallySheetId == tallySheetId)

    result = get_paginated_query(query).all()

    return result


def get_by_id(tallySheetId, tallySheetVersionId):
    tallySheet = TallySheet.get_by_id(tallySheetId=tallySheetId)
    if tallySheet is None:
        raise NotFoundException("Tally sheet not found. (tallySheetId=%d)" % tallySheetId)
    elif tallySheet.tallySheetCode is not TallySheetCodeEnum.PRE_41:
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
    partyWiseResult = PartyWiseResult.create()

    result = Model(
        tallySheetVersionId=submissionVersion.submissionVersionId,
        partyWiseResultId=partyWiseResult.partyWiseResultId
    )
    db.session.add(result)
    db.session.commit()

    return result
