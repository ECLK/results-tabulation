from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship
from app import db
from orm.entities.Audit import Stamp
from orm.enums import FileTypeEnum
from sqlalchemy.ext.hybrid import hybrid_property
from flask import request
from sqlalchemy.dialects.mysql import LONGBLOB


class FileModel(db.Model):
    __tablename__ = 'file'
    fileId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fileType = db.Column(db.Enum(FileTypeEnum), nullable=False)
    fileName = db.Column(db.String(100), nullable=True)
    fileMimeType = db.Column(db.String(100), nullable=False)
    fileContentLength = db.Column(db.String(100), nullable=False)
    fileContentType = db.Column(db.String(100), nullable=False)
    fileContent = db.Column(LONGBLOB, nullable=True)
    fileStampId = db.Column(db.Integer, db.ForeignKey(Stamp.Model.__table__.c.stampId), nullable=False)

    fileStamp = relationship(Stamp.Model, foreign_keys=[fileStampId])
    fileCreatedBy = association_proxy("fileStamp", "createdBy")
    fileCreatedAt = association_proxy("fileStamp", "createdAt")

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


def createFromFileSource(fileSource, fileType=FileTypeEnum.Any):
    # TODO validate the
    #   - file type
    #   - file size
    #         etc.

    file_stamp = Stamp.create()

    if fileType is None:
        fileType = FileTypeEnum.Any

    result = Model(
        fileType=fileType,
        fileMimeType=fileSource.mimetype,
        fileContentLength=fileSource.content_length,
        fileContentType=fileSource.content_type,
        fileContent=fileSource.stream.read(),
        fileName=fileSource.filename,
        fileStampId=file_stamp.stampId
    )

    db.session.add(result)
    db.session.flush()

    return result
