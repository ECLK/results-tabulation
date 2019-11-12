from exception import MethodNotAllowedException
from exception.messages import MESSAGE_CODE_TALLY_SHEET_NOT_ALLOWED_TO_BE_RELEASED, \
    MESSAGE_CODE_TALLY_SHEET_NOT_ALLOWED_TO_BE_NOTIFIED
from orm.entities.Submission.TallySheet import PREFERENCE_TALLY_SHEET_CODES
from orm.entities.SubmissionVersion import TallySheetVersion
from orm.enums import TallySheetCodeEnum
import requests
from app import connex_app

RESULT_DISSEMINATION_SYSTEM_URL = connex_app.app.config['RESULT_DISSEMINATION_SYSTEM_URL']
RESULT_DISSEMINATION_SYSTEM_ELECTION_CODE = connex_app.app.config['RESULT_DISSEMINATION_SYSTEM_ELECTION_CODE']
RESULT_DISSEMINATION_SYSTEM_RESULT_TYPE_VOTE = connex_app.app.config['RESULT_DISSEMINATION_SYSTEM_RESULT_TYPE_VOTE']
RESULT_DISSEMINATION_SYSTEM_RESULT_TYPE_PREF = connex_app.app.config['RESULT_DISSEMINATION_SYSTEM_RESULT_TYPE_PREF']

RELEASE_RESULTS_ENDPOINT = "result/data"
NOTIFY_RESULTS_ENDPOINT = "result/notification"

release_allowed_tally_sheet_codes = [
    TallySheetCodeEnum.PRE_30_PD,
    TallySheetCodeEnum.PRE_30_ED,
    TallySheetCodeEnum.PRE_ALL_ISLAND_RESULTS,
    TallySheetCodeEnum.PRE_34_PD,
    TallySheetCodeEnum.PRE_34_ED,
    TallySheetCodeEnum.PRE_34_AI
]

notify_allowed_tally_sheet_codes = [
    TallySheetCodeEnum.PRE_30_PD,
    TallySheetCodeEnum.PRE_30_ED,
    TallySheetCodeEnum.PRE_ALL_ISLAND_RESULTS,
    TallySheetCodeEnum.PRE_34_PD,
    TallySheetCodeEnum.PRE_34_ED,
    TallySheetCodeEnum.PRE_34_AI
]


def release_results(tally_sheet, tally_sheet_version_id):
    if tally_sheet.tallySheetCode in release_allowed_tally_sheet_codes:
        tally_sheet_version = TallySheetVersion.get_by_id(
            tallySheetId=tally_sheet.tallySheetId,
            tallySheetVersionId=tally_sheet_version_id
        )
        response = tally_sheet_version.json_data()

        result_dissemination_result_type = RESULT_DISSEMINATION_SYSTEM_RESULT_TYPE_VOTE
        if tally_sheet.tallySheetCode in PREFERENCE_TALLY_SHEET_CODES:
            result_dissemination_result_type = RESULT_DISSEMINATION_SYSTEM_RESULT_TYPE_PREF

        response['type'] = result_dissemination_result_type

        url = "%s/%s/%s/%s/%s" % (
            RESULT_DISSEMINATION_SYSTEM_URL,
            RELEASE_RESULTS_ENDPOINT,
            RESULT_DISSEMINATION_SYSTEM_ELECTION_CODE,
            result_dissemination_result_type,
            response['result_code']
        )

        print("#### RESULT_DISSEMINATION_API - Release #### ", [url, response])
        return requests.post(url, verify=False, json=response)
    else:
        raise MethodNotAllowedException(
            message="Tally sheet is not allowed to be released.",
            code=MESSAGE_CODE_TALLY_SHEET_NOT_ALLOWED_TO_BE_RELEASED
        )


def notify_results(tally_sheet, tally_sheet_version_id):
    if tally_sheet.tallySheetCode in notify_allowed_tally_sheet_codes:
        tally_sheet_version = TallySheetVersion.get_by_id(
            tallySheetId=tally_sheet.tallySheetId,
            tallySheetVersionId=tally_sheet_version_id
        )
        response = tally_sheet_version.json_data()

        result_dissemination_result_type = RESULT_DISSEMINATION_SYSTEM_RESULT_TYPE_VOTE
        if tally_sheet.tallySheetCode in PREFERENCE_TALLY_SHEET_CODES:
            result_dissemination_result_type = RESULT_DISSEMINATION_SYSTEM_RESULT_TYPE_PREF

        response['type'] = result_dissemination_result_type

        url = "%s/%s/%s/%s" % (
            RESULT_DISSEMINATION_SYSTEM_URL,
            NOTIFY_RESULTS_ENDPOINT,
            RESULT_DISSEMINATION_SYSTEM_ELECTION_CODE,
            # result_dissemination_result_type,
            response['result_code']
        )

        print("#### RESULT_DISSEMINATION_API - Notify #### ", [url, response])
        return requests.post(url, verify=False)
    else:
        raise MethodNotAllowedException(
            message="Tally sheet is not allowed to be notified.",
            code=MESSAGE_CODE_TALLY_SHEET_NOT_ALLOWED_TO_BE_NOTIFIED
        )
