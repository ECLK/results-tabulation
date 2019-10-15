from sqlalchemy.ext.hybrid import hybrid_property

from app import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

from util import get_paginated_query

from orm.entities import Submission
from orm.entities.History import HistoryVersion

from exception import NotFoundException


class SubmissionVersionModel(db.Model):
    __tablename__ = 'submissionVersion'
    submissionVersionId = db.Column(db.Integer, db.ForeignKey(HistoryVersion.Model.__table__.c.historyVersionId),
                                    primary_key=True)
    submissionId = db.Column(db.Integer, db.ForeignKey("submission.submissionId"))

    submission = relationship("SubmissionModel", foreign_keys=[submissionId])
    historyVersion = relationship(HistoryVersion.Model, foreign_keys=[submissionVersionId])

    createdBy = association_proxy("historyVersion", "createdBy")
    createdAt = association_proxy("historyVersion", "createdAt")
    stamp = association_proxy("historyVersion", "historyStamp")

    def set_locked(self):
        self.submission.set_locked_version(self.submissionVersionId)
        db.session.add(self)
        db.session.flush()

    def __init__(self, submissionId):
        submission = Submission.get_by_id(submissionId=submissionId)
        if submission is None:
            raise NotFoundException("Submission not found. (submissionId=%d)" % submissionId)

        historyVersion = HistoryVersion.create(submissionId)

        super(SubmissionVersionModel, self).__init__(
            submissionId=submissionId,
            submissionVersionId=historyVersion.historyVersionId,
        )
        db.session.add(self)
        db.session.flush()


Model = SubmissionVersionModel


def get_all(submissionId, submissionCode=None):
    query = Model.query.filter(Model.submissionId == submissionId)

    if submissionCode is not None:
        query = query.filter(Model.submissionCode == submissionCode)

    result = get_paginated_query(query).all()

    return result


def create(submissionId):
    result = Model(
        submissionId=submissionId
    )

    return result
