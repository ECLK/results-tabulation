from flask import abort
from util import RequestBody

from schemas import Invoice_StationaryItem_Schema as Schema
from domain import InvoiceStationaryItemDomain
from exception import ApiException, InternalServerErrorException


def get_all(invoiceId, limit=20, offset=0, received=None, receivedFrom=None, receivedBy=None, receivedOffice=None):
    result = InvoiceStationaryItemDomain.get_all(
        invoiceId=invoiceId,
        received=received,
        receivedFrom=receivedFrom,
        receivedBy=receivedBy,
        receivedOffice=receivedOffice,

        limit=limit,
        offset=offset
    )

    return Schema(many=True).dump(result).data


def get_by_id(invoiceId, stationaryItemId):
    result = InvoiceStationaryItemDomain.get_by_id(invoiceId, stationaryItemId)

    return Schema().dump(result).data, 201


def create(invoiceId, body):
    try:
        request_body = RequestBody(body)
        result = InvoiceStationaryItemDomain.create(
            invoiceId=invoiceId,
            stationaryItemId=request_body.get("stationaryItemId")
        )

        return Schema().dump(result).data, 201
    except ApiException as error:
        return error.to_json_response()


def receive(invoiceId, stationaryItemId, body):
    try:
        request_body = RequestBody(body)
        result = InvoiceStationaryItemDomain.update(
            invoiceId=invoiceId,
            stationaryItemId=stationaryItemId,
            received=True,
            receivedFrom=request_body.get("receivedFrom"),
            receivedOfficeId=request_body.get("receivedOfficeId")
        )

        return Schema().dump(result).data, 201
    except ApiException as error:
        return error.to_json_response()
    except Exception as error:
        return InternalServerErrorException().to_json_response()
