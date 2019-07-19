from config import db

from models import FileModel as Model
import os

FILE_DIRECTORY = os.path.join(os.getcwd(), 'data')


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
        fileCollectionId=fileCollectionId
    )

    db.session.add(result)
    db.session.commit()

    save_file(result, fileSource)

    return result


def save_file(file, fileSource):
    file_path = os.path.join(FILE_DIRECTORY, str(file.fileId))

    fileSource.save(file_path)

    return file_path
