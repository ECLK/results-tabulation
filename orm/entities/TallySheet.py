from app import db
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint

from util import get_paginated_query

from orm.entities import Election, Office, Proof

from orm.enums import TallySheetCodeEnum, ProofTypeEnum


class TallySheetModel(db.Model):
    __tablename__ = 'tallySheet'
    tallySheetId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.Enum(TallySheetCodeEnum), nullable=False)
    electionId = db.Column(db.Integer, db.ForeignKey(Election.Model.__table__.c.electionId), nullable=False)
    officeId = db.Column(db.Integer, db.ForeignKey(Office.Model.__table__.c.officeId), nullable=False)
    latestVersionId = db.Column(db.Integer, db.ForeignKey("tallySheet_version.tallySheetVersionId"), nullable=True,
                                post_update=True)
    tallySheetProofId = db.Column(db.Integer, db.ForeignKey(Proof.Model.__table__.c.proofId), nullable=False)

    election = relationship(Election.Model, foreign_keys=[electionId])
    office = relationship(Office.Model, foreign_keys=[officeId])
    tallySheetProof = relationship(Proof.Model, foreign_keys=[tallySheetProofId])
    latestVersion = relationship("TallySheetVersionModel", foreign_keys=[latestVersionId], post_update=True)

    __table_args__ = (
        UniqueConstraint('code', 'electionId', 'officeId', name='_tallysheet_unique_key'),
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


def create(code, electionId, officeId):
    tallySheetProof = Proof.create(proofType=ProofTypeEnum.ManuallyFilledTallySheets)

    result = Model(
        electionId=electionId,
        code=code,
        officeId=officeId,
        tallySheetProofId=tallySheetProof.proofId
    )

    db.session.add(result)
    db.session.commit()

    return result
