from typing import Set

from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from app import db
from sqlalchemy.orm import relationship

from auth import get_user_access_area_ids
from exception.messages import MESSAGE_CODE_TALLY_SHEET_NOT_FOUND
from orm.enums import TallySheetCodeEnum
from util import get_tally_sheet_code_string, get_tally_sheet_version_class
from orm.entities import SubmissionVersion
from orm.entities.Submission import TallySheet
from exception import NotFoundException
from flask import request


class TallySheetVersionModel(db.Model):
    __tablename__ = 'tallySheetVersion'
    tallySheetVersionId = db.Column(db.Integer, db.ForeignKey(SubmissionVersion.Model.__table__.c.submissionVersionId),
                                    primary_key=True)
    tallySheetVersionCode = db.Column(db.Enum(TallySheetCodeEnum), nullable=False)
    isComplete = db.Column(db.Boolean, default=False, nullable=False)
    submissionVersion = relationship(SubmissionVersion.Model, foreign_keys=[tallySheetVersionId])

    submission = association_proxy("submissionVersion", "submission")
    tallySheetId = association_proxy("submissionVersion", "submissionId")
    createdBy = association_proxy("submissionVersion", "createdBy")
    createdAt = association_proxy("submissionVersion", "createdAt")
    stamp = association_proxy("submissionVersion", "stamp")

    def set_complete(self):
        self.isComplete = True

    def set_locked(self):
        self.submissionVersion.set_locked()

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
        submissionVersion = SubmissionVersion.create(submissionId=tallySheetId)

        super(TallySheetVersionModel, self).__init__(
            tallySheetVersionId=submissionVersion.submissionVersionId
        )

        db.session.add(self)
        db.session.flush()

    def add_invalid_vote_count(self, electionId, rejectedVoteCount, areaId=None):
        from orm.entities.TallySheetVersionRow import TallySheetVersionRow_RejectedVoteCount

        TallySheetVersionRow_RejectedVoteCount.createAreaWiseCount(
            electionId=electionId,
            tallySheetVersionId=self.tallySheetVersionId,
            areaId=areaId,
            rejectedVoteCount=rejectedVoteCount
        )

    __mapper_args__ = {
        'polymorphic_on': tallySheetVersionCode
    }


Model = TallySheetVersionModel


def get_all(tallySheetId, tallySheetCode=None):
    query = Model.query.filter(Model.tallySheetId == tallySheetId)

    if tallySheetCode is not None:
        query = query.filter(Model.tallySheetCode == tallySheetCode)

    return query


def get_by_id(tallySheetId, tallySheetVersionId):
    tallySheet = TallySheet.get_by_id(tallySheetId=tallySheetId)
    if tallySheet is None:
        raise NotFoundException(
            message="Tally sheet not found. (tallySheetId=%d)" % tallySheetId,
            code=MESSAGE_CODE_TALLY_SHEET_NOT_FOUND
        )

    tallySheetVersion = get_tally_sheet_version_class(tallySheet.tallySheetCode).Model.query.filter(
        Model.tallySheetVersionId == tallySheetVersionId,
        Model.tallySheetId == tallySheetId
    ).one_or_none()

    return tallySheetVersion


def create_candidate_preference_struct(tallySheetContent):
    temp_data = {}
    struct = []
    total_vote_count = 0
    for candidateIndex in range(len(tallySheetContent)):
        candidate = tallySheetContent[candidateIndex]

        if candidate.preferenceNumber == 1 and candidate.preferenceCount is not None:
            total_vote_count += candidate.preferenceCount

        if candidate.candidateId not in temp_data and candidate.qualifiedForPreferences is True:
            temp_data[candidate.candidateId] = {
                "number": len(temp_data) + 1,
                "name": candidate.candidateName,
                "firstPreferenceCount": "",
                "secondPreferenceCount": "",
                "thirdPreferenceCount": "",
                "partyAbbreviation": candidate.partyAbbreviation,
                "partyName": candidate.partyName,
                "total": 0
            }

    for row_index in range(len(tallySheetContent)):
        row = tallySheetContent[row_index]
        if row.preferenceCount is not None and row.candidateId in temp_data:

            if row.preferenceNumber == 1:
                preference = "firstPreferenceCount"
            elif row.preferenceNumber == 2:
                preference = "secondPreferenceCount"
            elif row.preferenceNumber == 3:
                preference = "thirdPreferenceCount"
            else:
                preference = ""

            temp_data[row.candidateId]['name'] = row.candidateName
            temp_data[row.candidateId][preference] = row.preferenceCount
            temp_data[row.candidateId]["total"] = temp_data[row.candidateId]["total"] + row.preferenceCount
            temp_data[row.candidateId]["partyAbbreviation"] = temp_data[row.candidateId]["partyAbbreviation"]
            temp_data[row.candidateId]["partyName"] = temp_data[row.candidateId]["partyName"]

    for i in temp_data:
        struct.append(temp_data[i])

    return struct, total_vote_count
