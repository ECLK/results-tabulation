from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property

from app import db
from sqlalchemy.orm import relationship

from orm.enums import TallySheetCodeEnum
from util import get_paginated_query, get_tally_sheet_code_string

from orm.entities import SubmissionVersion
from orm.entities.Submission import TallySheet

from exception import NotFoundException
from flask import request


class TallySheetVersionModel(db.Model):
    __tablename__ = 'tallySheetVersion'
    tallySheetVersionId = db.Column(db.Integer, db.ForeignKey(SubmissionVersion.Model.__table__.c.submissionVersionId),
                                    primary_key=True)
    tallySheetVersionCode = db.Column(db.Enum(TallySheetCodeEnum), nullable=False)

    submissionVersion = relationship(SubmissionVersion.Model, foreign_keys=[tallySheetVersionId])

    submission = association_proxy("submissionVersion", "submission")
    tallySheetId = association_proxy("submissionVersion", "submissionId")
    createdBy = association_proxy("submissionVersion", "createdBy")
    createdAt = association_proxy("submissionVersion", "createdAt")

    @hybrid_property
    def htmlUrl(self):
        return "%stally-sheet/%d/version/%d/html" % (request.host_url, self.tallySheetId, self.tallySheetVersionId)

    @hybrid_property
    def contentUrl(self):
        return "%stally-sheet/%s/%d/version/%d" % (
            request.host_url,
            get_tally_sheet_code_string(tally_sheet_code=self.tallySheetVersionCode),
            self.tallySheetId,
            self.tallySheetVersionId
        )

    def __init__(self, tallySheetId):
        tallySheet = TallySheet.get_by_id(tallySheetId=tallySheetId)
        if tallySheet is None:
            raise NotFoundException("Tally sheet not found. (tallySheetId=%d)" % tallySheetId)
        elif tallySheet.tallySheetCode is not self.tallySheetVersionCode:
            raise NotFoundException("Invalid tally sheet. (tallySheetId=%d)" % tallySheetId)

        submissionVersion = SubmissionVersion.create(submissionId=tallySheetId)

        super(TallySheetVersionModel, self).__init__(
            tallySheetVersionId=submissionVersion.submissionVersionId
        )

        db.session.add(self)
        db.session.flush()

    __mapper_args__ = {
        'polymorphic_on': tallySheetVersionCode
    }


Model = TallySheetVersionModel


def get_all(tallySheetId, tallySheetCode=None):
    query = Model.query.filter(Model.tallySheetId == tallySheetId)

    if tallySheetCode is not None:
        query = query.filter(Model.tallySheetCode == tallySheetCode)

    result = get_paginated_query(query).all()

    return result


def get_by_id(tallySheetVersionId):
    result = Model.query.filter(
        Model.tallySheetVersionId == tallySheetVersionId
    ).one_or_none()

    return result
