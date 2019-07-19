from flask import abort
from util import RequestBody
from schemas import Invoice_StationaryItem_Schema as Schema
from domain import InvoiceStationaryItemDomain, ImageDomain
import os
import connexion


def get_all(invoiceId, stationaryItemId=None, limit=20, offset=0, received=None, receivedFrom=None, receivedBy=None,
            receivedOffice=None):
    result = InvoiceStationaryItemDomain.get_all(
        invoiceId=invoiceId,
        stationaryItemId=stationaryItemId,
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
    request_body = RequestBody(body)
    result = InvoiceStationaryItemDomain.create(
        invoiceId=invoiceId,
        stationaryItemId=request_body.get("stationaryItemId")
    )

    return Schema().dump(result).data, 201


def receive(body):
    request_body = RequestBody(body)

    image = ImageDomain.create(connexion.request.files['scannedImages'])

    result = InvoiceStationaryItemDomain.update(
        invoiceId=request_body.get("invoiceId"),
        stationaryItemId=request_body.get("stationaryItemId"),
        received=True,
        receivedFrom=request_body.get("receivedFrom"),
        receivedOfficeId=request_body.get("receivedOfficeId")
    )

    return Schema().dump(result).data, 201


def delete(invoiceId, stationaryItemId):
    result = InvoiceStationaryItemDomain.delete(
        invoiceId=invoiceId,
        stationaryItemId=stationaryItemId
    )

    return result
