from config import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from orm.entities import Election, ApprovalQueue, ApprovalQueueItem, User
from orm.enums import ApprovalStatusTypeEnum
from datetime import datetime


class ApprovalQueueItemUserModel(db.Model):
    __tablename__ = 'approval_queue_item_status'
    approvalQueueItemId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    approvalStatus = db.Column(db.Enum(ApprovalStatusTypeEnum), nullable=False)
    createdBy = db.Column(db.Integer, db.ForeignKey(User.Model.__table__.c.userId), nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = relationship(User.Model)


Model = ApprovalQueueItemUserModel


def get_all():
    result = Model.query.all()

    return result


def create():
    result = Model()
    db.session.add(result)
    db.session.commit()

    return result
