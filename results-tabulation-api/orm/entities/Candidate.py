from app import db
from sqlalchemy.orm import relationship

from constants.CANDIDATE_TYPE import CANDIDATE_TYPE_NORMAL
from orm.entities.IO.File import Image


class CandidateModel(db.Model):
    __tablename__ = 'candidate'
    candidateId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    candidateName = db.Column(db.String(100), nullable=False)
    candidateNumber = db.Column(db.String(100), nullable=False, default="")
    candidateType = db.Column(db.String(50), nullable=False, default=CANDIDATE_TYPE_NORMAL)
    candidateProfileImageFileId = db.Column(db.Integer, db.ForeignKey(Image.Model.__table__.c.fileId), nullable=True)

    candidateProfileImageFile = relationship(Image.Model)


Model = CandidateModel


def get_by_id(candidateId):
    result = Model.query.filter(
        Model.candidateId == candidateId
    ).one_or_none()

    return result


def create(candidateName, candidateNumber="", candidateProfileImageFileSource=None,
           candidateType=CANDIDATE_TYPE_NORMAL):
    if candidateProfileImageFileSource is not None:
        candidateProfileImageFile = Image.create(candidateProfileImageFileSource)
        result = Model(
            candidateName=candidateName,
            candidateNumber=candidateNumber,
            candidateType=candidateType,
            candidateProfileImageFileId=candidateProfileImageFile.fileId
        )
    else:
        result = Model(
            candidateName=candidateName,
            candidateNumber=candidateNumber,
            candidateType=candidateType
        )

    db.session.add(result)
    db.session.flush()

    return result
