from app import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.schema import UniqueConstraint

from util import get_paginated_query

from orm.entities import Election, Office, Proof, HistoryVersion, TallySheet

from orm.enums import TallySheetCodeEnum, ProofTypeEnum


class TallySheetVersionModel(db.Model):
    __tablename__ = 'tallySheetVersion'
    tallySheetVersionId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tallySheetId = db.Column(db.Integer, db.ForeignKey(TallySheet.Model.__table__.c.tallySheetId))
    tallySheetCode = db.Column(db.Enum(TallySheetCodeEnum), nullable=False)
    historyVersionId = db.Column(db.Integer, db.ForeignKey(HistoryVersion.Model.__table__.c.historyVersionId))

    __table_args__ = (
        UniqueConstraint('tallySheetId', 'historyVersionId', name='tallySheetVersion_unique_key'),
    )

    __mapper_args__ = {
        'polymorphic_on': tallySheetCode
    }


Model = TallySheetVersionModel
