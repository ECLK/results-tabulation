import pandas as pd

from flask import render_template
from sqlalchemy import MetaData
import requests
import app
from app import db
from auth import get_user_name, has_role_based_access
from constants.VOTE_TYPES import Postal, NonPostal
from exception import MethodNotAllowedException, UnauthorizedException
from exception.messages import MESSAGE_CODE_TALLY_SHEET_NOT_AUTHORIZED_TO_VERIFY, \
    MESSAGE_CODE_WORKFLOW_ACTION_NOT_AUTHORIZED, MESSAGE_CODE_TALLY_SHEET_NO_LONGER_READABLE, \
    MESSAGE_CODE_TALLY_SHEET_NO_LONGER_EDITABLE, MESSAGE_CODE_TALLY_SHEET_NO_LONGER_ACCEPTING_PROOF_DOCUMENTS, \
    MESSAGE_CODE_TALLY_SHEET_INCOMPLETE, \
    MESSAGE_CODE_TALLY_SHEET_CANNOT_BE_UNLOCKED_WHILE_HAVING_VERIFIED_PARENT_SUMMARY_SHEETS
from ext.ExtendedElection.WORKFLOW_ACTION_TYPE import WORKFLOW_ACTION_TYPE_SAVE, WORKFLOW_ACTION_TYPE_VERIFY, \
    WORKFLOW_ACTION_TYPE_VIEW, WORKFLOW_ACTION_TYPE_UPLOAD_PROOF_DOCUMENT, WORKFLOW_ACTION_TYPE_EDIT, \
    WORKFLOW_ACTION_TYPE_SUBMIT, WORKFLOW_ACTION_TYPE_REQUEST_CHANGES, WORKFLOW_ACTION_TYPE_RELEASE, \
    WORKFLOW_ACTION_TYPE_RELEASE_NOTIFY
from ext.ExtendedElection.WORKFLOW_STATUS_TYPE import WORKFLOW_STATUS_TYPE_EMPTY, WORKFLOW_STATUS_TYPE_SAVED, \
    WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED
from external_services import results_dist

from orm.entities import Workflow, Meta
from orm.entities.Meta import MetaData
from orm.entities.Workflow import WorkflowInstance, WorkflowActionModel
from orm.entities.Workflow.WorkflowInstance import WorkflowInstanceLog
from util import to_comma_seperated_num, to_percentage, convert_image_to_data_uri, \
    get_sum_of_numbers_only_and_nan_otherwise

DEFAULT_HTML_TABLE_COLUMNS = [
    "tallySheetVersionRowId",
    "electionId",
    # "electionName",
    "templateRowId",
    "templateRowType",
    "voteType",
    "rootElectionId",
    "areaId",
    "areaName",
    "candidateId",
    "candidateName",
    "candidateNumber",
    "candidateType",
    "electionPartyId",
    "partyId",
    "partyName",
    "partySymbol",
    "partyAbbreviation",
    "invalidVoteCategoryId",
    "invalidVoteCategoryDescription",
    "strValue",
    "numValue"
]


class ExtendedTallySheet:
    def __init__(self, tallySheet):
        self.tallySheet = tallySheet

    def get_template_column_to_query_column_map(self):
        from orm.entities import Election, Area, Candidate, Party, TallySheetVersionRow
        from orm.entities.Election import InvalidVoteCategory

        return {
            "electionId": Election.Model.electionId,
            "areaId": Area.Model.areaId,
            "candidateId": Candidate.Model.candidateId,
            "partyId": Party.Model.partyId,
            "numValue": TallySheetVersionRow.Model.numValue,
            "strValue": TallySheetVersionRow.Model.strValue,
            "ballotBoxId": TallySheetVersionRow.Model.ballotBoxId,
            "invalidVoteCategoryId": InvalidVoteCategory.Model.invalidVoteCategoryId
        }

    def get_template_column_to_query_filter_map(self, only_group_by_columns=False):
        from orm.entities import Election, Area, Candidate, Party, TallySheetVersionRow, Submission
        from orm.entities.Election import InvalidVoteCategory, ElectionCandidate, ElectionParty

        if only_group_by_columns:
            return {
                "electionId": [
                    Election.Model.electionId == Submission.Model.electionId
                ],
                "areaId": [
                    Area.Model.areaId == Submission.Model.areaId
                ],
                "candidateId": [
                    ElectionCandidate.Model.electionId == Election.Model.electionId,
                    Candidate.Model.candidateId == ElectionCandidate.Model.candidateId,
                    Party.Model.partyId == ElectionCandidate.Model.partyId
                ],
                "partyId": [
                    ElectionParty.Model.electionId == Election.Model.electionId,
                    Party.Model.partyId == ElectionParty.Model.partyId
                ],
                "invalidVoteCategoryId": []
            }
        else:
            return {
                "electionId": [
                    Election.Model.electionId == Submission.Model.electionId
                ],
                "areaId": [
                    Area.Model.areaId == Submission.Model.areaId
                ],
                "candidateId": [
                    Candidate.Model.candidateId == TallySheetVersionRow.Model.candidateId,
                    Party.Model.partyId == TallySheetVersionRow.Model.partyId,
                    ElectionCandidate.Model.electionId == Election.Model.electionId,
                    Candidate.Model.candidateId == ElectionCandidate.Model.candidateId,
                    Party.Model.partyId == ElectionCandidate.Model.partyId
                ],
                "partyId": [
                    Party.Model.partyId == TallySheetVersionRow.Model.partyId,
                    ElectionParty.Model.electionId == Election.Model.electionId,
                    Party.Model.partyId == ElectionParty.Model.partyId
                ],
                "invalidVoteCategoryId": [
                    InvalidVoteCategory.Model.invalidVoteCategoryId == TallySheetVersionRow.Model.invalidVoteCategoryId]
            }

    def execute_workflow_action(self, workflowActionId, tallySheetVersionId, content=None):
        workflow_action = db.session.query(
            WorkflowActionModel
        ).filter(
            WorkflowActionModel.fromStatus == WorkflowInstance.Model.status,
            WorkflowInstance.Model.workflowInstanceId == self.tallySheet.workflowInstanceId,
            WorkflowActionModel.workflowActionId == workflowActionId
        ).one_or_none()

        self.authorize_workflow_action(workflow_action=workflow_action, content=content)

        tally_sheet_version = self.on_workflow_tally_sheet_version(
            workflow_action=workflow_action, tallySheetVersionId=tallySheetVersionId, content=content)

        self.on_before_workflow_action(workflow_action=workflow_action, tally_sheet_version=tally_sheet_version)

        self.on_workflow_action(workflow_action=workflow_action, content=content,
                                tally_sheet_version=tally_sheet_version)

        return self.tallySheet

    def authorize_workflow_action(self, workflow_action, content=None):
        from auth import has_role_based_access

        if not has_role_based_access(election=self.tallySheet.submission.election,
                                     tally_sheet_code=self.tallySheet.tallySheetCode,
                                     access_type=workflow_action.actionType):
            UnauthorizedException(message="Not allowed to %s" % (workflow_action.actionName),
                                  code=MESSAGE_CODE_WORKFLOW_ACTION_NOT_AUTHORIZED)

        if workflow_action.actionType == WORKFLOW_ACTION_TYPE_REQUEST_CHANGES and workflow_action.toStatus in [
            WORKFLOW_STATUS_TYPE_SAVED, WORKFLOW_STATUS_TYPE_EMPTY]:

            from orm.entities.Submission import TallySheet
            from orm.entities.Submission.TallySheet import TallySheetTallySheetModel

            extended_election = self.tallySheet.submission.election.get_extended_election()

            verified_parent_tally_sheets = db.session.query(
                TallySheet.Model.tallySheetId
            ).filter(
                TallySheetTallySheetModel.childTallySheetId == self.tallySheet.tallySheetId,
                TallySheet.Model.tallySheetId == TallySheetTallySheetModel.parentTallySheetId,
                WorkflowInstance.Model.workflowInstanceId == TallySheet.Model.workflowInstanceId,
                WorkflowInstance.Model.status.in_(
                    extended_election.tally_sheet_verified_statuses_list()
                )
            ).all()

            if len(verified_parent_tally_sheets) > 0:
                raise MethodNotAllowedException(
                    message="Cannot request changes since the data from this report has been already aggregated in verified summary reports.",
                    code=MESSAGE_CODE_TALLY_SHEET_CANNOT_BE_UNLOCKED_WHILE_HAVING_VERIFIED_PARENT_SUMMARY_SHEETS)

    def on_workflow_tally_sheet_version(self, workflow_action, tallySheetVersionId, content=None):
        from orm.entities import SubmissionVersion
        from orm.entities.SubmissionVersion import TallySheetVersion

        tally_sheet_version = db.session.query(
            TallySheetVersion.Model
        ).filter(
            SubmissionVersion.Model.submissionId == self.tallySheet.tallySheetId,
            SubmissionVersion.Model.submissionVersionId == TallySheetVersion.Model.tallySheetVersionId,
            TallySheetVersion.Model.tallySheetVersionId == MetaData.Model.metaDataValue,
            MetaData.Model.metaDataKey == "tallySheetVersionId",
            MetaData.Model.metaId == Meta.Model.metaId,
            Meta.Model.metaId == WorkflowInstanceLog.Model.metaId,
            WorkflowInstanceLog.Model.workflowInstanceLogId == WorkflowInstance.Model.latestLogId,
            WorkflowInstance.Model.workflowInstanceId == self.tallySheet.workflowInstanceId
        ).one_or_none()

        return tally_sheet_version

    def on_before_workflow_action(self, workflow_action, tally_sheet_version):
        if not tally_sheet_version.isComplete:
            raise MethodNotAllowedException(message="Incomplete tally sheet.", code=MESSAGE_CODE_TALLY_SHEET_INCOMPLETE)

    def on_workflow_action(self, workflow_action, tally_sheet_version, content=None):
        self.tallySheet.workflowInstance.execute_action(
            action=workflow_action,
            meta=Meta.create({
                "tallySheetVersionId": tally_sheet_version.tallySheetVersionId
            })
        )

        if workflow_action.actionType == WORKFLOW_ACTION_TYPE_RELEASE:
            self.on_release_result(tally_sheet_version=tally_sheet_version)
        elif workflow_action.actionType == WORKFLOW_ACTION_TYPE_RELEASE_NOTIFY:
            self.on_release_result_notify(tally_sheet_version=tally_sheet_version)

        return self.tallySheet

    def on_get_release_result_params(self):
        result_type = None
        result_code = None
        ed_code = None
        ed_name = None
        pd_code = None
        pd_name = None

        return result_type, result_code, ed_code, ed_name, pd_code, pd_name

    def on_release_result_notify(self, tally_sheet_version):
        result_type, result_code, result_level, ed_code, ed_name, pd_code, pd_name = self.on_get_release_result_params()

        extended_tally_sheet_version = self.tallySheet.get_extended_tally_sheet_version(
            tallySheetVersionId=tally_sheet_version.tallySheetVersionId)
        data = extended_tally_sheet_version.json()

        results_dist.notify_release_result(result_type=result_type, result_code=result_code, data=data)

    def on_release_result(self, tally_sheet_version):
        result_type, result_code, result_level, ed_code, ed_name, pd_code, pd_name = self.on_get_release_result_params()

        extended_tally_sheet_version = self.tallySheet.get_extended_tally_sheet_version(
            tallySheetVersionId=tally_sheet_version.tallySheetVersionId)
        data = extended_tally_sheet_version.json()

        results_dist.release_result(result_type=result_type, result_code=result_code, data=data,
                                    stamp=tally_sheet_version.stamp)
        results_dist.upload_release_documents(result_type=result_type, result_code=result_code,
                                              files=self.tallySheet.workflowInstance.proof.scannedFiles)

    def execute_tally_sheet_proof_upload(self):
        workflow_actions = self.on_before_tally_sheet_proof_upload()
        self.on_tally_sheet_proof_upload()
        self.on_after_tally_sheet_proof_upload(workflow_actions=workflow_actions)

        return self.tallySheet

    def on_before_tally_sheet_proof_upload(self):
        workflow_actions = self._get_allowed_workflow_actions(
            workflow_action_type=WORKFLOW_ACTION_TYPE_UPLOAD_PROOF_DOCUMENT)

        if len(workflow_actions) == 0:
            raise MethodNotAllowedException(message="Tally sheet is longer accepting proof documents.",
                                            code=MESSAGE_CODE_TALLY_SHEET_NO_LONGER_ACCEPTING_PROOF_DOCUMENTS)

        return workflow_actions

    def on_tally_sheet_proof_upload(self):
        pass

    def on_after_tally_sheet_proof_upload(self, workflow_actions):
        tally_sheet_version = self.tallySheet.latestVersion
        if tally_sheet_version is not None:
            self._execute_workflow_actions_list(tally_sheet_version=tally_sheet_version,
                                                workflow_actions=workflow_actions)

    def execute_tally_sheet_get(self):
        workflow_actions = self.on_before_tally_sheet_get()
        self.on_tally_sheet_get()
        self.on_after_tally_sheet_get(workflow_actions=workflow_actions)

        return self.tallySheet

    def on_before_tally_sheet_get(self):
        workflow_actions = self._get_allowed_workflow_actions(workflow_action_type=WORKFLOW_ACTION_TYPE_VIEW)

        if len(workflow_actions) == 0:
            raise MethodNotAllowedException(message="Tally sheet is no longer readable.",
                                            code=MESSAGE_CODE_TALLY_SHEET_NO_LONGER_READABLE)

        return workflow_actions

    def on_tally_sheet_get(self):
        pass

    def on_after_tally_sheet_get(self, workflow_actions):
        tally_sheet_version = self.tallySheet.latestVersion
        if tally_sheet_version is not None:
            self._execute_workflow_actions_list(tally_sheet_version=tally_sheet_version,
                                                workflow_actions=workflow_actions)

    def execute_tally_sheet_post(self, content=None):
        workflow_actions = self.on_before_tally_sheet_post()
        tally_sheet_version = self.on_tally_sheet_post(content=content)
        self.on_after_tally_sheet_post(tally_sheet_version=tally_sheet_version, workflow_actions=workflow_actions)

    def _get_allowed_workflow_actions(self, workflow_action_type):
        workflow_actions = db.session.query(
            WorkflowActionModel
        ).filter(
            WorkflowActionModel.fromStatus == WorkflowInstance.Model.status,
            WorkflowInstance.Model.workflowInstanceId == self.tallySheet.workflowInstanceId,
            Workflow.Model.workflowId == WorkflowInstance.Model.workflowId,
            WorkflowActionModel.workflowId == WorkflowInstance.Model.workflowId,
            WorkflowActionModel.actionType == workflow_action_type
        ).all()

        authorized_workflow_actions = []
        for workflow_action in workflow_actions:
            if has_role_based_access(election=self.tallySheet.submission.election,
                                     tally_sheet_code=self.tallySheet.tallySheetCode,
                                     access_type=workflow_action.actionType):
                authorized_workflow_actions.append(workflow_action)

        return authorized_workflow_actions

    def on_before_tally_sheet_post(self):
        workflow_actions = self._get_allowed_workflow_actions(workflow_action_type=WORKFLOW_ACTION_TYPE_SAVE)

        if len(workflow_actions) == 0:
            raise MethodNotAllowedException(message="Tally sheet is no longer editable.",
                                            code=MESSAGE_CODE_TALLY_SHEET_NO_LONGER_EDITABLE)

        return workflow_actions

    def on_tally_sheet_post(self, content=None):
        tally_sheet, tally_sheet_version = self.tallySheet.create_latest_version(content=content)
        db.session.commit()

        return tally_sheet_version

    def _execute_workflow_actions_list(self, tally_sheet_version, workflow_actions):
        for tally_sheet_post_action in workflow_actions:
            self.tallySheet.workflowInstance.execute_action(
                action=tally_sheet_post_action,
                meta=Meta.create({"tallySheetVersionId": tally_sheet_version.tallySheetVersionId})
            )

        db.session.commit()

    def on_after_tally_sheet_post(self, tally_sheet_version, workflow_actions):
        self._execute_workflow_actions_list(tally_sheet_version=tally_sheet_version, workflow_actions=workflow_actions)

    class ExtendedTallySheetVersion:
        def __init__(self, tallySheet, tallySheetVersion):
            self.tallySheet = tallySheet
            self.tallySheetVersion = tallySheetVersion

            tallySheetVersionContent = tallySheetVersion.content

            index = []
            columns = [column for column in DEFAULT_HTML_TABLE_COLUMNS]
            data = []

            for content_row_index in range(len(tallySheetVersion.content)):
                content_row = tallySheetVersionContent[content_row_index]
                data_row = [getattr(content_row, column) for column in columns]
                data_row.append(getattr(content_row, "numValue"))

                index.append(content_row_index)
                data.append(data_row)

            columns.append("incompleteNumValue")

            self.df = pd.DataFrame(data=data, index=index, columns=columns)

        def json(self):
            return {
                "type": "RP_V",
                "level": "POLLING-DIVISION",
                "ed_code": "",
                "ed_name": "",
                "pd_code": "",
                "pd_name": "",
                "by_party": [
                    {
                        "party_code": "",
                        "party_name": "",
                        "vote_count": 0,
                        "vote_percentage": "",
                        "seat_count": "",
                        "national_list_seat_count": 0
                    }
                ],
                "by_candidate": [
                    {
                        "party_code": "",
                        "party_name": "",
                        "candidate_number": "",
                        "candidate_name": "",
                        "candidate_type": ""
                    }
                ],
                "summary": {
                    "valid": 0,
                    "rejected": 0,
                    "polled": 0,
                    "electors": 0,
                    "percent_polled": "",
                    "percent_valid": "",
                    "percent_rejected": ""
                }
            }

        def get_post_save_request_content(self):
            return []

        def html_letter(self, title="", total_registered_voters=None, required_signatures=[]):
            tallySheetVersion = self.tallySheetVersion
            stamp = tallySheetVersion.stamp

            if total_registered_voters is None:
                total_registered_voters = tallySheetVersion.submission.area.get_registered_voters_count()

            content = {
                "resultTitle": title,
                "election": {
                    "electionName": tallySheetVersion.submission.election.get_official_name()
                },
                "stamp": {
                    "createdAt": stamp.createdAt,
                    "createdBy": stamp.createdBy,
                    "barcodeString": stamp.barcodeString
                },
                "date": stamp.createdAt.strftime("%d/%m/%Y"),
                "time": stamp.createdAt.strftime("%H:%M:%S %p"),
                "data": [
                ],
                "validVoteCounts": [0, 0],
                "rejectedVoteCounts": [0, 0],
                "totalVoteCounts": [0, 0],
                "registeredVoters": [
                    to_comma_seperated_num(total_registered_voters),
                    100
                ]
            }

            candidate_wise_valid_vote_count_result = self.get_candidate_wise_valid_vote_count_result()
            vote_count_result = self.get_vote_count_result()
            valid_vote_count_result = self.get_valid_vote_count_result()
            rejected_vote_count_result = self.get_rejected_vote_count_result()

            for candidate_wise_valid_non_postal_vote_count_result_item in candidate_wise_valid_vote_count_result.itertuples():
                content["data"].append([
                    candidate_wise_valid_non_postal_vote_count_result_item.candidateName,
                    candidate_wise_valid_non_postal_vote_count_result_item.partyAbbreviation,
                    to_comma_seperated_num(candidate_wise_valid_non_postal_vote_count_result_item.numValue),
                    to_percentage(candidate_wise_valid_non_postal_vote_count_result_item.numValue * 100 /
                                  valid_vote_count_result["numValue"].values[0]) if
                    valid_vote_count_result["numValue"].values[
                        0] > 0 else ""
                ])

            content["validVoteCounts"] = [
                to_comma_seperated_num(valid_vote_count_result["numValue"].values[0]),
                to_percentage(
                    valid_vote_count_result["numValue"].values[0] * 100 / vote_count_result["numValue"].values[0])
                if vote_count_result["numValue"].values[0] > 0 else ""
            ]

            content["rejectedVoteCounts"] = [
                to_comma_seperated_num(rejected_vote_count_result["numValue"].values[0]),
                rejected_vote_count_result["numValue"].values[0] * 100 / vote_count_result["numValue"].values[0]
                if vote_count_result["numValue"].values[0] > 0 else ""
            ]

            content["totalVoteCounts"] = [
                to_comma_seperated_num(vote_count_result["numValue"].values[0]),
                to_percentage(vote_count_result["numValue"].values[0] * 100 / total_registered_voters)
            ]

            content["logo"] = convert_image_to_data_uri("static/Emblem_of_Sri_Lanka.png")

            html = render_template(
                'PRE_ALL_ISLAND_RESULTS.html',
                content=content
            )

            return html

        def html(self, title="", total_registered_voters=None, columns=None, df=None):
            stamp = self.tallySheetVersion.stamp
            data = []
            if columns is None:
                columns = DEFAULT_HTML_TABLE_COLUMNS
            if df is None:
                df = self.df

            content = {
                "columns": columns,
                "data": data,
                "stamp": {
                    "createdAt": stamp.createdAt,
                    "createdBy": stamp.createdBy,
                    "barcodeString": stamp.barcodeString
                },
            }

            for index, row in df.iterrows():
                data_row = []
                for column in columns:
                    cell_value = df.at[index, column]
                    if cell_value is None:
                        cell_value = ""

                    data_row.append(cell_value)

                data.append(data_row)

            html = render_template(
                'DEFAULT.html',
                content=content
            )

            return html

        def get_candidate_and_area_wise_valid_non_postal_vote_count_result(self):
            df = self.df.copy()

            df = df.loc[df['templateRowType'] == "CANDIDATE_FIRST_PREFERENCE"]
            df = df.loc[df['voteType'] == NonPostal]

            df = df.sort_values(
                by=['electionPartyId', 'partyId', 'partyName', 'partyAbbreviation', 'partySymbol', 'candidateId',
                    'candidateName', 'candidateNumber', 'candidateType', 'areaId', 'areaName'], ascending=True
            ).reset_index()

            return df

        def get_party_and_area_wise_valid_non_postal_vote_count_result(self):
            df = self.df.copy()

            df = df.loc[df['templateRowType'] == "PARTY_WISE_VOTE"]
            df = df.loc[df['voteType'] == NonPostal]

            df = df.sort_values(
                by=['electionPartyId', 'partyId', 'partyName', 'partyAbbreviation', 'partySymbol', 'areaId',
                    'areaName'], ascending=True
            ).reset_index()

            return df

        def get_candidate_wise_valid_non_postal_vote_count_result(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(float)

            df = df.loc[df['templateRowType'] == "CANDIDATE_FIRST_PREFERENCE"]
            df = df.loc[df['voteType'] == NonPostal]

            df = df.groupby(
                ['electionPartyId', 'partyId', 'partyName', 'partyAbbreviation', 'partySymbol', 'candidateId',
                 'candidateName', 'candidateNumber', 'candidateType']
            ).agg({
                'numValue': lambda x: x.sum(skipna=False),
                'incompleteNumValue': get_sum_of_numbers_only_and_nan_otherwise
            }).sort_values(
                by=['electionPartyId', 'partyId', 'candidateId'], ascending=True
            ).reset_index()

            return df

        def get_candidate_wise_valid_postal_vote_count_result(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(float)

            df = df.loc[df['templateRowType'] == "CANDIDATE_FIRST_PREFERENCE"]
            df = df.loc[df['voteType'] == Postal]

            df = df.groupby(
                ['electionPartyId', 'partyId', 'partyName', 'partyAbbreviation', 'partySymbol', 'candidateId',
                 'candidateName', 'candidateNumber', 'candidateType']
            ).agg({
                'numValue': lambda x: x.sum(skipna=False),
                'incompleteNumValue': get_sum_of_numbers_only_and_nan_otherwise
            }).sort_values(
                by=['electionPartyId', 'partyId', 'candidateId'], ascending=True
            ).reset_index()

            return df

        def get_party_wise_valid_postal_vote_count_result(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(float)

            df = df.loc[df['templateRowType'] == "PARTY_WISE_VOTE"]
            df = df.loc[df['voteType'] == Postal]

            df = df.groupby(
                ['electionPartyId', 'partyId', 'partyName', 'partyAbbreviation', 'partySymbol']
            ).agg({
                'numValue': lambda x: x.sum(skipna=False),
                'incompleteNumValue': get_sum_of_numbers_only_and_nan_otherwise
            }).sort_values(
                by=['electionPartyId', 'partyId'], ascending=True
            ).reset_index()

            return df

        def get_candidate_wise_valid_vote_count_result(self, vote_type=None):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(float)

            df = df.loc[df['templateRowType'] == "CANDIDATE_FIRST_PREFERENCE"]

            if vote_type is not None:
                df = df.loc[df['voteType'] == vote_type]

            df = df.groupby(
                ['electionPartyId', 'partyId', 'partyName', 'partyAbbreviation', 'partySymbol', 'candidateId',
                 'candidateName', 'candidateNumber', 'candidateType']
            ).agg({
                'numValue': lambda x: x.sum(skipna=False),
                'incompleteNumValue': get_sum_of_numbers_only_and_nan_otherwise
            }).sort_values(
                by=['electionPartyId', 'partyId', 'candidateId'], ascending=True
            ).reset_index()

            return df

        def get_area_wise_valid_non_postal_vote_count_result(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(float)

            df = df.loc[
                (df['templateRowType'] == "CANDIDATE_FIRST_PREFERENCE") | (df['templateRowType'] == "PARTY_WISE_VOTE")]
            df = df.loc[df['voteType'] == NonPostal]

            df = df.groupby(
                ['areaId', "areaName"]
            ).agg({
                'numValue': lambda x: x.sum(skipna=False),
                'incompleteNumValue': get_sum_of_numbers_only_and_nan_otherwise
            }).sort_values(
                by=['areaId'], ascending=True
            ).reset_index()

            return df

        def get_area_wise_rejected_non_postal_vote_count_result(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(float)

            df = df.loc[df['templateRowType'] == "REJECTED_VOTE"]
            df = df.loc[df['voteType'] == NonPostal]

            df = df.groupby(
                ['areaId', "areaName"]
            ).agg({
                'numValue': lambda x: x.sum(skipna=False),
                'incompleteNumValue': get_sum_of_numbers_only_and_nan_otherwise
            }).sort_values(
                by=['areaId'], ascending=True
            ).reset_index()

            return df

        def get_area_wise_non_postal_vote_count_result(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(float)

            df = df.loc[df['voteType'] == NonPostal]

            df = df.groupby(
                ['areaId', "areaName"]
            ).agg({
                'numValue': lambda x: x.sum(skipna=False),
                'incompleteNumValue': get_sum_of_numbers_only_and_nan_otherwise
            }).sort_values(
                by=['areaId'], ascending=True
            ).reset_index()

            return df

        def get_non_postal_valid_vote_count_result(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(float)

            df = df.loc[df['templateRowType'] == "CANDIDATE_FIRST_PREFERENCE"]
            df = df.loc[df['voteType'] == NonPostal]

            df = df.groupby(lambda a: True).agg({
                'numValue': lambda x: x.sum(skipna=False),
                'incompleteNumValue': get_sum_of_numbers_only_and_nan_otherwise
            })

            return df

        def get_non_postal_rejected_vote_count_result(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(float)

            df = df.loc[df['templateRowType'] == "REJECTED_VOTE"]
            df = df.loc[df['voteType'] == NonPostal]

            df = df.groupby(lambda a: True).agg({
                'numValue': lambda x: x.sum(skipna=False),
                'incompleteNumValue': get_sum_of_numbers_only_and_nan_otherwise
            })

            return df

        def get_non_postal_vote_count_result(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(float)
            df = df.loc[df['voteType'] == NonPostal]

            df = df.groupby(lambda a: True).agg({
                'numValue': lambda x: x.sum(skipna=False),
                'incompleteNumValue': get_sum_of_numbers_only_and_nan_otherwise
            })

            return df

        def get_postal_valid_vote_count_result(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(float)

            df = df.loc[df['templateRowType'] == "CANDIDATE_FIRST_PREFERENCE"]
            df = df.loc[df['voteType'] == Postal]

            df = df.groupby(lambda a: True).agg({
                'numValue': lambda x: x.sum(skipna=False),
                'incompleteNumValue': get_sum_of_numbers_only_and_nan_otherwise
            })

            return df

        def get_party_wise_postal_valid_vote_count_result(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(float)

            df = df.loc[df['templateRowType'] == "PARTY_WISE_VOTE"]
            df = df.loc[df['voteType'] == Postal]

            df = df.groupby(lambda a: True).agg({
                'numValue': lambda x: x.sum(skipna=False),
                'incompleteNumValue': get_sum_of_numbers_only_and_nan_otherwise
            })

            return df

        def get_postal_rejected_vote_count_result(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(float)

            df = df.loc[df['templateRowType'] == "REJECTED_VOTE"]
            df = df.loc[df['voteType'] == Postal]

            df = df.groupby(lambda a: True).agg({
                'numValue': lambda x: x.sum(skipna=False),
                'incompleteNumValue': get_sum_of_numbers_only_and_nan_otherwise
            })

            return df

        def get_postal_vote_count_result(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(float)
            df = df.loc[df['voteType'] == Postal]

            df = df.groupby(lambda a: True).agg({
                'numValue': lambda x: x.sum(skipna=False),
                'incompleteNumValue': get_sum_of_numbers_only_and_nan_otherwise
            })

            return df

        def get_valid_vote_count_result(self, vote_type=None):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(float)

            if vote_type is not None:
                df = df.loc[df['voteType'] == vote_type]

            df = df.loc[
                (df['templateRowType'] == "CANDIDATE_FIRST_PREFERENCE") | (df['templateRowType'] == "PARTY_WISE_VOTE")]

            df = df.groupby(lambda a: True).agg({
                'numValue': lambda x: x.sum(skipna=False),
                'incompleteNumValue': get_sum_of_numbers_only_and_nan_otherwise
            })

            return df

        def get_rejected_vote_count_result(self, vote_type=None):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(float)

            if vote_type is not None:
                df = df.loc[df['voteType'] == vote_type]

            df = df.loc[df['templateRowType'] == "REJECTED_VOTE"]

            df = df.groupby(lambda a: True).agg({
                'numValue': lambda x: x.sum(skipna=False),
                'incompleteNumValue': get_sum_of_numbers_only_and_nan_otherwise
            })

            return df

        def get_vote_count_result(self, vote_type=None):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(float)

            if vote_type is not None:
                df = df.loc[df['voteType'] == vote_type]

            df = df.groupby(lambda a: True).agg({
                'numValue': lambda x: x.sum(skipna=False),
                'incompleteNumValue': get_sum_of_numbers_only_and_nan_otherwise
            })

            return df

        def get_candidate_and_area_wise_valid_vote_count_result(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(float)

            df = df.loc[df['templateRowType'] == "CANDIDATE_FIRST_PREFERENCE"]

            df = df.sort_values(
                by=['electionPartyId', 'partyId', 'partyName', 'partyAbbreviation', 'partySymbol', 'candidateId',
                    'candidateName', 'candidateNumber', 'candidateType', 'areaId', 'areaName'], ascending=True
            ).reset_index()

            return df

        def get_party_and_area_wise_valid_vote_count_result(self):
            df = self.df.copy()

            df = df.loc[df['templateRowType'] == "PARTY_WISE_VOTE"]

            df = df.sort_values(
                by=['electionPartyId', 'partyId', 'partyName', 'partyAbbreviation', 'partySymbol', 'areaId',
                    'areaName'], ascending=True
            ).reset_index()
            return df

        def get_area_wise_valid_vote_count_result(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(float)

            df = df.loc[
                (df['templateRowType'] == "CANDIDATE_FIRST_PREFERENCE") | (df['templateRowType'] == "PARTY_WISE_VOTE")]

            df = df.groupby(
                ['areaId', "areaName"]
            ).agg({
                'numValue': lambda x: x.sum(skipna=False),
                'incompleteNumValue': get_sum_of_numbers_only_and_nan_otherwise
            }).sort_values(
                by=['areaId'], ascending=True
            ).reset_index()

            return df

        def get_party_wise_valid_vote_count_result(self, vote_type=None):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(float)

            df = df.loc[df['templateRowType'] == "PARTY_WISE_VOTE"]

            if vote_type is not None:
                df = df.loc[df['voteType'] == vote_type]

            df = df.groupby(
                ['electionPartyId', 'partyId', 'partyName', 'partyAbbreviation', 'partySymbol']
            ).agg({
                'numValue': lambda x: x.sum(skipna=False),
                'incompleteNumValue': get_sum_of_numbers_only_and_nan_otherwise
            }).sort_values(
                by=['electionPartyId', 'partyId'], ascending=True
            ).reset_index()

            return df

        def get_area_wise_rejected_vote_count_result(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(float)

            df = df.loc[df['templateRowType'] == "REJECTED_VOTE"]

            df = df.groupby(
                ['areaId', "areaName"]
            ).agg({
                'numValue': lambda x: x.sum(skipna=False),
                'incompleteNumValue': get_sum_of_numbers_only_and_nan_otherwise
            }).sort_values(
                by=['areaId'], ascending=True
            ).reset_index()

            return df

        def get_area_wise_vote_count_result(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(float)

            df = df.loc[(df['templateRowType'] == "PARTY_WISE_VOTE") | (df['templateRowType'] == "REJECTED_VOTE")]

            df = df.groupby(
                ['areaId', "areaName"]
            ).agg({
                'numValue': lambda x: x.sum(skipna=False),
                'incompleteNumValue': get_sum_of_numbers_only_and_nan_otherwise
            }).sort_values(
                by=['areaId'], ascending=True
            ).reset_index()

            return df

        def get_polling_station_wise_number_of_ballots_recieved(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(float)
            df = df.loc[df['templateRowType'] == "NUMBER_OF_BALLOTS_RECEIVED"]

            df = df.groupby(
                ['areaId', "areaName"]
            ).agg({
                'numValue': lambda x: x.sum(skipna=False),
                'incompleteNumValue': get_sum_of_numbers_only_and_nan_otherwise
            }).sort_values(
                by=['areaId'], ascending=True
            ).reset_index()

            return df

        # def get_polling_station_wise_number_of_spoilt_ballot_papers(self):
        #     df = self.df.copy()
        #     df['numValue'] = df['numValue'].astype(float)
        #     df = df.loc[df['templateRowType'] == "NUMBER_OF_BALLOTS_SPOILT"]
        #
        #     df = df.groupby(
        #         ['areaId', "areaName"]
        #     ).agg({
        #         'numValue': lambda x: x.sum(skipna=False),
        #         'incompleteNumValue': get_sum_of_numbers_only_and_nan_otherwise
        #     }).sort_values(
        #         by=['areaId'], ascending=True
        #     ).reset_index()
        #
        #     return df
        #
        # def get_polling_station_wise_number_of_issued_ballot_papers(self):
        #     df = self.df.copy()
        #     df['numValue'] = df['numValue'].astype(float)
        #     df = df.loc[df['templateRowType'] == "NUMBER_OF_BALLOTS_ISSUED"]
        #
        #     df = df.groupby(
        #         ['areaId', "areaName"]
        #     ).agg({
        #         'numValue': lambda x: x.sum(skipna=False),
        #         'incompleteNumValue': get_sum_of_numbers_only_and_nan_otherwise
        #     }).sort_values(
        #         by=['areaId'], ascending=True
        #     ).reset_index()
        #
        #     return df
        #
        # def get_polling_station_wise_number_of_unused_ballot_papers(self):
        #     df = self.df.copy()
        #     df['numValue'] = df['numValue'].astype(float)
        #     df = df.loc[df['templateRowType'] == "NUMBER_OF_BALLOTS_UNUSED"]
        #
        #     df = df.groupby(
        #         ['areaId', "areaName"]
        #     ).agg({
        #         'numValue': lambda x: x.sum(skipna=False),
        #         'incompleteNumValue': get_sum_of_numbers_only_and_nan_otherwise
        #     }).sort_values(
        #         by=['areaId'], ascending=True
        #     ).reset_index()
        #
        #     return df
        #
        # def get_polling_station_wise_number_of_ordinary_ballots_in_ballot_paper_account(self):
        #     df = self.df.copy()
        #     df['numValue'] = df['numValue'].astype(float)
        #     df = df.loc[df['templateRowType'] == "NUMBER_OF_ORDINARY_BALLOTS_IN_BALLOT_PAPER_ACCOUNT"]
        #
        #     df = df.groupby(
        #         ['areaId', "areaName"]
        #     ).agg({
        #         'numValue': lambda x: x.sum(skipna=False),
        #         'incompleteNumValue': get_sum_of_numbers_only_and_nan_otherwise
        #     }).sort_values(
        #         by=['areaId'], ascending=True
        #     ).reset_index()
        #
        #     return df

        def get_polling_station_wise_number_of_ordinary_ballots_in_ballot_box(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(float)
            df = df.loc[df['templateRowType'] == "NUMBER_OF_ORDINARY_BALLOTS_IN_BALLOT_BOX"]

            df = df.groupby(
                ['areaId', "areaName"]
            ).agg({
                'numValue': lambda x: x.sum(skipna=False),
                'incompleteNumValue': get_sum_of_numbers_only_and_nan_otherwise
            }).sort_values(
                by=['areaId'], ascending=True
            ).reset_index()

            return df

        def get_invalid_vote_category_count(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(int)
            df = df.loc[df["templateRowType"] == "NUMBER_OF_VOTES_REJECTED_AGAINST_GROUNDS_FOR_REJECTION"]

            df = df.sort_values(
                by=['invalidVoteCategoryId'], ascending=True
            ).reset_index()

            return df

        def get_party_wise_invalid_vote_category_count(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(int)
            df = df.loc[df["templateRowType"] == "PARTY_WISE_INVALID_VOTE_COUNT"]

            df = df.sort_values(
                by=['invalidVoteCategoryId'], ascending=True
            ).reset_index()

            return df

        def get_time_of_commencement(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(int)
            df = df.loc[df["templateRowType"] == "TIME_OF_COMMENCEMENT"]

            return df

        def get_number_of_a_packets_found(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(int)
            df = df.loc[df["templateRowType"] == "NUMBER_OF_PACKETS_FOUND_INSIDE_BALLOT_BOX"]

            df = df.sort_values(
                by=['tallySheetVersionRowId'], ascending=True
            ).reset_index()

            return df

        def get_ballot_box_serial_number(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(int)
            df = df.loc[df["templateRowType"] == "BALLOT_BOX"]

            df = df.sort_values(
                by=['tallySheetVersionRowId'], ascending=True
            ).reset_index()

            return df

        def get_no_of_packets_inserted_to_ballot_box(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(int)
            df = df.loc[df["templateRowType"] == "NUMBER_OF_PACKETS_INSERTED_TO_BALLOT_BOX"]

            df = df.sort_values(
                by=['tallySheetVersionRowId'], ascending=True
            ).reset_index()

            return df

        def get_number_of_a_covers_rejected(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(int)
            df = df.loc[df["templateRowType"] == "NUMBER_OF_PACKETS_REJECTED_AFTER_OPENING_COVER_A"]

            return df

        def get_number_of_b_covers_rejected(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(int)
            df = df.loc[df["templateRowType"] == "NUMBER_OF_PACKETS_REJECTED_AFTER_OPENING_COVER_B"]

            return df


class ExtendedTallySheetDataEntry(ExtendedTallySheet):

    def on_workflow_tally_sheet_version(self, workflow_action, tallySheetVersionId, content=None):
        if workflow_action.actionType in [WORKFLOW_ACTION_TYPE_SUBMIT]:
            from orm.entities.SubmissionVersion import TallySheetVersion

            tally_sheet_version = db.session.query(
                TallySheetVersion.Model
            ).filter(
                TallySheetVersion.Model.tallySheetVersionId == tallySheetVersionId
            ).one_or_none()

            self.tallySheet.set_latest_version(tallySheetVersion=tally_sheet_version)

            return tally_sheet_version
        else:
            return super(ExtendedTallySheetDataEntry, self).on_workflow_tally_sheet_version(
                workflow_action=workflow_action, tallySheetVersionId=tallySheetVersionId, content=content)

    def on_before_workflow_action(self, workflow_action, tally_sheet_version):
        if workflow_action.actionType in [WORKFLOW_ACTION_TYPE_VERIFY]:
            if tally_sheet_version.createdBy == get_user_name():
                raise UnauthorizedException("You cannot verify the data last edited by yourself.",
                                            code=MESSAGE_CODE_TALLY_SHEET_NOT_AUTHORIZED_TO_VERIFY)

        if workflow_action.actionType in [WORKFLOW_ACTION_TYPE_SAVE, WORKFLOW_ACTION_TYPE_EDIT]:
            # To ignore the completion check
            pass
        else:
            return super(ExtendedTallySheetDataEntry, self).on_before_workflow_action(
                workflow_action=workflow_action, tally_sheet_version=tally_sheet_version)

    class ExtendedTallySheetVersion(ExtendedTallySheet.ExtendedTallySheetVersion):
        pass


class ExtendedTallySheetReport(ExtendedTallySheet):

    def on_workflow_tally_sheet_version(self, workflow_action, tallySheetVersionId, content=None):
        if workflow_action.actionType in [WORKFLOW_ACTION_TYPE_SAVE, WORKFLOW_ACTION_TYPE_VERIFY]:
            tally_sheet_version = self.on_tally_sheet_post()

            return tally_sheet_version
        else:
            return super(ExtendedTallySheetReport, self).on_workflow_tally_sheet_version(
                workflow_action=workflow_action, tallySheetVersionId=tallySheetVersionId, content=content)

    def on_before_workflow_action(self, workflow_action, tally_sheet_version):
        if workflow_action.actionType in [WORKFLOW_ACTION_TYPE_SAVE]:
            # To ignore the completion check
            pass
        else:
            return super(ExtendedTallySheetReport, self).on_before_workflow_action(
                workflow_action=workflow_action, tally_sheet_version=tally_sheet_version)

    def on_tally_sheet_get(self):
        if self.tallySheet.workflowInstance.status in [WORKFLOW_STATUS_TYPE_EMPTY, WORKFLOW_STATUS_TYPE_SAVED,
                                                       WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED]:
            # Create a version before it's fetched.
            self.on_tally_sheet_post()
            db.session.commit()

    class ExtendedTallySheetVersion(ExtendedTallySheet.ExtendedTallySheetVersion):
        pass


class ExtendedEditableTallySheetReport(ExtendedTallySheetDataEntry):

    def on_tally_sheet_get(self):
        if self.tallySheet.workflowInstance.status in [WORKFLOW_STATUS_TYPE_EMPTY, WORKFLOW_STATUS_TYPE_SAVED,
                                                       WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED]:
            # Create a version before it's fetched.
            self.on_tally_sheet_post()
            db.session.commit()

    class ExtendedTallySheetVersion(ExtendedTallySheetDataEntry.ExtendedTallySheetVersion):
        pass
