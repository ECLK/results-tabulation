from config import db


class Model(db.Model):
    __tablename__ = 'file_collection'
    fileCollectionId = db.Column(db.Integer, primary_key=True, autoincrement=True)


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
