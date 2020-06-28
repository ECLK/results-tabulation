from api import ProofApi, FileApi
from app import db
from auth import authorize
from constants.AUTH_CONSTANTS import ALL_ROLES
from exception import NotFoundException
from exception.messages import MESSAGE_CODE_TALLY_SHEET_NOT_FOUND
from ext.ExtendedTallySheet import ExtendedTallySheet
from orm.entities.Submission import TallySheet
from schemas import TallySheetSchema, TallySheetSchema_1, WorkflowInstanceLogSchema
from util import RequestBody


@authorize(required_roles=ALL_ROLES)
def getAll(electionId=None, areaId=None, tallySheetCode=None, voteType=None):
    result = TallySheet.get_all(
        electionId=electionId,
        areaId=areaId,
        tallySheetCode=tallySheetCode,
        voteType=voteType
    )

    # result = get_paginated_query(result).all()

    return TallySheetSchema(many=True).dump(result).data


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

    return TallySheetSchema_1().dump(tally_sheet).data


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

    return TallySheetSchema_1().dump(tally_sheet).data


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

    return TallySheetSchema_1().dump(tally_sheet).data


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
