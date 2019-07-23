from config import db
from orm.enums import FileTypeEnum
import os
from orm.entities import FileCollection
from util import Auth
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from flask import Flask, request

FILE_DIRECTORY = os.path.join(os.getcwd(), 'data')


class FileModel(db.Model):
    __tablename__ = 'file'
    fileId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fileType = db.Column(db.Enum(FileTypeEnum), nullable=False)
    fileName = db.Column(db.String(100), nullable=True)
    fileMimeType = db.Column(db.String(100), nullable=False)
    fileContentLength = db.Column(db.String(100), nullable=False)
    fileContentType = db.Column(db.String(100), nullable=False)
    fileCollectionId = db.Column(db.Integer, db.ForeignKey(FileCollection.Model.__table__.c.fileCollectionId),
                                 nullable=True)

    fileCreatedBy = db.Column(db.Integer, nullable=False)
    fileCreatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    @hybrid_property
    def urlInline(self):
        return "%sfile/%d/inline" % (request.host_url, self.fileId)

    @hybrid_property
    def urlDownload(self):
        return "%sfile/%d/download" % (request.host_url, self.fileId)

    __mapper_args__ = {
        'polymorphic_on': fileType,
        'polymorphic_identity': FileTypeEnum.Any
    }


Model = FileModel


def get_by_id(fileId):
    result = Model.query.filter(
        Model.fileId == fileId
    ).one_or_none()

    return result


def create(fileSource, fileType, fileCollectionId=None):
    # TODO validate the
    #   - file type
    #   - file size
    #         etc.

    result = Model(
        fileType=fileType,
        fileMimeType=fileSource.mimetype,
        fileContentLength=fileSource.content_length,
        fileContentType=fileSource.content_type,
        fileName=fileSource.filename,
        fileCollectionId=fileCollectionId,
        fileCreatedBy=Auth().get_user_id()
    )

    db.session.add(result)
    db.session.commit()

    save_file(result, fileSource)

    return result


def save_file(file, fileSource):
    file_path = os.path.join(FILE_DIRECTORY, str(file.fileId))

    fileSource.save(file_path)

    return file_path
