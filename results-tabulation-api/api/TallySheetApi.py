from api import ProofApi, FileApi, TallySheetVersionApi
from app import db, cache
from auth import authorize, has_role_based_access, get_user_access_area_ids
from constants.AUTH_CONSTANTS import ALL_ROLES
from exception import NotFoundException
from exception.messages import MESSAGE_CODE_TALLY_SHEET_NOT_FOUND
from ext.ExtendedTallySheet import ExtendedTallySheet
from orm.entities import Election, Submission
from orm.entities.Submission import TallySheet
from orm.entities.Workflow import WorkflowInstance
from schemas import TallySheetSchema_1, WorkflowInstanceLogSchema, WorkflowInstanceSchema
from util import RequestBody


@authorize(required_roles=ALL_ROLES)
def getAll(electionId=None, areaId=None, tallySheetCode=None, voteType=None, partyId=None, limit=None, offset=None):
    user_access_area_ids = get_user_access_area_ids()

    cached_tally_sheets = _cache_get_all(user_access_area_ids, electionId=electionId, areaId=areaId,
                                         tallySheetCode=tallySheetCode, voteType=voteType, partyId=partyId, limit=limit,
                                         offset=offset)

    _append_latest_workflow_instance_to_cached_tally_sheets(cached_tally_sheets=cached_tally_sheets)
    _append_latest_version_ids_to_cached_tally_sheets(cached_tally_sheets=cached_tally_sheets)

    return cached_tally_sheets


@cache.memoize()
def _cache_get_all(user_access_area_ids, electionId=None, areaId=None, tallySheetCode=None, voteType=None, partyId=None,
                   limit=None, offset=None):
    tally_sheets = TallySheet.get_all(
        electionId=electionId,
        areaId=areaId,
        tallySheetCode=tallySheetCode,
        voteType=voteType,
        partyId=partyId,
        limit=limit, offset=offset
    )

    tally_sheet_response_list = []
    for tally_sheet_index in range(len(tally_sheets)):
        tally_sheet = tally_sheets[tally_sheet_index]
        refactor_tally_sheet(tally_sheet)
        tally_sheet_response_list_item = dict(TallySheetSchema_1(only=[
            "tallySheetId",
            "tallySheetCode",
            "templateId",
            "template",
            "electionId",
            "areaId",
            "metaDataList",
            "workflowInstanceId"
        ]).dump(tally_sheet).data)
        tally_sheet_response_list.append(tally_sheet_response_list_item)

    return tally_sheet_response_list


@authorize(required_roles=ALL_ROLES)
def get_by_id(tallySheetId):
    tally_sheet = TallySheet.get_by_id(tallySheetId=tallySheetId)

    if tally_sheet is None:
        NotFoundException(
            message="Tally sheet not found (tallySheetId=%s)" % tallySheetId,
            code=MESSAGE_CODE_TALLY_SHEET_NOT_FOUND
        )

    extended_tally_sheet: ExtendedTallySheet = tally_sheet.get_extended_tally_sheet()
    extended_tally_sheet.execute_tally_sheet_get()

    tally_sheet_response = TallySheetSchema_1().dump(refactor_tally_sheet(tally_sheet)).data
    _append_latest_workflow_instance_to_cached_tally_sheets(cached_tally_sheets=[tally_sheet_response])
    _append_latest_version_ids_to_cached_tally_sheets(cached_tally_sheets=[tally_sheet_response])

    return tally_sheet_response


@authorize(required_roles=ALL_ROLES)
def workflow(tallySheetId, body):
    request_body = RequestBody(body)
    workflowActionId = request_body.get("workflowActionId")
    tallySheetVersionId = request_body.get("tallySheetVersionId")

    tally_sheet = TallySheet.get_by_id(tallySheetId=tallySheetId)

    if tally_sheet is None:
        raise NotFoundException("Tally sheet not found (tallySheetId=%d)" % tallySheetId,
                                code=MESSAGE_CODE_TALLY_SHEET_NOT_FOUND)

    extended_tally_sheet: ExtendedTallySheet = tally_sheet.get_extended_tally_sheet()
    extended_tally_sheet.execute_workflow_action(workflowActionId=workflowActionId,
                                                 tallySheetVersionId=tallySheetVersionId)

    db.session.commit()

    tally_sheet_response = TallySheetSchema_1().dump(refactor_tally_sheet(tally_sheet)).data
    _append_latest_workflow_instance_to_cached_tally_sheets(cached_tally_sheets=[tally_sheet_response])
    _append_latest_version_ids_to_cached_tally_sheets(cached_tally_sheets=[tally_sheet_response])

    return tally_sheet_response


@authorize(required_roles=ALL_ROLES)
def upload_workflow_proof_file(body):
    request_body = RequestBody(body)
    tallySheetId = request_body.get("tallySheetId")

    tally_sheet = TallySheet.get_by_id(tallySheetId=tallySheetId)

    if tally_sheet is None:
        raise NotFoundException("Tally sheet not found (tallySheetId=%d)" % tallySheetId,
                                code=MESSAGE_CODE_TALLY_SHEET_NOT_FOUND)

    body["proofId"] = tally_sheet.workflowInstance.proofId
    ProofApi.upload_file(body=body)

    extended_tally_sheet: ExtendedTallySheet = tally_sheet.get_extended_tally_sheet()
    extended_tally_sheet.execute_tally_sheet_proof_upload()

    tally_sheet_response = TallySheetSchema_1().dump(refactor_tally_sheet(tally_sheet)).data
    _append_latest_workflow_instance_to_cached_tally_sheets(cached_tally_sheets=[tally_sheet_response])
    _append_latest_version_ids_to_cached_tally_sheets(cached_tally_sheets=[tally_sheet_response])

    return tally_sheet_response


@authorize(required_roles=ALL_ROLES)
def get_workflow_logs(tallySheetId):
    tally_sheet = TallySheet.get_by_id(tallySheetId=tallySheetId)

    if tally_sheet is None:
        raise NotFoundException("Tally sheet not found (tallySheetId=%d)" % tallySheetId,
                                code=MESSAGE_CODE_TALLY_SHEET_NOT_FOUND)

    workflow_logs = tally_sheet.workflowInstance.logs

    return WorkflowInstanceLogSchema(many=True).dump(workflow_logs).data


@authorize(required_roles=ALL_ROLES)
def get_workflow_proof_file(tallySheetId, fileId):
    tally_sheet = TallySheet.get_by_id(tallySheetId=tallySheetId)

    if tally_sheet is None:
        raise NotFoundException("Tally sheet not found (tallySheetId=%d)" % tallySheetId,
                                code=MESSAGE_CODE_TALLY_SHEET_NOT_FOUND)

    # TODO validate fileId

    return FileApi.get_by_id(fileId=fileId)


@authorize(required_roles=ALL_ROLES)
def get_workflow_proof_inline_file(tallySheetId, fileId):
    tally_sheet = TallySheet.get_by_id(tallySheetId=tallySheetId)

    if tally_sheet is None:
        raise NotFoundException("Tally sheet not found (tallySheetId=%d)" % tallySheetId,
                                code=MESSAGE_CODE_TALLY_SHEET_NOT_FOUND)

    # TODO validate fileId

    return FileApi.get_inline_file(fileId=fileId)


@authorize(required_roles=ALL_ROLES)
def get_workflow_proof_download_file(tallySheetId, fileId):
    tally_sheet = TallySheet.get_by_id(tallySheetId=tallySheetId)

    if tally_sheet is None:
        raise NotFoundException("Tally sheet not found (tallySheetId=%d)" % tallySheetId,
                                code=MESSAGE_CODE_TALLY_SHEET_NOT_FOUND)

    # TODO validate fileId

    return FileApi.get_download_file(fileId=fileId)


def refactor_tally_sheet(tally_sheet):
    setattr(tally_sheet, "areaId", tally_sheet.submission.areaId)
    setattr(tally_sheet, "area", tally_sheet.submission.area)

    return tally_sheet


def _append_latest_version_ids_to_cached_tally_sheets(cached_tally_sheets):
    cached_tally_sheet_ids = [cached_tally_sheet["tallySheetId"] for cached_tally_sheet in cached_tally_sheets]

    tally_sheets = db.session.query(Submission.Model.submissionId.label("tallySheetId"),
                                    Submission.Model.latestVersionId).filter(
        Submission.Model.submissionId.in_(cached_tally_sheet_ids))
    tally_sheets_map = {tally_sheet.tallySheetId: tally_sheet for tally_sheet in tally_sheets}

    for cached_tally_sheet in cached_tally_sheets:
        cached_tally_sheet["latestVersionId"] = tally_sheets_map[cached_tally_sheet["tallySheetId"]].latestVersionId


def _append_latest_version_to_cached_tally_sheet(cached_tally_sheet):
    latest_tally_sheet_version_id = cached_tally_sheet["latestVersionId"]
    if latest_tally_sheet_version_id is not None:
        cached_tally_sheet["latestVersion"] = TallySheetVersionApi.get_by_id(
            tallySheetId=cached_tally_sheet["tallySheetId"], tallySheetVersionId=latest_tally_sheet_version_id)
    else:
        cached_tally_sheet["latestVersion"] = None

    return cached_tally_sheet


def _append_latest_workflow_instance_to_cached_tally_sheets(cached_tally_sheets):
    cached_tally_sheet_ids = [cached_tally_sheet["tallySheetId"] for cached_tally_sheet in cached_tally_sheets]

    tally_sheet_workflow_instances = WorkflowInstance.Model.query.filter(
        WorkflowInstance.Model.workflowInstanceId == TallySheet.Model.workflowInstanceId,
        TallySheet.Model.tallySheetId.in_(cached_tally_sheet_ids)
    ).all()
    tally_sheet_workflow_instances_map = {
        tally_sheet_workflow_instance.workflowInstanceId: tally_sheet_workflow_instance for
        tally_sheet_workflow_instance in tally_sheet_workflow_instances}

    tally_sheet_elections = db.session.query(
        Election.Model.electionId, Election.Model.electionTemplateName, Election.Model.voteType
    ).filter(Election.Model.electionId == Submission.Model.electionId,
             Submission.Model.submissionId.in_(cached_tally_sheet_ids)).all()
    tally_sheet_elections_map = {tally_sheet_election.electionId: tally_sheet_election for tally_sheet_election in
                                 tally_sheet_elections}

    for tally_sheet_index in range(len(cached_tally_sheet_ids)):
        cached_tally_sheet = cached_tally_sheets[tally_sheet_index]
        tally_sheet_workflow_instance_id = cached_tally_sheet["workflowInstanceId"]

        workflow_instance = tally_sheet_workflow_instances_map[tally_sheet_workflow_instance_id]
        workflow_actions = workflow_instance.workflow.actions

        # Convert the actions list to a list of dictionary objects due to following issue
        # https://github.com/ECLK/results-tabulation/issues/708
        workflow_action_dict_list = []
        for workflow_action in workflow_actions:
            workflow_action_dict_list.append({
                "workflowActionId": workflow_action.workflowActionId,
                "actionName": workflow_action.actionName,
                "actionType": workflow_action.actionType,
                "fromStatus": workflow_action.fromStatus,
                "toStatus": workflow_action.toStatus,
                "allowed": workflow_action.fromStatus == workflow_instance.status,
                "authorized": has_role_based_access(
                    election=tally_sheet_elections_map[cached_tally_sheet["electionId"]],
                    tally_sheet_code=cached_tally_sheet["tallySheetCode"],
                    access_type=workflow_action.actionType)
            })

        setattr(workflow_instance, "actions", workflow_action_dict_list)
        cached_tally_sheet["workflowInstance"] = WorkflowInstanceSchema().dump(workflow_instance).data

    return cached_tally_sheets
