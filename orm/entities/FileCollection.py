from config import db
from sqlalchemy.orm import relationship


class FileCollectionModel(db.Model):
    __tablename__ = 'file_collection'
    fileCollectionId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    files = relationship("FileModel")


Model = FileCollectionModel


def get_by_id(fileCollectionId):
    result = Model.query.filter(
        Model.fileCollectionId == fileCollectionId
    ).one_or_none()

    return result


def create():
    result = Model()
    db.session.add(result)
    db.session.commit()

    return result
