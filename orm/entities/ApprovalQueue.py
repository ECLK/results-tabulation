from config import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from orm.enums import StationaryItemTypeEnum
from orm.entities import StationaryItem, Election


class ApprovalQueueModel(db.Model):
    __tablename__ = 'approval_queue'
    approvalQueueId =db.Column(db.Integer, primary_key=True, autoincrement=True)


Model = ApprovalQueueModel


def get_all():
    result = Model.query.all()

    return result


def create():
    result = Model()
    db.session.add(result)
    db.session.commit()

    return result
