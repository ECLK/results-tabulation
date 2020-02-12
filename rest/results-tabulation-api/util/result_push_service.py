from exception import MethodNotAllowedException
from exception.messages import MESSAGE_CODE_TALLY_SHEET_NOT_ALLOWED_TO_BE_RELEASED, \
    MESSAGE_CODE_TALLY_SHEET_NOT_ALLOWED_TO_BE_NOTIFIED
from orm.entities.SubmissionVersion import TallySheetVersion
import requests
from app import connex_app
from ext.ExtendedElection.ExtendedElectionPresidentialElection2019.TALLY_SHEET_CODES import PRE_30_PD, PRE_30_ED, \
    PRE_ALL_ISLAND_RESULTS, PRE_34_PD, PRE_34_ED, PRE_34_AI

RESULT_DISSEMINATION_SYSTEM_URL = connex_app.app.config['RESULT_DISSEMINATION_SYSTEM_URL']
RESULT_DISSEMINATION_SYSTEM_ELECTION_CODE = connex_app.app.config['RESULT_DISSEMINATION_SYSTEM_ELECTION_CODE']
RESULT_DISSEMINATION_SYSTEM_RESULT_TYPE_VOTE = connex_app.app.config['RESULT_DISSEMINATION_SYSTEM_RESULT_TYPE_VOTE']
RESULT_DISSEMINATION_SYSTEM_RESULT_TYPE_PREF = connex_app.app.config['RESULT_DISSEMINATION_SYSTEM_RESULT_TYPE_PREF']

RELEASE_RESULTS_ENDPOINT = "result/data"

NOTIFY_RESULTS_ENDPOINT = "result/notification"
RESULTS_PROOF_IMAGE_UPLOAD_ENDPOINT = "result/image"

release_allowed_tally_sheet_codes = [
    PRE_30_PD,
    PRE_30_ED,
    PRE_ALL_ISLAND_RESULTS,
    PRE_34_PD,
    PRE_34_ED,
    PRE_34_AI
]

notify_allowed_tally_sheet_codes = [
    PRE_30_PD,
    PRE_30_ED,
    PRE_ALL_ISLAND_RESULTS,
    PRE_34_PD,
    PRE_34_ED,
    PRE_34_AI
]

RESULT_LEVEL_NATIONAL_FINAL = "NATIONAL-FINAL"
RESULT_LEVEL_ELECTORAL_DISTRICT = "ELECTORAL-DISTRICT"
RESULT_LEVEL_POLLING_DIVISION = "POLLING-DIVISION"

PARAM_ED_NAME = "ed_name"
PARAM_PD_NAME = "pd_name"

tally_sheet_code_result_level = {

}


def get_result_level(tally_sheet):
    if tally_sheet.tallySheetCode in [PRE_34_AI, PRE_ALL_ISLAND_RESULTS]:
        return RESULT_LEVEL_NATIONAL_FINAL
    elif tally_sheet.tallySheetCode in [
        PRE_30_PD, PRE_34_PD
    ]:
        return RESULT_LEVEL_POLLING_DIVISION
    else:
        return RESULT_LEVEL_ELECTORAL_DISTRICT


def upload_proof_last_image(tally_sheet, tally_sheet_version):
    if tally_sheet.tallySheetCode in release_allowed_tally_sheet_codes:
        response, result_code = tally_sheet_version.json_data()

        result_dissemination_result_type = RESULT_DISSEMINATION_SYSTEM_RESULT_TYPE_VOTE
        # if tally_sheet.tallySheetCode in PREFERENCE_TALLY_SHEET_CODES:
        #     result_dissemination_result_type = RESULT_DISSEMINATION_SYSTEM_RESULT_TYPE_PREF

        response['type'] = result_dissemination_result_type

        url = "%s/%s/%s/%s" % (
            RESULT_DISSEMINATION_SYSTEM_URL,
            RESULTS_PROOF_IMAGE_UPLOAD_ENDPOINT,
            RESULT_DISSEMINATION_SYSTEM_ELECTION_CODE,
            result_code
        )

        files = tally_sheet.submissionProof.scannedFiles
        last_file = files[len(files) - 1]

        last_file_data = last_file.fileContent

        print("#### RESULT_DISSEMINATION_API - Image Upload #### ", [url, response, last_file_data])

        result = requests.post(
            url=url,
            data=last_file_data,
            headers={'Content-Type': last_file.fileContentType}
        )
        print(result.status_code, result.content)
        return result
    else:
        raise MethodNotAllowedException(
            message="Tally sheet is not allowed to be released.",
            code=MESSAGE_CODE_TALLY_SHEET_NOT_ALLOWED_TO_BE_RELEASED
        )


def release_results(tally_sheet, tally_sheet_version_id):
    if tally_sheet.tallySheetCode in release_allowed_tally_sheet_codes:
        tally_sheet_version = TallySheetVersion.get_by_id(
            tallySheetId=tally_sheet.tallySheetId,
            tallySheetVersionId=tally_sheet_version_id
        )
        response, result_code = tally_sheet_version.json_data()

        result_dissemination_result_type = RESULT_DISSEMINATION_SYSTEM_RESULT_TYPE_VOTE
        # if tally_sheet.tallySheetCode in PREFERENCE_TALLY_SHEET_CODES:
        #     result_dissemination_result_type = RESULT_DISSEMINATION_SYSTEM_RESULT_TYPE_PREF

        response['type'] = result_dissemination_result_type

        url = "%s/%s/%s/%s/%s" % (
            RESULT_DISSEMINATION_SYSTEM_URL,
            RELEASE_RESULTS_ENDPOINT,
            RESULT_DISSEMINATION_SYSTEM_ELECTION_CODE,
            result_dissemination_result_type,
            result_code
        )

        print("#### RESULT_DISSEMINATION_API - Release #### ", [url, response])
        result = requests.post(url, verify=False, json=response)
        print(result.status_code, result.content)

        upload_proof_last_image(tally_sheet, tally_sheet_version)

        return result
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
        response, result_code = tally_sheet_version.json_data()

        result_dissemination_result_type = RESULT_DISSEMINATION_SYSTEM_RESULT_TYPE_VOTE
        # if tally_sheet.tallySheetCode in PREFERENCE_TALLY_SHEET_CODES:
        #     result_dissemination_result_type = RESULT_DISSEMINATION_SYSTEM_RESULT_TYPE_PREF

        response['type'] = result_dissemination_result_type

        url = "%s/%s/%s/%s/%s" % (
            RESULT_DISSEMINATION_SYSTEM_URL,
            NOTIFY_RESULTS_ENDPOINT,
            RESULT_DISSEMINATION_SYSTEM_ELECTION_CODE,
            result_dissemination_result_type,
            result_code
        )

        params = {
            "level": get_result_level(tally_sheet),
        }

        required_params_from_response = [PARAM_ED_NAME, PARAM_PD_NAME]
        for required_param in required_params_from_response:
            if required_param in response:
                params[required_param] = response[required_param]

        print("#### RESULT_DISSEMINATION_API - Notify #### ", [url, response, params])
        result = requests.post(url, verify=False, params=params)
        print(result.status_code, result.content)
        return result
    else:
        raise MethodNotAllowedException(
            message="Tally sheet is not allowed to be notified.",
            code=MESSAGE_CODE_TALLY_SHEET_NOT_ALLOWED_TO_BE_NOTIFIED
        )
