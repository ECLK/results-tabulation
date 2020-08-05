from app import connex_app
from exception.messages import MESSAGE_RESULTS_DIST_RELEASE_FAILED, MESSAGE_RESULTS_DIST_RELEASE_NOTIFICATION_FAILED, \
    MESSAGE_RESULTS_DIST_RELEASE_DOCUMENT_UPLOAD_FAILED
from exception import InternalServerErrorException
import requests
import traceback

from orm.entities.IO.File import FileModel


def release_result(result_type, result_code, data, stamp):
    try:
        data["timestamp"] = stamp.createdAt.strftime("%m/%d/%Y, %H:%M:%S")

        url = "%s/result/data/%s/%s/%s" % (
            connex_app.app.config['RESULT_DISSEMINATION_SYSTEM_URL'],
            connex_app.app.config['RESULT_DISSEMINATION_SYSTEM_ELECTION_CODE'],
            result_type, result_code
        )
        data = str(data)

        print("[RESULTS DIST] %s\n%s" % (url, data))

        response = requests.request(
            method="POST",
            url=url,
            headers={'Content-Type': 'application/json'},
            data=data,
            timeout=300
        )

        if response.status_code != 202:
            print("[RESULTS DIST] Error %d" % response.status_code)
            raise InternalServerErrorException(
                message="Results releasing failed.",
                code=MESSAGE_RESULTS_DIST_RELEASE_FAILED
            )
    except Exception as e:
        error_string = traceback.format_exc()
        print("[RESULTS DIST] Exception\n%s", error_string)

        raise InternalServerErrorException(
            message="Results releasing request failed.",
            code=MESSAGE_RESULTS_DIST_RELEASE_FAILED
        )


def upload_release_documents(result_type, result_code, files: FileModel):
    if len(files) == 0:
        return
    else:
        try:
            # Upload only the last uploaded file.
            file = files[len(files) - 1]

            response = requests.request(
                method="POST",
                url="%s/result/image/%s/%s/%s" % (
                    connex_app.app.config['RESULT_DISSEMINATION_SYSTEM_URL'],
                    connex_app.app.config['RESULT_DISSEMINATION_SYSTEM_ELECTION_CODE'],
                    result_type, result_code
                ),
                data=file.fileContent,
                headers={'Content-Type': file.fileContentType},
                timeout=300
            )

            print("URL : ", "%s/result/image/%s/%s/%s" % (
                connex_app.app.config['RESULT_DISSEMINATION_SYSTEM_URL'],
                connex_app.app.config['RESULT_DISSEMINATION_SYSTEM_ELECTION_CODE'],
                result_type, result_code
            ))
            print("\n\n\n\n########## response.status_code : ", response.status_code)

            if response.status_code != 202:
                raise InternalServerErrorException(
                    message="Results release document upload failed. %d",
                    code=MESSAGE_RESULTS_DIST_RELEASE_DOCUMENT_UPLOAD_FAILED
                )
        except Exception as e:
            error_string = traceback.format_exc()
            print(error_string)

            raise InternalServerErrorException(
                message="Results release document upload request failed.",
                code=MESSAGE_RESULTS_DIST_RELEASE_DOCUMENT_UPLOAD_FAILED
            )


def notify_release_result(result_type, result_code, data):
    try:
        request_query_string = ""
        for param in ["level", "ed_name", "pd_name"]:
            if param in data:
                if request_query_string == "":
                    request_query_string += "?"
                else:
                    request_query_string += "&"

                request_query_string += "%s=%s" % (param, data[param])

        response = requests.request(
            method="POST",
            url="%s/result/notification/%s/%s/%s%s" % (
                connex_app.app.config['RESULT_DISSEMINATION_SYSTEM_URL'],
                connex_app.app.config['RESULT_DISSEMINATION_SYSTEM_ELECTION_CODE'],
                result_type, result_code,
                request_query_string
            ),
            headers={'Content-Type': 'application/json'},
            timeout=300
        )

        if response.status_code != 202:
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
