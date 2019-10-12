from typing import Set

from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from app import db
from auth import get_user_access_area_ids
from orm.entities import Submission, Election
from orm.entities.SubmissionVersion import TallySheetVersion
from orm.enums import TallySheetCodeEnum, SubmissionTypeEnum
from util import get_paginated_query, get_tally_sheet_code


class TallySheetModel(db.Model):
    __tablename__ = 'tallySheet'

    tallySheetId = db.Column(db.Integer, db.ForeignKey(Submission.Model.__table__.c.submissionId), primary_key=True)
    tallySheetCode = db.Column(db.Enum(TallySheetCodeEnum), nullable=False)

    submission = relationship("SubmissionModel", foreign_keys=[tallySheetId])

    electionId = association_proxy("submission", "electionId")
    areaId = association_proxy("submission", "areaId")
    areaId = association_proxy("submission", "area")
    latestVersionId = association_proxy("submission", "latestVersionId")
    lockedVersionId = association_proxy("submission", "lockedVersionId")
    locked = association_proxy("submission", "locked")
    submissionProofId = association_proxy("submission", "submissionProofId")
    versions = association_proxy("submission", "versions")

    def set_latest_version(self, tallySheetVersion: TallySheetVersion):
        if tallySheetVersion is None:
            self.submission.set_latest_version(submissionVersion=None)
        else:
            self.submission.set_latest_version(submissionVersion=tallySheetVersion.submissionVersion)

    def set_locked_version(self, tallySheetVersion: TallySheetVersion):
        if tallySheetVersion is None:
            self.submission.set_locked_version(submissionVersion=None)
        else:
            self.submission.set_locked_version(submissionVersion=tallySheetVersion.submissionVersion)

    @hybrid_property
    def latestVersion(self):
        return TallySheetVersion.Model.query.filter(
            TallySheetVersion.Model.tallySheetVersionId == self.latestVersionId
        ).one_or_none()

    def __init__(self, tallySheetCode, electionId, areaId):
        submission = Submission.create(
            submissionType=SubmissionTypeEnum.TallySheet,
            electionId=electionId,
            areaId=areaId
        )

        super(TallySheetModel, self).__init__(
            tallySheetId=submission.submissionId,
            tallySheetCode=tallySheetCode,
        )

        db.session.add(self)
        db.session.flush()


Model = TallySheetModel


def get_by_id(tallySheetId):
    query = Model.query.join(
        Submission.Model,
        Submission.Model.submissionId == Model.tallySheetId
    ).filter(
        Model.tallySheetId == tallySheetId
    )

    # Filter by authorized areas
    user_access_area_ids: Set[int] = get_user_access_area_ids()
    query = query.filter(Submission.Model.areaId.in_(user_access_area_ids))

    result = query.one_or_none()

    return result


def get_all(electionId=None, areaId=None, tallySheetCode=None):
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

    if areaId is not None:
        query = query.filter(Submission.Model.areaId == areaId)

    if tallySheetCode is not None:
        query = query.filter(Model.tallySheetCode == get_tally_sheet_code(tallySheetCode))

    # Filter by authorized areas
    user_access_area_ids: Set[int] = get_user_access_area_ids()
    query = query.filter(Submission.Model.areaId.in_(user_access_area_ids))

    result = get_paginated_query(query).all()

    return result


def create(tallySheetCode, electionId, areaId):
    result = Model(
        tallySheetCode=tallySheetCode,
        electionId=electionId,
        areaId=areaId
    )

    return result
