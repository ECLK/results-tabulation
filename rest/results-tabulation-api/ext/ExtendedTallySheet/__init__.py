import pandas as pd
from flask import render_template
from sqlalchemy import MetaData

from app import db
from auth import get_user_name
from constants.VOTE_TYPES import Postal, NonPostal
from exception import MethodNotAllowedException, UnauthorizedException
from ext.ExtendedElection.WORKFLOW_ACTION_TYPE import WORKFLOW_ACTION_TYPE_SAVE, WORKFLOW_ACTION_TYPE_VERIFY, \
    WORKFLOW_ACTION_TYPE_VIEW
from ext.ExtendedElection.WORKFLOW_STATUS_TYPE import WORKFLOW_STATUS_TYPE_EMPTY, WORKFLOW_STATUS_TYPE_SAVED, \
    WORKFLOW_STATUS_TYPE_CHANGES_REQUESTED

from orm.entities import Workflow, Meta
from orm.entities.Meta import MetaData
from orm.entities.Workflow import WorkflowInstance, WorkflowActionModel
from orm.entities.Workflow.WorkflowInstance import WorkflowInstanceLog
from util import to_comma_seperated_num, to_percentage, convert_image_to_data_uri

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

    def execute_workflow_action(self, workflowActionId, content=None):
        workflow_action = db.session.query(
            WorkflowActionModel
        ).filter(
            WorkflowActionModel.fromStatus == WorkflowInstance.Model.status,
            WorkflowInstance.Model.workflowInstanceId == self.tallySheet.workflowInstanceId,
            WorkflowActionModel.workflowActionId == workflowActionId
        ).one_or_none()

        self.authorize_workflow_action(workflow_action=workflow_action, content=content)

        tally_sheet_version = self.on_workflow_tally_sheet_version(workflow_action=workflow_action, content=content)

        self.on_before_workflow_action(workflow_action=workflow_action, tally_sheet_version=tally_sheet_version)

        self.on_workflow_action(workflow_action=workflow_action, content=content,
                                tally_sheet_version=tally_sheet_version)

        return self.tallySheet

    def authorize_workflow_action(self, workflow_action, content=None):
        from auth import has_role_based_access

        if not has_role_based_access(self.tallySheet, workflow_action.actionType):
            UnauthorizedException(message="Not allowed to %s" % (workflow_action.actionName))

    def on_workflow_tally_sheet_version(self, workflow_action, content=None):
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
            raise MethodNotAllowedException(message="Incomplete tally sheet.")

    def on_workflow_action(self, workflow_action, tally_sheet_version, content=None):
        self.tallySheet.workflowInstance.execute_action(
            action=workflow_action,
            meta=Meta.create({
                "tallySheetVersionId": tally_sheet_version.tallySheetVersionId
            })
        )

        return self.tallySheet

    def execute_tally_sheet_get(self):
        workflow_actions = self.on_before_tally_sheet_get()
        self.on_tally_sheet_get()
        self.on_after_tally_sheet_get(workflow_actions=workflow_actions)

        return self.tallySheet

    def on_before_tally_sheet_get(self):
        workflow_actions = self._get_allowed_workflow_actions(workflow_action_type=WORKFLOW_ACTION_TYPE_VIEW)

        if len(workflow_actions) == 0:
            raise MethodNotAllowedException(message="Tally sheet is longer readable.")

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

        return workflow_actions

    def on_before_tally_sheet_post(self):
        workflow_actions = self._get_allowed_workflow_actions(workflow_action_type=WORKFLOW_ACTION_TYPE_SAVE)

        if len(workflow_actions) == 0:
            raise MethodNotAllowedException(message="Tally sheet is longer editable.")

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

        def get_post_save_request_content(self):
            return []

        def html_letter(self, title="", total_registered_voters=None):
            tallySheetVersion = self.tallySheetVersion
            stamp = tallySheetVersion.stamp

            if total_registered_voters is None:
                total_registered_voters = float(tallySheetVersion.submission.area.registeredVotersCount)

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
                by=['partyId', 'partyName', 'partyAbbreviation', 'partySymbol', 'candidateId', 'candidateName',
                    'candidateNumber', 'areaId', 'areaName'], ascending=True
            ).reset_index()

            return df

        def get_party_and_area_wise_valid_non_postal_vote_count_result(self):
            df = self.df.copy()

            df = df.loc[df['templateRowType'] == "PARTY_WISE_VOTE"]
            df = df.loc[df['voteType'] == NonPostal]

            df = df.sort_values(
                by=['partyId', 'partyName', 'partyAbbreviation', 'partySymbol', 'areaId', 'areaName'], ascending=True
            ).reset_index()

            return df

        def get_candidate_wise_valid_non_postal_vote_count_result(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(float)

            df = df.loc[df['templateRowType'] == "CANDIDATE_FIRST_PREFERENCE"]
            df = df.loc[df['voteType'] == NonPostal]

            df = df.groupby(
                ['partyId', 'partyName', 'partyAbbreviation', 'partySymbol', 'candidateId', 'candidateName',
                 'candidateNumber']
            ).agg({
                'numValue': lambda x: x.sum(skipna=False),
                'incompleteNumValue': lambda x: x.sum(skipna=True)
            }).sort_values(
                by=['partyId', 'candidateId'], ascending=True
            ).reset_index()

            return df

        def get_candidate_wise_valid_postal_vote_count_result(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(float)

            df = df.loc[df['templateRowType'] == "CANDIDATE_FIRST_PREFERENCE"]
            df = df.loc[df['voteType'] == Postal]

            df = df.groupby(
                ['partyId', 'partyName', 'partyAbbreviation', 'partySymbol', 'candidateId', 'candidateName',
                 'candidateNumber']
            ).agg({
                'numValue': lambda x: x.sum(skipna=False),
                'incompleteNumValue': lambda x: x.sum(skipna=True)
            }).sort_values(
                by=['partyId', 'candidateId'], ascending=True
            ).reset_index()

            return df

        def get_party_wise_valid_postal_vote_count_result(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(float)

            df = df.loc[df['templateRowType'] == "PARTY_WISE_VOTE"]
            df = df.loc[df['voteType'] == Postal]

            df = df.groupby(
                ['partyId', 'partyName', 'partyAbbreviation', 'partySymbol']
            ).agg({
                'numValue': lambda x: x.sum(skipna=False),
                'incompleteNumValue': lambda x: x.sum(skipna=True)
            }).sort_values(
                by=['partyId'], ascending=True
            ).reset_index()

            return df

        def get_candidate_wise_valid_vote_count_result(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(float)

            df = df.loc[df['templateRowType'] == "CANDIDATE_FIRST_PREFERENCE"]

            df = df.groupby(
                ['partyId', 'partyName', 'partyAbbreviation', 'partySymbol', 'candidateId', 'candidateName',
                 'candidateNumber']
            ).agg({
                'numValue': lambda x: x.sum(skipna=False),
                'incompleteNumValue': lambda x: x.sum(skipna=True)
            }).sort_values(
                by=['partyId', 'candidateId'], ascending=True
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
                'incompleteNumValue': lambda x: x.sum(skipna=True)
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
                'incompleteNumValue': lambda x: x.sum(skipna=True)
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
                'incompleteNumValue': lambda x: x.sum(skipna=True)
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
                'incompleteNumValue': lambda x: x.sum(skipna=True)
            })

            return df

        def get_non_postal_rejected_vote_count_result(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(float)

            df = df.loc[df['templateRowType'] == "REJECTED_VOTE"]
            df = df.loc[df['voteType'] == NonPostal]

            df = df.groupby(lambda a: True).agg({
                'numValue': lambda x: x.sum(skipna=False),
                'incompleteNumValue': lambda x: x.sum(skipna=True)
            })

            return df

        def get_non_postal_vote_count_result(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(float)
            df = df.loc[df['voteType'] == NonPostal]

            df = df.groupby(lambda a: True).agg({
                'numValue': lambda x: x.sum(skipna=False),
                'incompleteNumValue': lambda x: x.sum(skipna=True)
            })

            return df

        def get_postal_valid_vote_count_result(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(float)

            df = df.loc[df['templateRowType'] == "CANDIDATE_FIRST_PREFERENCE"]
            df = df.loc[df['voteType'] == Postal]

            df = df.groupby(lambda a: True).agg({
                'numValue': lambda x: x.sum(skipna=False),
                'incompleteNumValue': lambda x: x.sum(skipna=True)
            })

            return df

        def get_party_wise_postal_valid_vote_count_result(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(float)

            df = df.loc[df['templateRowType'] == "PARTY_WISE_VOTE"]
            df = df.loc[df['voteType'] == Postal]

            df = df.groupby(lambda a: True).agg({
                'numValue': lambda x: x.sum(skipna=False),
                'incompleteNumValue': lambda x: x.sum(skipna=True)
            })

            return df

        def get_postal_rejected_vote_count_result(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(float)

            df = df.loc[df['templateRowType'] == "REJECTED_VOTE"]
            df = df.loc[df['voteType'] == Postal]

            df = df.groupby(lambda a: True).agg({
                'numValue': lambda x: x.sum(skipna=False),
                'incompleteNumValue': lambda x: x.sum(skipna=True)
            })

            return df

        def get_postal_vote_count_result(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(float)
            df = df.loc[df['voteType'] == Postal]

            df = df.groupby(lambda a: True).agg({
                'numValue': lambda x: x.sum(skipna=False),
                'incompleteNumValue': lambda x: x.sum(skipna=True)
            })

            return df

        def get_valid_vote_count_result(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(float)

            df = df.loc[
                (df['templateRowType'] == "CANDIDATE_FIRST_PREFERENCE") | (df['templateRowType'] == "PARTY_WISE_VOTE")]

            df = df.groupby(lambda a: True).agg({
                'numValue': lambda x: x.sum(skipna=False),
                'incompleteNumValue': lambda x: x.sum(skipna=True)
            })

            return df

        def get_rejected_vote_count_result(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(float)

            df = df.loc[df['templateRowType'] == "REJECTED_VOTE"]

            df = df.groupby(lambda a: True).agg({
                'numValue': lambda x: x.sum(skipna=False),
                'incompleteNumValue': lambda x: x.sum(skipna=True)
            })

            return df

        def get_vote_count_result(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(float)

            df = df.groupby(lambda a: True).agg({
                'numValue': lambda x: x.sum(skipna=False),
                'incompleteNumValue': lambda x: x.sum(skipna=True)
            })

            return df

        def get_candidate_and_area_wise_valid_vote_count_result(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(float)

            df = df.loc[df['templateRowType'] == "CANDIDATE_FIRST_PREFERENCE"]

            df = df.sort_values(
                by=['partyId', 'partyName', 'partyAbbreviation', 'partySymbol', 'candidateId', 'candidateName',
                    'candidateNumber', 'areaId', 'areaName'], ascending=True
            ).reset_index()

            return df

        def get_party_and_area_wise_valid_vote_count_result(self):
            df = self.df.copy()

            df = df.loc[df['templateRowType'] == "PARTY_WISE_VOTE"]

            df = df.sort_values(
                by=['partyId', 'partyName', 'partyAbbreviation', 'partySymbol', 'areaId', 'areaName'], ascending=True
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
                'incompleteNumValue': lambda x: x.sum(skipna=True)
            }).sort_values(
                by=['areaId'], ascending=True
            ).reset_index()

            return df

        def get_party_wise_valid_vote_count_result(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(float)

            df = df.loc[df['templateRowType'] == "PARTY_WISE_VOTE"]

            df = df.groupby(
                ['partyId', 'partyName', 'partyAbbreviation', 'partySymbol']
            ).agg({
                'numValue': lambda x: x.sum(skipna=False),
                'incompleteNumValue': lambda x: x.sum(skipna=True)
            }).sort_values(
                by=['partyId'], ascending=True
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
                'incompleteNumValue': lambda x: x.sum(skipna=True)
            }).sort_values(
                by=['areaId'], ascending=True
            ).reset_index()

            return df

        def get_area_wise_vote_count_result(self):
            df = self.df.copy()
            df['numValue'] = df['numValue'].astype(float)

            df = df.groupby(
                ['areaId', "areaName"]
            ).agg({
                'numValue': lambda x: x.sum(skipna=False),
                'incompleteNumValue': lambda x: x.sum(skipna=True)
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
                'incompleteNumValue': lambda x: x.sum(skipna=True)
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
        #         'incompleteNumValue': lambda x: x.sum(skipna=True)
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
        #         'incompleteNumValue': lambda x: x.sum(skipna=True)
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
        #         'incompleteNumValue': lambda x: x.sum(skipna=True)
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
        #         'incompleteNumValue': lambda x: x.sum(skipna=True)
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
                'incompleteNumValue': lambda x: x.sum(skipna=True)
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


class ExtendedTallySheetDataEntry(ExtendedTallySheet):
    def on_before_workflow_action(self, workflow_action, tally_sheet_version):
        if workflow_action.actionType in [WORKFLOW_ACTION_TYPE_VERIFY]:
            if tally_sheet_version.createdBy == get_user_name():
                raise UnauthorizedException("You cannot very the data last edited by yourself.")

        return super(ExtendedTallySheetDataEntry, self).on_before_workflow_action(
            workflow_action=workflow_action, tally_sheet_version=tally_sheet_version)

    class ExtendedTallySheetVersion(ExtendedTallySheet.ExtendedTallySheetVersion):
        pass


class ExtendedTallySheetReport(ExtendedTallySheet):

    def on_workflow_tally_sheet_version(self, workflow_action, content=None):
        if workflow_action.actionType in [WORKFLOW_ACTION_TYPE_SAVE, WORKFLOW_ACTION_TYPE_VERIFY]:
            tally_sheet_version = self.on_tally_sheet_post()

            return tally_sheet_version
        else:
            return super(ExtendedTallySheetReport, self).on_workflow_tally_sheet_version(
                workflow_action=workflow_action, content=content)

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
