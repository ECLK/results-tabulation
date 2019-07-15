from flask import abort
from util import RequestBody

from schemas import Invoice_Schema as Schema
from domain import InvoiceDomain as Domain


def get_all(limit=20, offset=0, electionId=None, issuingOfficeId=None, receivingOfficeId=None, issuedBy=None,
            issuedTo=None):
    result = Domain.get_all(
        electionId=electionId,
        issuingOfficeId=issuingOfficeId,
        receivingOfficeId=receivingOfficeId,
        issuedBy=issuedBy,
        issuedTo=issuedTo,

        limit=limit,
        offset=offset
    )

    return Schema(many=True).dump(result).data


def get_by_id(invoiceId):
    result = Domain.get_by_id(
        invoiceId=invoiceId
    )

    return Schema().dump(result).data


def create(body):
    request_body = RequestBody(body)
    result = Domain.create(
        electionId=request_body.get("electionId"),
        issuingOfficeId=request_body.get("issuingOfficeId"),
        receivingOfficeId=request_body.get("receivingOfficeId"),
        issuedTo=request_body.get("issuedTo"),
    )

    return Schema().dump(result).data


def update(tallySheetId, body):
    print("")


def confirm(invoiceId):
    result = Domain.update(
        invoiceId=invoiceId,
        confirmed=True
    )

    return Schema().dump(result).data
