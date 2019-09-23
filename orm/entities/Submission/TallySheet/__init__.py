from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import or_

from app import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

from orm.entities.SubmissionVersion import TallySheetVersion
from util import get_paginated_query, get_tally_sheet_code

from orm.entities import Submission, Election

from orm.enums import TallySheetCodeEnum, SubmissionTypeEnum


class TallySheetModel(db.Model):
    __tablename__ = 'tallySheet'

    tallySheetId = db.Column(db.Integer, db.ForeignKey(Submission.Model.__table__.c.submissionId), primary_key=True)
    tallySheetCode = db.Column(db.Enum(TallySheetCodeEnum), nullable=False)

    submission = relationship("SubmissionModel", foreign_keys=[tallySheetId])

    electionId = association_proxy("submission", "electionId")
    officeId = association_proxy("submission", "areaId")
    office = association_proxy("submission", "area")
    latestVersionId = association_proxy("submission", "latestVersionId")
    submissionProofId = association_proxy("submission", "submissionProofId")
    versions = association_proxy("submission", "versions")

    @hybrid_property
    def latestVersion(self):
        return TallySheetVersion.Model.query.filter(
            TallySheetVersion.Model.tallySheetVersionId == self.latestVersionId
        ).one_or_none()

    def __init__(self, tallySheetCode, electionId, officeId):
        submission = Submission.create(
            submissionType=SubmissionTypeEnum.TallySheet,
            electionId=electionId,
            areaId=officeId
        )

        super(TallySheetModel, self).__init__(
            tallySheetId=submission.submissionId,
            tallySheetCode=tallySheetCode,
        )

        db.session.add(self)
        db.session.flush()


Model = TallySheetModel


def get_by_id(tallySheetId):
    result = Model.query.filter(
        Model.tallySheetId == tallySheetId
    ).one_or_none()

    return result


def get_all(electionId=None, officeId=None, tallySheetCode=None):
    election = Election.get_by_id(electionId=electionId)

    query = Model.query.join(
        Submission.Model,
        Submission.Model.submissionId == Model.tallySheetId
    ).join(
        Election.Model,
        Election.Model.electionId == Submission.Model.electionId
    )

    if electionId is not None:
        query = query.filter(
            Election.Model.electionId.in_(election.mappedElectionIds)
        )

    if officeId is not None:
        query = query.filter(Submission.Model.areaId == officeId)

    if tallySheetCode is not None:
        query = query.filter(Model.tallySheetCode == get_tally_sheet_code(tallySheetCode))

    result = get_paginated_query(query).all()

    return result


def create(tallySheetCode, electionId, officeId):
    result = Model(
        tallySheetCode=tallySheetCode,
        electionId=electionId,
        officeId=officeId
    )

    return result
