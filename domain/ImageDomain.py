from config import db

from models import ImageModel as Model, FileTypeEnum
from domain import FileDomain


def get_by_id(fileId):
    result = Model.query.filter(
        Model.fileId == fileId
    ).one_or_none()

    return result


def create(fileSource, fileCollectionId = None):
    return FileDomain.create(
        fileSource=fileSource,
        fileType=FileTypeEnum.Image,
        fileCollectionId=fileCollectionId
    )
