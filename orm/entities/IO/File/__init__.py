import shutil

from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from app import db
from orm.entities.Audit import Stamp
from orm.enums import FileTypeEnum
import os
from sqlalchemy.ext.hybrid import hybrid_property
from flask import request

FILE_DIRECTORY = os.path.join(os.getcwd(), 'data')


class FileModel(db.Model):
    __tablename__ = 'file'
    fileId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fileType = db.Column(db.Enum(FileTypeEnum), nullable=False)
    fileName = db.Column(db.String(100), nullable=True)
    fileMimeType = db.Column(db.String(100), nullable=False)
    fileContentLength = db.Column(db.String(100), nullable=False)
    fileContentType = db.Column(db.String(100), nullable=False)
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
        fileName=fileSource.filename,
        fileStampId=file_stamp.stampId
    )

    db.session.add(result)
    db.session.flush()

    save_uploaded_file_source(result, fileSource)

    return result


#
#
# def createReport(fileName, html):
#     file = Model(
#         fileType=FileTypeEnum.Pdf,
#         fileMimeType="application/pdf",
#         fileContentLength=len(html),
#         fileContentType="application/pdf ",
#         fileName=fileName,
#         fileCreatedBy=Auth().get_user_id()
#     )
#
#     db.session.add(file)
#     db.session.flush()
#
#     options = {}
#     file_path = os.path.join(FILE_DIRECTORY, str(file.fileId))
#     pdfkit.from_string(html, file_path, options=options)
#
#     return file


def save_uploaded_file_source(file, fileSource):
    file_path = os.path.join(FILE_DIRECTORY, str(file.fileId))

    fileSource.save(file_path)

    return file_path


def copy_file(fileId: int, target_file: str):
    source_file = os.path.join(FILE_DIRECTORY, str(fileId))
    shutil.copyfile(source_file, target_file)
