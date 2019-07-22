from models import FileTypeEnum, FileModel


class ImageModel(FileModel):
    __mapper_args__ = {
        'polymorphic_identity': FileTypeEnum.Image
    }
