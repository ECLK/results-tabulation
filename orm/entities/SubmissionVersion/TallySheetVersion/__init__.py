from app import db
from sqlalchemy.orm import relationship

from util import get_paginated_query

from orm.entities import SubmissionVersion
from orm.entities.Submission import TallySheet

from orm.entities.SubmissionVersion.TallySheetVersion import TallySheetVersionPRE41
from exception import NotFoundException


class TallySheetVersionModel(db.Model):
    __tablename__ = 'tallySheetVersion'
    tallySheetVersionId = db.Column(db.Integer, db.ForeignKey(SubmissionVersion.Model.__table__.c.submissionVersionId),
                                    primary_key=True)

    submissionVersion = relationship(SubmissionVersion.Model, foreign_keys=[tallySheetVersionId])


Model = TallySheetVersionModel


def get_all(tallySheetId, tallySheetCode=None):
    query = Model.query.filter(Model.tallySheetId == tallySheetId)

    if tallySheetCode is not None:
        query = query.filter(Model.tallySheetCode == tallySheetCode)

    result = get_paginated_query(query).all()

    return result


def create(tallySheetId):
    tallySheet = TallySheet.get_by_id(tallySheetId=tallySheetId)
    if tallySheet is None:
        raise NotFoundException("Tally sheet not found. (tallySheetId=%d)" % tallySheetId)

    submissionVersion = SubmissionVersion.create(submissionId=tallySheetId)

    result = Model(
        tallySheetVersionId=submissionVersion.submissionVersionId
    )
    db.session.add(result)
    db.session.commit()

    return result
