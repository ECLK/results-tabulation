from app import db, connex_app
from exception.messages import MESSAGE_CODE_PDF_SERVICE_ENTRY_CREATION_FAILED, MESSAGE_CODE_PDF_SERVICE_FETCH_FAILED
from exception import InternalServerErrorException
import requests
import json
import traceback


def html_to_pdf(html):
    try:
        pdf_service_entry_response = requests.request(
            method="POST",
            url="%s/generate" % connex_app.app.config['PDF_SERVICE_URL'],
            headers={'Content-Type': 'application/json'},
            data=json.dumps({"html": html})
        )
    except Exception as e:
        error_string = traceback.format_exc()
        print(error_string)

        raise InternalServerErrorException(
            message="PDF creation request failed.",
            code=MESSAGE_CODE_PDF_SERVICE_ENTRY_CREATION_FAILED
        )

    if pdf_service_entry_response.status_code != 200:
        raise InternalServerErrorException(
            message="PDF creation unsuccessful.",
            code=MESSAGE_CODE_PDF_SERVICE_ENTRY_CREATION_FAILED
        )

    try:
        pdf_response = requests.get(url=pdf_service_entry_response.json()["url"])
    except Exception as e:
        error_string = traceback.format_exc()
        print(error_string)

        raise InternalServerErrorException(
            message="PDF fetch request failed.",
            code=MESSAGE_CODE_PDF_SERVICE_FETCH_FAILED
        )

    if pdf_response.status_code != 200:
        raise InternalServerErrorException(
            message="PDF fetch unsuccessful.",
            code=MESSAGE_CODE_PDF_SERVICE_FETCH_FAILED
        )

    return pdf_response.content
