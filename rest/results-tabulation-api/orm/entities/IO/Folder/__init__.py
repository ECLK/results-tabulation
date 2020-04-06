from app import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy


class FolderModel(db.Model):
    __tablename__ = 'folder'
    folderId = db.Column(db.Integer, primary_key=True, autoincrement=True)

    folderFiles = relationship("FolderFileModel")

    files = association_proxy("folderFiles", "file")

    @classmethod
    def create(cls):
        folder = cls()
        db.session.add(folder)
        db.session.flush()

        return folder


Model = FolderModel
create = Model.create


def get_by_id(folderId):
    result = Model.query.filter(
        Model.folderId == folderId
    ).one_or_none()

    return result
