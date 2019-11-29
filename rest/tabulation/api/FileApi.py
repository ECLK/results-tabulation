from flask import send_from_directory

from schemas import File_Schema as Schema
from orm.entities.IO import File as Model
from orm.entities.IO.File import FILE_DIRECTORY


def get_by_id(fileId):
    result = Model.get_by_id(
        fileId=fileId
    )

    return Schema().dump(result).data


def response_file(fileId, as_attachment):
    file = Model.get_by_id(
        fileId=fileId
    )

    fileName = "%d-%s" % (file.fileId, file.fileName)

    return send_from_directory(
        directory=FILE_DIRECTORY,
        filename=str(file.fileId),
        mimetype=file.fileMimeType,
        attachment_filename=fileName,
        as_attachment=as_attachment
    )


def get_inline_file(fileId):
    return response_file(
        fileId=fileId,
        as_attachment=False
    )


def get_download_file(fileId):
    return response_file(
        fileId=fileId,
        as_attachment=True
    )
