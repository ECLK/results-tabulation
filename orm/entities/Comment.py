from config import db
from orm.entities import Discussion
from datetime import datetime


class CommentModel(db.Model):
    __tablename__ = 'comment'
    commentId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    discussionId = db.Column(db.Integer, db.ForeignKey(Discussion.Model.__table__.c.discussionId))
    createdBy = db.Column(db.Integer, nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


Model = CommentModel


def create():
    result = Model()
    db.session.add(result)
    db.session.commit()

    return result
