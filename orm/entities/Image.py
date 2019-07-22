from orm.entities import File
from orm.enums import FileTypeEnum


class Model(File.Model):
    __mapper_args__ = {
        'polymorphic_identity': FileTypeEnum.Image
    }


def get_by_id(fileId):
    result = Model.query.filter(
        Model.fileId == fileId
    ).one_or_none()

    return result


def create(fileSource, fileCollectionId=None):
    return File.create(
        fileSource=fileSource,
        fileType=FileTypeEnum.Image,
        fileCollectionId=fileCollectionId
    )
