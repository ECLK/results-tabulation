from typing import Set

from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from app import db
from sqlalchemy.orm import relationship

from auth import has_role_based_access
from exception.messages import MESSAGE_CODE_TALLY_SHEET_NOT_FOUND, MESSAGE_CODE_TALLY_SHEET_NOT_AUTHORIZED_TO_SAVE
from ext.ExtendedElection.WORKFLOW_ACTION_TYPE import WORKFLOW_ACTION_TYPE_SAVE
from orm.entities.Election import InvalidVoteCategory
from orm.entities.Template import TemplateRowModel
from orm.entities import SubmissionVersion, TallySheetVersionRow, Area, Candidate, Party, Election
from orm.entities.Submission import TallySheet
from exception import NotFoundException
from flask import request


class TallySheetVersionModel(db.Model):
    __tablename__ = 'tallySheetVersion'
    tallySheetVersionId = db.Column(db.Integer, db.ForeignKey(SubmissionVersion.Model.__table__.c.submissionVersionId),
                                    primary_key=True)
    isComplete = db.Column(db.Boolean, default=True, nullable=False)
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
    def content(self):
        try:
            meta_data_key_to_column_map = {
                # "areaId": Area.Model.areaId,
                "partyId": Party.Model.partyId
            }

            tally_sheet = TallySheet.get_by_id(tallySheetId=self.tallySheetId)
            query_filter = []
            for meta_data in tally_sheet.meta.metaDataList:
                if meta_data.metaDataKey in meta_data_key_to_column_map:
                    query_filter.append(
                        meta_data_key_to_column_map[meta_data.metaDataKey] == meta_data.metaDataValue
                    )

            query_args = [
                TallySheetVersionRow.Model.tallySheetVersionRowId,
                TallySheetVersionRow.Model.electionId,
                TemplateRowModel.templateRowId,
                TemplateRowModel.templateRowType,
                Election.Model.electionId,
                Election.Model.voteType,
                Election.Model.rootElectionId,
                Area.Model.areaId,
                Area.Model.areaName,
                TallySheetVersionRow.Model.ballotBoxId,
                Candidate.Model.candidateId,
                Candidate.Model.candidateName,
                Candidate.Model.candidateNumber,
                Party.Model.partyId,
                Party.Model.partyName,
                Party.Model.partySymbol,
                Party.Model.partyAbbreviation,
                InvalidVoteCategory.Model.invalidVoteCategoryId,
                InvalidVoteCategory.Model.categoryDescription.label("invalidVoteCategoryDescription"),
                TallySheetVersionRow.Model.strValue,
                TallySheetVersionRow.Model.numValue
            ]
            return db.session.query(
                *query_args
            ).join(
                TemplateRowModel,
                TemplateRowModel.templateRowId == TallySheetVersionRow.Model.templateRowId
            ).join(
                Election.Model,
                Election.Model.electionId == TallySheetVersionRow.Model.electionId,
                isouter=True
            ).join(
                Area.Model,
                Area.Model.areaId == TallySheetVersionRow.Model.areaId,
                isouter=True
            ).join(
                Candidate.Model,
                Candidate.Model.candidateId == TallySheetVersionRow.Model.candidateId,
                isouter=True
            ).join(
                Party.Model,
                Party.Model.partyId == TallySheetVersionRow.Model.partyId,
                isouter=True
            ).join(
                InvalidVoteCategory.Model,
                InvalidVoteCategory.Model.invalidVoteCategoryId == TallySheetVersionRow.Model.invalidVoteCategoryId,
                isouter=True
            ).filter(
                TallySheetVersionRow.Model.tallySheetVersionId == self.tallySheetVersionId,
                *query_filter
            ).order_by(
                InvalidVoteCategory.Model.invalidVoteCategoryId,
                Party.Model.partyId,
                Candidate.Model.candidateId,
                Area.Model.areaId
            ).all()
        except Exception as e:
            print("\n\n\n\n\n\n\n### ERROR ### ", e)

    @hybrid_property
    def htmlUrl(self):
        return "%stally-sheet/%d/version/%d/html" % (request.host_url, self.tallySheetId, self.tallySheetVersionId)

    @hybrid_property
    def contentUrl(self):
        return "%stally-sheet/%s/%d/version/%d" % (
            request.host_url,
            "",
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

    @classmethod
    def create(cls, tallySheetId):
        tally_sheet = TallySheet.get_by_id(tallySheetId=tallySheetId)
        if tally_sheet is None:
            raise NotFoundException(
                message="Tally sheet not found. (tallySheetId=%d)" % tallySheetId,
                code=MESSAGE_CODE_TALLY_SHEET_NOT_FOUND
            )

        # Validate the authorization
        if not has_role_based_access(tally_sheet=tally_sheet, access_type=WORKFLOW_ACTION_TYPE_SAVE):
            raise NotFoundException(
                message="Not authorized to edit tally sheet. (tallySheetId=%d)" % tallySheetId,
                code=MESSAGE_CODE_TALLY_SHEET_NOT_AUTHORIZED_TO_SAVE
            )

        return TallySheetVersionModel(tallySheetId=tallySheetId)

    @classmethod
    def get_by_id(cls, tallySheetId, tallySheetVersionId):
        tallySheet = TallySheet.get_by_id(tallySheetId=tallySheetId)
        if tallySheet is None:
            raise NotFoundException(
                message="Tally sheet not found. (tallySheetId=%d)" % tallySheetId,
                code=MESSAGE_CODE_TALLY_SHEET_NOT_FOUND
            )

        tallySheetVersion = Model.query.filter(
            Model.tallySheetVersionId == tallySheetVersionId,
            Model.tallySheetId == tallySheetId
        ).one_or_none()

        return tallySheetVersion

    @classmethod
    def get_all(cls, tallySheetId, tallySheetCode=None):
        query = Model.query.filter(Model.tallySheetId == tallySheetId)

        if tallySheetCode is not None:
            query = query.filter(Model.tallySheetCode == tallySheetCode)

        return query


Model = TallySheetVersionModel

create = TallySheetVersionModel.create
get_by_id = TallySheetVersionModel.get_by_id
get_all = TallySheetVersionModel.get_all


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
