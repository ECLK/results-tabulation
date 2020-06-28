from app import db, connex_app
from exception.messages import MESSAGE_CODE_PDF_SERVICE_ENTRY_CREATION_FAILED, MESSAGE_CODE_PDF_SERVICE_FETCH_FAILED
from exception import InternalServerErrorException
import requests
import json


def html_to_pdf(html):
    pdf_service_entry_response = requests.request(
        method="POST",
        url="%s/generate" % connex_app.app.config['PDF_SERVICE_URL'],
        headers={'Content-Type': 'application/json'},
        data=json.dumps({"html": html})
    )

    if pdf_service_entry_response.status_code != 200:
        raise InternalServerErrorException(
            message="PDF creation failed.",
            code=MESSAGE_CODE_PDF_SERVICE_ENTRY_CREATION_FAILED
        )

    pdf_response = requests.get(url=pdf_service_entry_response.json()["url"])

    if pdf_response.status_code != 200:
        raise InternalServerErrorException(
            message="PDF fetch failed.",
            code=MESSAGE_CODE_PDF_SERVICE_FETCH_FAILED
        )

    return pdf_response.content
