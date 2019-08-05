from config import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from orm.entities import Election, ApprovalQueue, ApprovalQueueItem, User
from orm.enums import ApprovalStatusTypeEnum


class ApprovalQueueItemUserModel(db.Model):
    __tablename__ = 'approval_queue_item_user'
    userId = db.Column(db.Integer, db.ForeignKey(User.Model.__table__.c.userId), primary_key=True)
    approvalQueueItemId = db.Column(db.Integer, db.ForeignKey(ApprovalQueueItem.Model.__table__.c.approvalQueueItemId),
                                    primary_key=True)

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
