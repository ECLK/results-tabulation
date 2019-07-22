from config import db
from models import FileTypeEnum


class FileModel(db.Model):
    __tablename__ = 'file'
    fileId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fileType = db.Column(db.Enum(FileTypeEnum), nullable=False)
    fileName = db.Column(db.String(100), nullable=True)
    fileMimeType = db.Column(db.String(100), nullable=False)
    fileContentLength = db.Column(db.String(100), nullable=False)
    fileContentType = db.Column(db.String(100), nullable=False)
    fileCollectionId = db.Column(db.Integer, db.ForeignKey("file_collection.fileCollectionId"), nullable=True)

    __mapper_args__ = {
        'polymorphic_on': fileType,
        'polymorphic_identity': FileTypeEnum.Any
    }
