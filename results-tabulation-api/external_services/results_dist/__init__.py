from app import connex_app
from exception.messages import MESSAGE_RESULTS_DIST_RELEASE_FAILED, MESSAGE_RESULTS_DIST_RELEASE_NOTIFICATION_FAILED
from exception import InternalServerErrorException
import requests
import traceback


def release_result(result_type, result_code, data):
    try:
        response = requests.request(
            method="POST",
            url="%s/result/data/%s/%s/%s" % (
                connex_app.app.config['RESULT_DISSEMINATION_SYSTEM_URL'],
                connex_app.app.config['RESULT_DISSEMINATION_SYSTEM_ELECTION_CODE'],
                result_type, result_code
            ),
            headers={'Content-Type': 'application/json'},
            data=str(data),
            timeout=300
        )

        if response.status_code != 202:
            raise InternalServerErrorException(
                message="Results releasing failed.",
                code=MESSAGE_RESULTS_DIST_RELEASE_FAILED
            )
    except Exception as e:
        error_string = traceback.format_exc()
        print(error_string)

        raise InternalServerErrorException(
            message="Results releasing request failed.",
            code=MESSAGE_RESULTS_DIST_RELEASE_FAILED
        )


def notify_release_result(result_type, result_code, data):
    try:
        response = requests.request(
            method="POST",
            url="%s/result/notification/%s/%s/%s" % (
                connex_app.app.config['RESULT_DISSEMINATION_SYSTEM_URL'],
                connex_app.app.config['RESULT_DISSEMINATION_SYSTEM_ELECTION_CODE'],
                result_type, result_code
            ),
            headers={'Content-Type': 'application/json'},
            timeout=300
        )

        if response.status_code != 200:
            raise InternalServerErrorException(
                message="Results release notification failed.",
                code=MESSAGE_RESULTS_DIST_RELEASE_NOTIFICATION_FAILED
            )
    except Exception as e:
        error_string = traceback.format_exc()
        print(error_string)

        raise InternalServerErrorException(
            message="Results release notification request failed.",
            code=MESSAGE_RESULTS_DIST_RELEASE_NOTIFICATION_FAILED
        )
