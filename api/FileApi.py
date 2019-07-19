from flask import abort
from util import RequestBody

from flask import send_from_directory
import os
import connexion

from schemas import File_Schema as Schema
from domain import FileDomain as Domain
from domain.FileDomain import FILE_DIRECTORY


def get_by_id(fileId):
    result = Domain.get_by_id(
        fileId=fileId
    )

    return Schema().dump(result).data


def get_inline_file(fileId):
    file = Domain.get_by_id(
        fileId=fileId
    )

    return send_from_directory(directory=FILE_DIRECTORY, filename=str(file.fileId), mimetype=file.fileMimeType,
                               attachment_filename=file.fileName)


def get_download_file(fileId):
    file = Domain.get_by_id(
        fileId=fileId
    )

    return send_from_directory(directory=FILE_DIRECTORY, filename=str(file.fileId), mimetype=file.fileMimeType,
                               attachment_filename=file.fileName, as_attachment=True)
