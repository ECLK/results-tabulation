from typing import Set

from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from app import db
from auth import get_user_access_area_ids, get_user_name, has_role_based_access, ACCESS_TYPE_LOCK, ACCESS_TYPE_UNLOCK, \
    ACCESS_TYPE_READ, DATA_EDITOR_ROLE, get_user_roles
from exception import NotFoundException, MethodNotAllowedException, ForbiddenException
from exception.messages import MESSAGE_CODE_TALLY_SHEET_SAME_USER_CANNOT_SAVE_AND_SUBMIT, \
    MESSAGE_CODE_TALLY_SHEET_NOT_AUTHORIZED_TO_UNLOCK, MESSAGE_CODE_TALLY_SHEET_NOT_AUTHORIZED_TO_LOCK, \
    MESSAGE_CODE_TALLY_SHEET_CANNOT_SUBMIT_AFTER_LOCK, MESSAGE_CODE_TALLY_SHEET_NOT_AUTHORIZED_TO_VIEW, \
    MESSAGE_CODE_TALLY_SHEET_NOT_FOUND, MESSAGE_CODE_TALLY_SHEET_CANNOT_LOCK_BEFORE_SUBMIT
from orm.entities import Submission, Election
from orm.entities.SubmissionVersion import TallySheetVersion
from orm.enums import TallySheetCodeEnum, SubmissionTypeEnum
from util import get_tally_sheet_code, get_tally_sheet_version_class

DATA_ENTRY_TALLY_SHEET_CODES = [
    TallySheetCodeEnum.PRE_41,
    TallySheetCodeEnum.CE_201,
    TallySheetCodeEnum.CE_201_PV,
    TallySheetCodeEnum.PRE_34_CO
]


class TallySheetModel(db.Model):
    __tablename__ = 'tallySheet'

    tallySheetId = db.Column(db.Integer, db.ForeignKey(Submission.Model.__table__.c.submissionId), primary_key=True)
    tallySheetCode = db.Column(db.Enum(TallySheetCodeEnum), nullable=False)

    submission = relationship("SubmissionModel", foreign_keys=[tallySheetId])

    electionId = association_proxy("submission", "electionId")
    areaId = association_proxy("submission", "areaId")
    area = association_proxy("submission", "area")
    latestVersionId = association_proxy("submission", "latestVersionId")
    latestStamp = association_proxy("submission", "latestStamp")
    lockedVersionId = association_proxy("submission", "lockedVersionId")
    lockedStamp = association_proxy("submission", "lockedStamp")
    submittedVersionId = association_proxy("submission", "submittedVersionId")
    submittedStamp = association_proxy("submission", "submittedStamp")
    locked = association_proxy("submission", "locked")
    submitted = association_proxy("submission", "submitted")
    submissionProofId = association_proxy("submission", "submissionProofId")
    versions = association_proxy("submission", "versions")

    def set_latest_version(self, tallySheetVersion: TallySheetVersion):
        if tallySheetVersion is None:
            self.submission.set_latest_version(submissionVersion=None)
        else:
            self.submission.set_latest_version(submissionVersion=tallySheetVersion.submissionVersion)

    def set_locked_version(self, tallySheetVersion: TallySheetVersion):
        if tallySheetVersion is None:
            if not has_role_based_access(self, ACCESS_TYPE_UNLOCK):
                raise ForbiddenException(
                    message="User not authorized to unlock the tally sheet.",
                    code=MESSAGE_CODE_TALLY_SHEET_NOT_AUTHORIZED_TO_UNLOCK
                )

            self.submission.set_locked_version(submissionVersion=None)
        else:
            if self.tallySheetCode in DATA_ENTRY_TALLY_SHEET_CODES:
                if self.submittedVersionId is None:
                    raise ForbiddenException(
                        message="Data entry tally sheet cannot be locked before submitting",
                        code=MESSAGE_CODE_TALLY_SHEET_CANNOT_LOCK_BEFORE_SUBMIT
                    )
                elif self.submittedStamp.createdBy == get_user_name():
                    raise ForbiddenException(
                        message="Data entry tally sheet submitted user is not allowed to lock/unlock.",
                        code=MESSAGE_CODE_TALLY_SHEET_SAME_USER_CANNOT_SAVE_AND_SUBMIT
                    )

            if not has_role_based_access(self, ACCESS_TYPE_LOCK):
                raise ForbiddenException(
                    message="User is not authorized to lock the tally sheet.",
                    code=MESSAGE_CODE_TALLY_SHEET_NOT_AUTHORIZED_TO_LOCK
                )

            self.submission.set_locked_version(submissionVersion=tallySheetVersion.submissionVersion)

    def set_submitted_version(self, tallySheetVersion: TallySheetVersion):
        if self.locked:
            raise ForbiddenException(
                message="Tally sheet is already locked.",
                code=MESSAGE_CODE_TALLY_SHEET_CANNOT_SUBMIT_AFTER_LOCK
            )

        if tallySheetVersion is None:
            self.submission.set_submitted_version(submissionVersion=None)
        else:
            self.submission.set_submitted_version(submissionVersion=tallySheetVersion.submissionVersion)

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

    def create_empty_version(self):
        tallySheetVersion = get_tally_sheet_version_class(self.tallySheetCode).Model(
            tallySheetId=self.tallySheetId
        )

        return tallySheetVersion

    def create_version(self):
        # if self.locked is True:
        #     raise MethodNotAllowedException("Tally sheet is Locked. (tallySheetId=%d)" % self.tallySheetId)

        tallySheetVersion = self.create_empty_version()

        return tallySheetVersion


Model = TallySheetModel


def get_by_id(tallySheetId, tallySheetCode=None):
    query = Model.query.join(
        Submission.Model,
        Submission.Model.submissionId == Model.tallySheetId
    ).filter(
        Model.tallySheetId == tallySheetId
    )

    if tallySheetCode is not None:
        query = query.filter(Model.tallySheetCode == tallySheetCode)

    # Filter by authorized areas
    user_access_area_ids: Set[int] = get_user_access_area_ids()
    query = query.filter(Submission.Model.areaId.in_(user_access_area_ids))

    result = query.one_or_none()

    # if not has_role_based_access(result, ACCESS_TYPE_READ):
    #     raise ForbiddenException(
    #         message="User doesn't have access to tally sheet.",
    #         code=MESSAGE_CODE_TALLY_SHEET_NOT_AUTHORIZED_TO_VIEW
    #     )

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

    return query


def create(tallySheetCode, electionId, areaId):
    result = Model(
        tallySheetCode=tallySheetCode,
        electionId=electionId,
        areaId=areaId
    )

    return result


def create_empty_version(tallySheetId, tallySheetCode=None):
    tallySheet = get_by_id(tallySheetId=tallySheetId, tallySheetCode=tallySheetCode)
    if tallySheet is None:
        raise NotFoundException(
            message="Tally sheet not found. (tallySheetId=%d)" % tallySheetId,
            code=MESSAGE_CODE_TALLY_SHEET_NOT_FOUND
        )

    tallySheetVersion = tallySheet.create_empty_version()

    return tallySheet, tallySheetVersion


def create_version(tallySheetId, tallySheetCode=None):
    tallySheet = get_by_id(tallySheetId=tallySheetId, tallySheetCode=tallySheetCode)
    if tallySheet is None:
        raise NotFoundException(
            message="Tally sheet not found. (tallySheetId=%d, tallySheetCode=%s)" % (tallySheetId, tallySheetCode.name),
            code=MESSAGE_CODE_TALLY_SHEET_NOT_FOUND
        )

    tallySheetVersion = tallySheet.create_version()

    return tallySheet, tallySheetVersion


def create_latest_version(tallySheetId, tallySheetCode=None):
    tallySheet, tallySheetVersion = create_version(tallySheetId, tallySheetCode)
    tallySheet.set_latest_version(tallySheetVersion=tallySheetVersion)

    return tallySheet, tallySheetVersion
