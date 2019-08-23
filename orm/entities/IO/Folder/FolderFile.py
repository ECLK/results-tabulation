from app import db
from sqlalchemy.orm import relationship
from orm.entities.IO import File, Folder


class FolderFileModel(db.Model):
    __tablename__ = 'folder_file'
    fileId = db.Column(db.Integer, db.ForeignKey(File.Model.__table__.c.fileId), primary_key=True)
    folderId = db.Column(db.Integer, db.ForeignKey(Folder.Model.__table__.c.folderId), primary_key=True)

    file = relationship(File.Model, foreign_keys=[fileId])
    folder = relationship(Folder.Model, foreign_keys=[folderId])


Model = FolderFileModel


def get_by_id(folderId, fileId):
    result = Model.query.filter(
        Model.folderId == folderId,
        Model.fileId == fileId
    ).one_or_none()

    return result


def create(folderId, fileId):
    result = Model(
        fileId=fileId,
        folderId=folderId
    )
    db.session.add(result)
    db.session.commit()

    return result
