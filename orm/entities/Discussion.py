from config import db
from sqlalchemy.orm import relationship
from orm.entities import Comment


class DiscussionModel(db.Model):
    __tablename__ = 'discussion'
    discussionId = db.Column(db.Integer, primary_key=True, autoincrement=True)

    comments = relationship(Comment.Model)


Model = DiscussionModel


def create():
    result = Model()
    db.session.add(result)
    db.session.commit()

    return result
