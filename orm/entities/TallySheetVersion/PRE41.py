from app import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.schema import UniqueConstraint

from util import get_paginated_query

from orm.entities import Election, Office, Proof, HistoryVersion, TallySheetVersion
from orm.entities.Result import PartyWiseResult

from orm.enums import TallySheetCodeEnum, ProofTypeEnum


class TallySheetVersionPRE41Model(TallySheetVersion.Model):
    __tablename__ = 'tallySheetVersion_PRE-41'
    partyWiseResultId = db.Column(db.Integer, db.ForeignKey(PartyWiseResult.Model.__table__.c.partyWiseResultId))

    partyWiseResult = relationship(PartyWiseResult.Model, foreign_keys=[partyWiseResultId])

    resultCounts = association_proxy("partyWiseResult", "resultCounts")

    __mapper_args__ = {
        'polymorphic_identity': TallySheetCodeEnum.PRE_41
    }


Model = TallySheetVersionPRE41Model
