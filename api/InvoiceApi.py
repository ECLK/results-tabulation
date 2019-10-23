from app import db
from util import RequestBody, get_paginated_query

from schemas import Invoice_Schema as Schema
from orm.entities import Invoice as Model


def get_all(electionId=None, issuingOfficeId=None, receivingOfficeId=None, issuedBy=None,
            issuedTo=None):
    result = Model.get_all(
        electionId=electionId,
        issuingOfficeId=issuingOfficeId,
        receivingOfficeId=receivingOfficeId,
        issuedBy=issuedBy,
        issuedTo=issuedTo
    )

    result = get_paginated_query(result).all()

    return Schema(many=True).dump(result).data


def get_by_id(invoiceId):
    result = Model.get_by_id(
        invoiceId=invoiceId
    )

    return Schema().dump(result).data


def create(body):
    request_body = RequestBody(body)
    result = Model.create(
        electionId=request_body.get("electionId"),
        issuingOfficeId=request_body.get("issuingOfficeId"),
        receivingOfficeId=request_body.get("receivingOfficeId"),
        issuedTo=request_body.get("issuedTo"),
    )

    db.session.commit()

    return Schema().dump(result).data


def update(tallySheetId, body):
    print("")


def confirm(invoiceId):
    result = Model.update(
        invoiceId=invoiceId,
        confirmed=True
    )

    db.session.commit()

    return Schema().dump(result).data


def delete(invoiceId):
    result = Model.delete(
        invoiceId=invoiceId
    )

    db.session.commit()

    return result
