from config import db
from sqlalchemy.orm import relationship

class FileCollectionModel(db.Model):
    __tablename__ = 'file_collection'
    fileCollectionId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    files = relationship("FileModel")
