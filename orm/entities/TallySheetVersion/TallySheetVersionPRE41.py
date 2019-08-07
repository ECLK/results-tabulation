from app import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.schema import UniqueConstraint

from exception import NotFoundException
from util import get_paginated_query

from orm.entities import HistoryVersion, TallySheetVersion, TallySheet
from orm.entities.Result import PartyWiseResult
from orm.enums import TallySheetCodeEnum


class TallySheetVersionPRE41Model(db.Model):
    __tablename__ = 'tallySheetVersion_PRE41'
    tallySheetVersionId = db.Column(db.Integer, db.ForeignKey("tallySheetVersion.tallySheetVersionId"),
                                    primary_key=True)
    partyWiseResultId = db.Column(db.Integer, db.ForeignKey(PartyWiseResult.Model.__table__.c.partyWiseResultId))

    partyWiseResult = relationship(PartyWiseResult.Model, foreign_keys=[partyWiseResultId])
    tallySheetVersion = relationship("TallySheetVersionModel", foreign_keys=[tallySheetVersionId])

    tallySheetId = association_proxy("tallySheetVersion", "tallySheetId")
    tallySheet = association_proxy("tallySheetVersion", "tallySheet")
    historyVersion = association_proxy("tallySheetVersion", "historyVersion")
    tallySheetCode = association_proxy("tallySheetVersion", "tallySheetCode")
    createdBy = association_proxy("tallySheetVersion", "createdBy")
    createdAt = association_proxy("tallySheetVersion", "createdAt")
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
    tallySheetVersion = TallySheetVersion.create(tallySheetId=tallySheetId)
    partyWiseResult = PartyWiseResult.create()

    result = Model(
        tallySheetVersionId=tallySheetVersion.tallySheetVersionId,
        partyWiseResultId=partyWiseResult.partyWiseResultId
    )
    db.session.add(result)
    db.session.commit()

    return result
