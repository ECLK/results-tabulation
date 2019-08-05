from app import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.schema import UniqueConstraint

from util import get_paginated_query

from orm.entities import Election, Office, Proof, History, HistoryVersion

from orm.enums import TallySheetCodeEnum, ProofTypeEnum


class TallySheetModel(db.Model):
    __tablename__ = 'tallySheet'
    tallySheetId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tallySheetCode = db.Column(db.Enum(TallySheetCodeEnum), nullable=False)
    electionId = db.Column(db.Integer, db.ForeignKey(Election.Model.__table__.c.electionId), nullable=False)
    officeId = db.Column(db.Integer, db.ForeignKey(Office.Model.__table__.c.officeId), nullable=False)
    latestHistoryVersionId = db.Column(db.Integer, db.ForeignKey(HistoryVersion.Model.__table__.c.historyVersionId),
                                nullable=True)
    tallySheetProofId = db.Column(db.Integer, db.ForeignKey(Proof.Model.__table__.c.proofId), nullable=False)
    tallySheetHistoryId = db.Column(db.Integer, db.ForeignKey(History.Model.__table__.c.historyId), nullable=False)

    election = relationship(Election.Model, foreign_keys=[electionId])
    office = relationship(Office.Model, foreign_keys=[officeId])
    tallySheetProof = relationship(Proof.Model, foreign_keys=[tallySheetProofId])
    tallySheetHistory = relationship(History.Model, foreign_keys=[tallySheetHistoryId])
    latestHistoryVersion = relationship(HistoryVersion.Model, foreign_keys=[latestHistoryVersionId], post_update=True)

    historyVersions = association_proxy("tallySheetHistory", "versions")

    __table_args__ = (
        UniqueConstraint('tallySheetCode', 'electionId', 'officeId', name='_tallysheet_unique_key'),
    )


Model = TallySheetModel


def get_all(electionId=None, officeId=None):
    query = Model.query

    if electionId is not None:
        query = query.filter(Model.electionId == electionId)

    if officeId is not None:
        query = query.filter(Model.officeId == officeId)

    result = get_paginated_query(query).all()

    return result


def create(tallySheetCode, electionId, officeId):
    tallySheetProof = Proof.create(proofType=ProofTypeEnum.ManuallyFilledTallySheets)
    tallySheetHistory = History.create()

    result = Model(
        electionId=electionId,
        tallySheetCode=tallySheetCode,
        officeId=officeId,
        tallySheetProofId=tallySheetProof.proofId,
        tallySheetHistoryId=tallySheetHistory.historyId
    )

    db.session.add(result)
    db.session.commit()

    return result
