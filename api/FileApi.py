from flask import send_from_directory

from schemas import File_Schema as Schema
from orm.entities import File as Model
from orm.entities.File import FILE_DIRECTORY


def get_by_id(fileId):
    result = Model.get_by_id(
        fileId=fileId
    )

    return Schema().dump(result).data


def get_inline_file(fileId):
    file = Model.get_by_id(
        fileId=fileId
    )

    return send_from_directory(directory=FILE_DIRECTORY, filename=str(file.fileId), mimetype=file.fileMimeType,
                               attachment_filename=file.fileName)


def get_download_file(fileId):
    file = Model.get_by_id(
        fileId=fileId
    )

    return send_from_directory(directory=FILE_DIRECTORY, filename=str(file.fileId), mimetype=file.fileMimeType,
                               attachment_filename=file.fileName, as_attachment=True)
