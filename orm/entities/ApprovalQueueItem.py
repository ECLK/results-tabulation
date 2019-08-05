from config import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from orm.entities import Election, ApprovalQueue


class ApprovalQueueItemModel(db.Model):
    __tablename__ = 'approval_queue_item'
    approvalQueueItemId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    approvalQueueId = db.Column(db.Integer, db.ForeignKey(ApprovalQueue.Model.__table__.c.electionId), primary_key=True)

    approvalQueueItemUsers = relationship("ApprovalQueueItemUserModel")

    users = association_proxy("approvalQueueItemUsers", "user")


Model = ApprovalQueueItemModel


def get_all():
    result = Model.query.all()

    return result


def create():
    result = Model()
    db.session.add(result)
    db.session.commit()

    return result
