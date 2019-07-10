from flask import abort
from config import db
from models import InvoiceModel, InvoiceStationaryItemModel
from schemas import Invoice_Schema
from util import RequestBody


def get_all(limit=20, offset=0, electionId=None, issuingOfficeId=None, receivingOfficeId=None, issuedBy=None,
            issuedTo=None):

    query = InvoiceModel.query

    if electionId is not None:
        query = query.filter(InvoiceModel.electionId == electionId)

    if issuingOfficeId is not None:
        query = query.filter(InvoiceModel.issuingOfficeId == issuingOfficeId)

    if receivingOfficeId is not None:
        query = query.filter(InvoiceModel.receivingOfficeId == receivingOfficeId)

    if issuedBy is not None:
        query = query.filter(InvoiceModel.issuedBy == issuedBy)

    if issuedTo is not None:
        query = query.filter(InvoiceModel.issuedTo == issuedTo)

    invoices = query.limit(limit).offset(offset).all()

    invoices_schema = Invoice_Schema(many=True)
    data = invoices_schema.dump(invoices).data
    return data


def create(body):
    request_body = RequestBody(body)
    invoice = InvoiceModel(
        electionId=request_body.get("electionId"),
        issuingOfficeId=request_body.get("issuingOfficeId"),
        receivingOfficeId=request_body.get("receivingOfficeId"),
        issuedTo=request_body.get("issuedTo")
    )

    # Add the entry to the database
    db.session.add(invoice)
    db.session.commit()

    # _create_invoice_items(invoice, request_body.get("stationaryItems"))

    return Invoice_Schema().dump(invoice).data, 201


# def _create_invoice_item(invoice, invoice_item_body):
#     request_body = RequestBody(invoice_item_body)
#     invoice_stationary_item = InvoiceStationaryItemModel(
#         invoiceId=invoice.invoiceId,
#         stationaryItemId=request_body.get("stationaryItemId")
#     )
#
#     db.session.add(invoice_stationary_item)
#     db.session.commit()
#
#
# def _create_invoice_items(invoice, invoice_items_body):
#     for item_body in invoice_items_body:
#         _create_invoice_item(invoice, item_body)


def update(tallySheetId, body):
    print("")


def confirm(invoiceId):
    result = InvoiceModel.query.filter(
        InvoiceModel.invoiceId == invoiceId
    ).update({"confirmed": True})

    db.session.commit()

    return result, 201
