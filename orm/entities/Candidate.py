from app import db
from sqlalchemy.orm import relationship
from orm.entities import Image


class CandidateModel(db.Model):
    __tablename__ = 'candidate'
    candidateId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    candidateName = db.Column(db.String(100), nullable=False)
    candidateProfileImageFileId = db.Column(db.Integer, db.ForeignKey(Image.Model.__table__.c.fileId), nullable=True)

    candidateProfileImageFile = relationship(Image.Model)


Model = CandidateModel


def get_by_id(candidateId):
    result = Model.query.filter(
        Model.candidateId == candidateId
    ).one_or_none()

    return result


def create(candidateName, candidateProfileImageFileSource=None):
    if candidateProfileImageFileSource is not None:
        candidateProfileImageFile = Image.create(candidateProfileImageFileSource)
        result = Model(
            candidateName=candidateName,
            candidateProfileImageFileId=candidateProfileImageFile.fileId
        )
    else:
        result = Model(
            candidateName=candidateName
        )

    db.session.add(result)
    db.session.commit()

    return result
