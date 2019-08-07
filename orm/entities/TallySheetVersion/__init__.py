from app import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.schema import UniqueConstraint

from util import get_paginated_query

from orm.entities import HistoryVersion, TallySheet

from orm.enums import TallySheetCodeEnum, ProofTypeEnum

from orm.entities.TallySheetVersion import TallySheetVersionPRE41
from exception import NotFoundException


class TallySheetVersionModel(db.Model):
    __tablename__ = 'tallySheetVersion'
    tallySheetVersionId = db.Column(db.Integer, db.ForeignKey(HistoryVersion.Model.__table__.c.historyVersionId),
                                    primary_key=True)
    tallySheetId = db.Column(db.Integer, db.ForeignKey(TallySheet.Model.__table__.c.tallySheetId))

    tallySheet = relationship(TallySheet.Model, foreign_keys=[tallySheetId])
    historyVersion = relationship(HistoryVersion.Model, foreign_keys=[tallySheetVersionId])

    tallySheetCode = association_proxy("tallySheet", "tallySheetCode")
    createdBy = association_proxy("historyVersion", "createdBy")
    createdAt = association_proxy("historyVersion", "createdAt")

    @hybrid_property
    def tallySheetContent(self):
        if self.tallySheetCode == TallySheetCodeEnum.PRE_41:
            pre41 = TallySheetVersionPRE41.get_by_id(tallySheetVersionId=self.tallySheetVersionId)
            if pre41 is not None:
                return pre41.partyWiseResult.resultCounts

        return None


Model = TallySheetVersionModel


def get_all(tallySheetId, tallySheetCode=None):
    query = Model.query.filter(Model.tallySheetId == tallySheetId)

    if tallySheetCode is not None:
        query = query.filter(Model.tallySheetCode == tallySheetCode)

    result = get_paginated_query(query).all()

    return result


def create(tallySheetId):
    tallySheet = TallySheet.get_by_id(tallySheetId=tallySheetId)
    if tallySheet is None:
        raise NotFoundException("Tally sheet not found. (tallySheetId=%d)" % tallySheetId)

    historyVersion = HistoryVersion.create(tallySheet.tallySheetHistoryId)

    result = Model(
        tallySheetId=tallySheetId,
        tallySheetVersionId=historyVersion.historyVersionId,
    )
    db.session.add(result)
    db.session.commit()

    return result
