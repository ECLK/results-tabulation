from api import ProofApi, FileApi
from app import db
from auth import authorize, has_role_based_access
from constants.AUTH_CONSTANTS import ALL_ROLES
from exception import NotFoundException
from exception.messages import MESSAGE_CODE_TALLY_SHEET_NOT_FOUND
from ext.ExtendedTallySheet import ExtendedTallySheet
from orm.entities.Submission import TallySheet
from schemas import TallySheetSchema, TallySheetSchema_1, WorkflowInstanceLogSchema
from util import RequestBody


@authorize(required_roles=ALL_ROLES)
def getAll(electionId=None, areaId=None, tallySheetCode=None, voteType=None):
    tally_sheets = TallySheet.get_all(
        electionId=electionId,
        areaId=areaId,
        tallySheetCode=tallySheetCode,
        voteType=voteType
    )

    tally_sheets = [refactor_tally_sheet_response(tally_sheet) for tally_sheet in tally_sheets]

    return TallySheetSchema(many=True).dump(tally_sheets).data


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

    return TallySheetSchema_1().dump(refactor_tally_sheet_response(tally_sheet)).data


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

    return TallySheetSchema_1().dump(refactor_tally_sheet_response(tally_sheet)).data


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

    return TallySheetSchema_1().dump(refactor_tally_sheet_response(tally_sheet)).data


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


def refactor_tally_sheet_response(tally_sheet):
    print("status ", tally_sheet.workflowInstance.status)
    workflow_instance = tally_sheet.workflowInstance
    workflow_actions = tally_sheet.workflowInstance.workflow.actions

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
            "authorized": has_role_based_access(tally_sheet=tally_sheet,
                                                access_type=workflow_action.actionType)
        })

    setattr(tally_sheet.workflowInstance, "actions", workflow_action_dict_list)
    setattr(tally_sheet, "areaId", tally_sheet.submission.areaId)
    setattr(tally_sheet, "area", tally_sheet.submission.area)

    return tally_sheet
