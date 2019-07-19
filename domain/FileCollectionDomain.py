from config import db

from models import FileCollectionModel as Model
import os


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
