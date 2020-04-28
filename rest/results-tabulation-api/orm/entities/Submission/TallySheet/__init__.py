from typing import Set
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from app import db
from auth import get_user_access_area_ids, get_user_name, has_role_based_access
from constants.TALLY_SHEET_COLUMN_SOURCE import TALLY_SHEET_COLUMN_SOURCE_META
from exception import NotFoundException, ForbiddenException
from exception.messages import MESSAGE_CODE_TALLY_SHEET_SAME_USER_CANNOT_SAVE_AND_SUBMIT, \
    MESSAGE_CODE_TALLY_SHEET_NOT_AUTHORIZED_TO_UNLOCK, MESSAGE_CODE_TALLY_SHEET_NOT_AUTHORIZED_TO_LOCK, \
    MESSAGE_CODE_TALLY_SHEET_CANNOT_SUBMIT_AFTER_LOCK, MESSAGE_CODE_TALLY_SHEET_NOT_FOUND, \
    MESSAGE_CODE_TALLY_SHEET_CANNOT_LOCK_BEFORE_SUBMIT, \
    MESSAGE_CODE_TALLY_SHEET_CANNOT_BE_NOTIFIED_BEFORE_LOCK, \
    MESSAGE_CODE_TALLY_SHEET_CANNOT_BE_RELEASED_BEFORE_NOTIFYING, MESSAGE_CODE_TALLY_SHEET_ALREADY_RELEASED, \
    MESSAGE_CODE_TALLY_SHEET_ALREADY_NOTIFIED, MESSAGE_CODE_TALLY_SHEET_NOT_AUTHORIZED_TO_VIEW
from ext.ExtendedElection.WORKFLOW_ACTION_TYPE import WORKFLOW_ACTION_TYPE_VIEW
from ext.ExtendedTallySheet import ExtendedTallySheet
from orm.entities import Submission, Election, Template, TallySheetVersionRow, Candidate, Party, Area, Meta
from orm.entities.Dashboard import StatusReport
from orm.entities.Election import ElectionCandidate, ElectionParty, InvalidVoteCategory
from orm.entities.SubmissionVersion import TallySheetVersion
from orm.entities.Template import TemplateRow_DerivativeTemplateRow_Model, TemplateRowModel
from orm.entities.Workflow import WorkflowInstance, WorkflowActionModel
from orm.enums import SubmissionTypeEnum, AreaTypeEnum
from sqlalchemy import and_, func, or_, case, bindparam

from util import get_dict_key_value_or_none


class TallySheetModel(db.Model):
    __tablename__ = 'tallySheet'

    tallySheetId = db.Column(db.Integer, db.ForeignKey(Submission.Model.__table__.c.submissionId), primary_key=True)
    templateId = db.Column(db.Integer, db.ForeignKey(Template.Model.__table__.c.templateId), nullable=False)
    statusReportId = db.Column(db.Integer, db.ForeignKey(StatusReport.Model.__table__.c.statusReportId), nullable=True)
    metaId = db.Column(db.Integer, db.ForeignKey(Meta.Model.__table__.c.metaId), nullable=False)
    workflowInstanceId = db.Column(db.Integer, db.ForeignKey(WorkflowInstance.Model.__table__.c.workflowInstanceId),
                                   nullable=True)

    submission = relationship("SubmissionModel", foreign_keys=[tallySheetId])
    statusReport = relationship(StatusReport.Model, foreign_keys=[statusReportId])
    template = relationship(Template.Model, foreign_keys=[templateId])
    meta = relationship(Meta.Model, foreign_keys=[metaId])
    _workflowInstance = relationship(WorkflowInstance.Model, foreign_keys=[workflowInstanceId])

    electionId = association_proxy("submission", "electionId")
    election = association_proxy("submission", "election")
    areaId = association_proxy("submission", "areaId")
    area = association_proxy("submission", "area")
    latestVersionId = association_proxy("submission", "latestVersionId")
    latestStamp = association_proxy("submission", "latestStamp")
    lockedVersionId = association_proxy("submission", "lockedVersionId")
    lockedVersion = association_proxy("submission", "lockedVersion")
    notifiedVersionId = association_proxy("submission", "notifiedVersionId")
    notifiedVersion = association_proxy("submission", "notifiedVersion")
    releasedVersionId = association_proxy("submission", "releasedVersionId")
    releasedVersion = association_proxy("submission", "releasedVersion")
    lockedStamp = association_proxy("submission", "lockedStamp")
    submittedVersionId = association_proxy("submission", "submittedVersionId")
    submittedStamp = association_proxy("submission", "submittedStamp")
    locked = association_proxy("submission", "locked")
    submitted = association_proxy("submission", "submitted")
    notified = association_proxy("submission", "notified")
    released = association_proxy("submission", "released")
    submissionProofId = association_proxy("submission", "submissionProofId")
    submissionProof = association_proxy("submission", "submissionProof")
    versions = association_proxy("submission", "versions")
    metaDataList = association_proxy("meta", "metaDataList")

    children = relationship("TallySheetModel", secondary="tallySheet_tallySheet", lazy="subquery",
                            primaryjoin="TallySheetModel.tallySheetId==TallySheetTallySheetModel.parentTallySheetId",
                            secondaryjoin="TallySheetModel.tallySheetId==TallySheetTallySheetModel.childTallySheetId"
                            )
    parents = relationship("TallySheetModel", secondary="tallySheet_tallySheet", lazy="subquery",
                           primaryjoin="TallySheetModel.tallySheetId==TallySheetTallySheetModel.childTallySheetId",
                           secondaryjoin="TallySheetModel.tallySheetId==TallySheetTallySheetModel.parentTallySheetId"
                           )

    def get_tally_sheet_workflow_instance_actions(self, workflow_instance):
        tally_sheet_workflow_instance_actions = db.session.query(
            WorkflowActionModel.workflowActionId,
            WorkflowActionModel.actionName,
            WorkflowActionModel.actionType,
            WorkflowActionModel.fromStatus,
            WorkflowActionModel.toStatus
        ).filter(
            WorkflowActionModel.workflowId == workflow_instance.workflowId
        ).order_by(
            WorkflowActionModel.workflowActionId
        ).all()

        processed_tally_sheet_workflow_instance_actions = []
        for tally_sheet_workflow_instance_action in tally_sheet_workflow_instance_actions:
            processed_tally_sheet_workflow_instance_actions.append({
                "workflowActionId": tally_sheet_workflow_instance_action.workflowActionId,
                "actionName": tally_sheet_workflow_instance_action.actionName,
                "actionType": tally_sheet_workflow_instance_action.actionType,
                "fromStatus": tally_sheet_workflow_instance_action.fromStatus,
                "toStatus": tally_sheet_workflow_instance_action.toStatus,
                "allowed": tally_sheet_workflow_instance_action.fromStatus == workflow_instance.status,
                "authorized": has_role_based_access(tally_sheet=self,
                                                    access_type=tally_sheet_workflow_instance_action.actionType)
            })

        return processed_tally_sheet_workflow_instance_actions

    @hybrid_property
    def workflowInstance(self):
        tally_sheet_workflow_instance = self._workflowInstance
        setattr(tally_sheet_workflow_instance, "actions",
                self.get_tally_sheet_workflow_instance_actions(tally_sheet_workflow_instance))

        return tally_sheet_workflow_instance

    @hybrid_property
    def areaMapList(self):
        extended_election = self.submission.election.get_extended_election()
        area_map = extended_election.get_area_map_for_tally_sheet(tally_sheet=self)

        return area_map

    def add_parent(self, parentTallySheet):
        parentTallySheet.add_child(self)

        return self

    def add_child(self, childTallySheet):
        existing_mapping = TallySheetTallySheetModel.query.filter(
            TallySheetTallySheetModel.parentTallySheetId == self.tallySheetId,
            TallySheetTallySheetModel.childTallySheetId == childTallySheet.tallySheetId
        ).one_or_none()

        if existing_mapping is None:
            tallySheetAssociation = TallySheetTallySheetModel(
                parentTallySheetId=self.tallySheetId,
                childTallySheetId=childTallySheet.tallySheetId
            )
            db.session.add(tallySheetAssociation)
            db.session.flush()

        return self

    @hybrid_property
    def tallySheetCode(self):
        return self.template.templateName

    def get_status_report_type(self):
        electoral_district_name = ""
        polling_division_name = ""
        status_report_type = ""

        election = self.submission.election
        submission_area = self.submission.area
        # if self.tallySheetCode == PRE_30_PD:
        #     if election.voteType is Postal:
        #         electoral_district_name = submission_area.areaName
        #         status_report_type = "PV"
        #     else:
        #         electoral_district_name = _get_electoral_district_name(submission_area)
        #         polling_division_name = submission_area.areaName
        #         status_report_type = "PD"
        # elif self.tallySheetCode == PRE_34_PD:
        #     if election.voteType is Postal:
        #         electoral_district_name = submission_area.areaName
        #         status_report_type = "PV [Revised]"
        #     else:
        #         electoral_district_name = _get_electoral_district_name(submission_area)
        #         polling_division_name = submission_area.areaName
        #         status_report_type = "PD [Revised]"
        # elif self.tallySheetCode == PRE_30_ED:
        #     electoral_district_name = submission_area.areaName
        #     status_report_type = "ED"
        # elif self.tallySheetCode == PRE_34_ED:
        #     electoral_district_name = submission_area.areaName
        #     status_report_type = "ED [Revised]"
        # else:
        # TODO
        status_report_type = self.tallySheetCode

        return electoral_district_name, polling_division_name, status_report_type

    def get_report_status(self):
        pass
        # if self.template.has_data_entry():
        #     if self.locked:
        #         if self.released:
        #             return "RELEASED"
        #         elif self.notified:
        #             return "NOTIFIED"
        #         elif self.submissionProof.size() > 0:
        #             return "CERTIFIED"
        #         else:
        #             return "VERIFIED"
        #     elif self.submitted:
        #         return "SUBMITTED"
        #     elif self.latestVersionId is not None:
        #         return "ENTERED"
        #     else:
        #         return "NOT ENTERED"
        # else:
        #     if self.locked:
        #         if self.released:
        #             return "RELEASED"
        #         elif self.notified:
        #             return "NOTIFIED"
        #         elif self.submissionProof.size() > 0:
        #             return "CERTIFIED"
        #         else:
        #             return "VERIFIED"
        #     else:
        #         return "PENDING"

    def update_status_report(self):
        pass
        # election = self.submission.election.get_root_election()
        #
        # if self.statusReportId is None:
        #     electoral_district_name, polling_division_name, status_report_type = self.get_status_report_type()
        #     status_report = StatusReport.create(
        #         electionId=election.electionId,
        #         reportType=status_report_type,
        #         electoralDistrictName=electoral_district_name,
        #         pollingDivisionName=polling_division_name,
        #         status=self.get_report_status()
        #     )
        #
        #     self.statusReportId = status_report.statusReportId
        # else:
        #     self.statusReport.update_status(
        #         status=self.get_report_status()
        #     )

    def set_latest_version(self, tallySheetVersion: TallySheetVersion):
        if tallySheetVersion is None:
            self.submission.set_latest_version(submissionVersion=None)
        else:
            self.submission.set_latest_version(submissionVersion=tallySheetVersion.submissionVersion)

        self.update_status_report()

    @hybrid_property
    def latestVersion(self):
        return TallySheetVersion.Model.query.filter(
            TallySheetVersion.Model.tallySheetVersionId == self.latestVersionId
        ).one_or_none()

    @classmethod
    def create(cls, template, electionId, areaId, metaId, workflowInstanceId, parentTallySheets=None,
               childTallySheets=None):

        submission = Submission.create(
            submissionType=SubmissionTypeEnum.TallySheet,
            electionId=electionId,
            areaId=areaId
        )

        tally_sheet = TallySheetModel(
            tallySheetId=submission.submissionId,
            templateId=template.templateId,
            metaId=metaId,
            workflowInstanceId=workflowInstanceId
        )

        db.session.add(tally_sheet)
        db.session.flush()

        if parentTallySheets is not None:
            for parentTallySheet in parentTallySheets:
                tally_sheet.add_parent(parentTallySheet)

        if childTallySheets is not None:
            for childTallySheet in childTallySheets:
                tally_sheet.add_child(childTallySheet)

        return tally_sheet

    def create_empty_version(self):
        tally_sheet_version = TallySheetVersion.create(tallySheetId=self.tallySheetId)

        return tally_sheet_version

    def create_version(self, content=None):
        tally_sheet_version = self.create_empty_version()

        # Create derived rows first. (Passing None as Content)
        self.create_tally_sheet_version_rows(tally_sheet_version=tally_sheet_version, content=None)

        db.session.commit()

        # Generate a post save content only if the content input is not defined.
        if content is None:
            extended_tally_sheet_version = self.get_extended_tally_sheet_version(
                tallySheetVersionId=tally_sheet_version.tallySheetVersionId)
            content = extended_tally_sheet_version.get_post_save_request_content()

        # Create data entry rows.
        self.create_tally_sheet_version_rows(tally_sheet_version=tally_sheet_version, content=content)

        return tally_sheet_version

    def create_latest_version(self, content=None):
        tally_sheet, tally_sheet_version = create_version(self.tallySheetId, content=content)
        tally_sheet.set_latest_version(tallySheetVersion=tally_sheet_version)

        return tally_sheet, tally_sheet_version

    def get_template_row_query_parameters(self, templateRow, only_group_by_columns=False):
        extended_tally_sheet = self.get_extended_tally_sheet()
        meta_data_map = {}
        for metaData in self.meta.metaDataList:
            meta_data_map[metaData.metaDataKey] = metaData.metaDataValue

        column_name_map = extended_tally_sheet.get_template_column_to_query_column_map()
        template_column_to_query_filter_map = extended_tally_sheet.get_template_column_to_query_filter_map(
            only_group_by_columns=only_group_by_columns)
        column_function_map = {
            "sum": func.sum,
            "count": func.count,
            "group_concat": func.group_concat
        }

        query_args = [
            TallySheetModel.tallySheetId
        ]
        group_by_args = []
        filter_by_args = []

        for templateRowColumn in templateRow.columns:

            column_name = templateRowColumn.templateRowColumnName
            column = column_name_map[column_name]

            if only_group_by_columns and not templateRowColumn.grouped:
                column = bindparam(column_name, None)
            else:
                if templateRowColumn.func is not None:
                    column_func = column_function_map[templateRowColumn.func]
                    column = column_func(column).label(column_name)

                if templateRowColumn.grouped:
                    group_by_args.append(column)

                if column_name in template_column_to_query_filter_map:
                    filter_by_args += template_column_to_query_filter_map[column_name]

                if column_name in meta_data_map:
                    # TODO
                    if column_name == "partyId":
                        filter_by_args.append(column_name_map[column_name] == meta_data_map[column_name])

            query_args.append(column)

        return query_args, group_by_args, filter_by_args

    def create_tally_sheet_version_rows(self, tally_sheet_version, content=None):
        meta_data_map = {}
        for metaData in self.meta.metaDataList:
            meta_data_map[metaData.metaDataKey] = metaData.metaDataValue

        extended_election = self.submission.election.get_extended_election()
        is_tally_sheet_version_complete = tally_sheet_version.isComplete

        for templateRow in self.template.rows:

            content_rows = []

            if content is None and templateRow.isDerived is True:

                # Retrieve completed tally sheet results.
                query_args, group_by_args, filter_by_args = self.get_template_row_query_parameters(
                    templateRow=templateRow)

                filter_by_args += [
                    # Child tally sheets
                    TallySheetTallySheetModel.parentTallySheetId == self.tallySheetId,
                    TallySheetTallySheetModel.childTallySheetId == TallySheetModel.tallySheetId,
                    Submission.Model.submissionId == TallySheetModel.tallySheetId,

                    # Tally sheet templates
                    TemplateRow_DerivativeTemplateRow_Model.templateRowId == templateRow.templateRowId,
                    TemplateRowModel.templateId == TallySheetModel.templateId,
                    TemplateRow_DerivativeTemplateRow_Model.derivativeTemplateRowId == TemplateRowModel.templateRowId,

                    # Workflow
                    WorkflowInstance.Model.workflowInstanceId == TallySheetModel.workflowInstanceId,
                    WorkflowInstance.Model.status.in_(
                        extended_election.tally_sheet_verified_statuses_list()
                    ),

                    # Tally sheet rows
                    TallySheetVersionRow.Model.templateRowId == TemplateRowModel.templateRowId,
                    TallySheetVersionRow.Model.tallySheetVersionId == Submission.Model.latestVersionId,
                ]

                complete_tally_sheet_results = db.session.query(*query_args).filter(*filter_by_args).group_by(
                    *group_by_args).all()

                # Retrieve incomplete tally sheet results.
                query_args, group_by_args, filter_by_args = self.get_template_row_query_parameters(
                    templateRow=templateRow, only_group_by_columns=True)

                filter_by_args += [
                    # Child tally sheets
                    TallySheetTallySheetModel.parentTallySheetId == self.tallySheetId,
                    TallySheetTallySheetModel.childTallySheetId == TallySheetModel.tallySheetId,
                    Submission.Model.submissionId == TallySheetModel.tallySheetId,

                    # Tally sheet templates
                    TemplateRow_DerivativeTemplateRow_Model.templateRowId == templateRow.templateRowId,
                    TemplateRowModel.templateId == TallySheetModel.templateId,
                    TemplateRow_DerivativeTemplateRow_Model.derivativeTemplateRowId == TemplateRowModel.templateRowId,

                    # Workflow
                    WorkflowInstance.Model.workflowInstanceId == TallySheetModel.workflowInstanceId,
                    WorkflowInstance.Model.status.notin_(
                        extended_election.tally_sheet_verified_statuses_list()
                    )
                ]

                incomplete_tally_sheet_results = db.session.query(*query_args).filter(*filter_by_args).group_by(
                    *group_by_args).all()

                aggregated_results = complete_tally_sheet_results + incomplete_tally_sheet_results

                for aggregated_result in aggregated_results:
                    content_row = {}

                    for templateRowColumn in templateRow.columns:
                        column_name = templateRowColumn.templateRowColumnName
                        content_row[column_name] = getattr(aggregated_result, column_name)

                    content_rows.append(content_row)

            elif content is not None:

                for content_row in content:
                    if content_row["templateRowId"] == templateRow.templateRowId:
                        for template_row_column in templateRow.columns:
                            if template_row_column.source == TALLY_SHEET_COLUMN_SOURCE_META:
                                template_row_column_name = template_row_column.templateRowColumnName
                                content_row[template_row_column_name] = meta_data_map[template_row_column_name]

                        content_rows.append(content_row)

                if templateRow.hasMany is False and len(content_rows) > 0:
                    content_rows = [content_rows[0]]

            for content_row in content_rows:

                # Update the completed flag to False if there are null values in any row.
                if "numValue" not in content_row or content_row["numValue"] is None:
                    is_tally_sheet_version_complete = False

                TallySheetVersionRow.create(
                    templateRow=templateRow,
                    tallySheetVersion=tally_sheet_version,
                    electionId=get_dict_key_value_or_none(content_row, "electionId"),
                    numValue=get_dict_key_value_or_none(content_row, "numValue"),
                    strValue=get_dict_key_value_or_none(content_row, "strValue"),
                    areaId=get_dict_key_value_or_none(content_row, "areaId"),
                    candidateId=get_dict_key_value_or_none(content_row, "candidateId"),
                    partyId=get_dict_key_value_or_none(content_row, "partyId"),
                    ballotBoxId=get_dict_key_value_or_none(content_row, "ballotBoxId"),
                    invalidVoteCategoryId=get_dict_key_value_or_none(content_row, "invalidVoteCategoryId")
                )

        if is_tally_sheet_version_complete:
            tally_sheet_version.isComplete = True
        else:
            tally_sheet_version.isComplete = False

    def get_extended_tally_sheet_version(self, tallySheetVersionId):
        tally_sheet_version = TallySheetVersion.get_by_id(tallySheetId=self.tallySheetId,
                                                          tallySheetVersionId=tallySheetVersionId)
        extended_election = self.submission.election.get_extended_election()
        extended_tally_sheet_class = extended_election.get_extended_tally_sheet_class(
            self.template.templateName)
        extended_tally_sheet_version = extended_tally_sheet_class.ExtendedTallySheetVersion(
            tallySheet=self,
            tallySheetVersion=tally_sheet_version
        )

        return extended_tally_sheet_version

    def get_extended_tally_sheet(self):
        extended_election = self.submission.election.get_extended_election()
        extended_tally_sheet_class = extended_election.get_extended_tally_sheet_class(
            self.template.templateName)
        extended_tally_sheet = extended_tally_sheet_class(self)

        return extended_tally_sheet

    def html(self, tallySheetVersionId):
        extended_tally_sheet_version = self.get_extended_tally_sheet_version(tallySheetVersionId=tallySheetVersionId)
        return extended_tally_sheet_version.html()

    def html_letter(self, tallySheetVersionId):
        extended_tally_sheet_version = self.get_extended_tally_sheet_version(tallySheetVersionId=tallySheetVersionId)
        return extended_tally_sheet_version.html_letter()


Model = TallySheetModel
create = Model.create


class TallySheetTallySheetModel(db.Model):
    __tablename__ = 'tallySheet_tallySheet'
    parentTallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), primary_key=True)
    childTallySheetId = db.Column(db.Integer, db.ForeignKey("tallySheet.tallySheetId"), primary_key=True)


def _get_electoral_district_name(polling_division):
    electoral_district_name = ""
    electoral_district = polling_division.get_associated_areas(
        areaType=AreaTypeEnum.ElectoralDistrict,
        electionId=polling_division.electionId
    )
    if len(electoral_district) > 0:
        electoral_district_name = electoral_district[0].areaName

    return electoral_district_name


def get_by_id(tallySheetId, tallySheetCode=None):
    # Filter by authorized areas
    user_access_area_ids: Set[int] = get_user_access_area_ids()

    query_args = [TallySheetModel]
    query_filters = [
        TallySheetModel.tallySheetId == tallySheetId,
        Submission.Model.areaId.in_(user_access_area_ids),
        Template.Model.templateId == Model.templateId,
        Submission.Model.submissionId == Model.tallySheetId
    ]
    query_group_by = [Model.tallySheetId]

    if tallySheetCode is not None:
        query_filters.append(Template.Model.templateName == tallySheetCode)

    tally_sheet = db.session.query(*query_args).filter(*query_filters).group_by(*query_group_by).one_or_none()

    # Validate the authorization
    if not has_role_based_access(tally_sheet=tally_sheet, access_type=WORKFLOW_ACTION_TYPE_VIEW):
        raise NotFoundException(
            message="Not authorized to view tally sheet. (tallySheetId=%d)" % tallySheetId,
            code=MESSAGE_CODE_TALLY_SHEET_NOT_AUTHORIZED_TO_VIEW
        )

    return tally_sheet


def get_all(electionId=None, areaId=None, tallySheetCode=None, voteType=None):
    # Filter by authorized areas
    user_access_area_ids: Set[int] = get_user_access_area_ids()

    query_args = [Model]
    query_filters = [
        Submission.Model.areaId.in_(user_access_area_ids),
        Template.Model.templateId == Model.templateId,
        Submission.Model.submissionId == Model.tallySheetId,
        Election.Model.electionId == Submission.Model.electionId
    ]
    query_group_by = [Model.tallySheetId]

    if areaId is not None:
        query_filters.append(Submission.Model.areaId == areaId)

    if electionId is not None:
        election = Election.get_by_id(electionId=electionId)
        query_filters.append(Election.Model.electionId.in_(election.get_this_and_below_election_ids()))

    if tallySheetCode is not None:
        query_filters.append(Template.Model.templateName == tallySheetCode)

    if voteType is not None:
        query_filters.append(Election.Model.voteType == voteType)

    tally_sheet_list = db.session.query(*query_args).filter(*query_filters).group_by(*query_group_by)

    authorized_tally_sheet_list = []
    for tally_sheet in tally_sheet_list:
        if has_role_based_access(tally_sheet=tally_sheet, access_type=WORKFLOW_ACTION_TYPE_VIEW):
            authorized_tally_sheet_list.append(tally_sheet)

    return authorized_tally_sheet_list


def create_empty_version(tallySheetId):
    tallySheet = get_by_id(tallySheetId=tallySheetId)
    if tallySheet is None:
        raise NotFoundException(
            message="Tally sheet not found. (tallySheetId=%d)" % tallySheetId,
            code=MESSAGE_CODE_TALLY_SHEET_NOT_FOUND
        )

    tallySheetVersion = tallySheet.create_empty_version()

    return tallySheet, tallySheetVersion


def create_version(tallySheetId, content=None):
    tally_sheet = get_by_id(tallySheetId=tallySheetId)
    if tally_sheet is None:
        raise NotFoundException(
            message="Tally sheet not found. (tallySheetId=%d)" % (tallySheetId),
            code=MESSAGE_CODE_TALLY_SHEET_NOT_FOUND
        )

    tallySheetVersion = tally_sheet.create_version(content=content)

    return tally_sheet, tallySheetVersion
