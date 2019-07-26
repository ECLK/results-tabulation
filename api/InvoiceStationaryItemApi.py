from util import RequestBody
from schemas import Invoice_StationaryItem_Schema as Schema
from orm.entities import Image, InvoiceStationaryItem
import connexion


def get_all(invoiceId, stationaryItemId=None, received=None, receivedFrom=None, receivedBy=None,
            receivedOffice=None):
    result = InvoiceStationaryItem.get_all(
        invoiceId=invoiceId,
        stationaryItemId=stationaryItemId,
        received=received,
        receivedFrom=receivedFrom,
        receivedBy=receivedBy,
        receivedOffice=receivedOffice
    )

    return Schema(many=True).dump(result).data


def get_by_id(invoiceId, stationaryItemId):
    result = InvoiceStationaryItem.get_by_id(invoiceId, stationaryItemId)

    return Schema().dump(result).data, 201


def create(invoiceId, body):
    request_body = RequestBody(body)
    result = InvoiceStationaryItem.create(
        invoiceId=invoiceId,
        stationaryItemId=request_body.get("stationaryItemId")
    )

    return Schema().dump(result).data, 201


def receive(body):
    request_body = RequestBody(body)
    result = InvoiceStationaryItem.update(
        invoiceId=request_body.get("invoiceId"),
        stationaryItemId=request_body.get("stationaryItemId"),
        received=True,
        receivedFrom=request_body.get("receivedFrom"),
        receivedOfficeId=request_body.get("receivedOfficeId"),
        scannedImages=connexion.request.files['scannedImages']
    )

    return Schema().dump(result).data, 201


def delete(invoiceId, stationaryItemId):
    result = InvoiceStationaryItem.delete(
        invoiceId=invoiceId,
        stationaryItemId=stationaryItemId
    )

    return result
