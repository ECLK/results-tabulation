"""
This is the people module and supports all the REST actions for the
people data
"""

from flask import make_response, abort
from config import db
from models import Invoice, InvoiceItem, Invoice_InvoiceItem
from schemas import Invoice_Schema
from api import tallySheet_PRE_41


def get_all():
    invoices = Invoice.query.all()

    invoices_schema = Invoice_Schema(many=True)
    data = invoices_schema.dump(invoices).data
    return data


def create_invoice_item(invoice, invoice_item_body):
    invoice_invoiceitem = Invoice_InvoiceItem(
        invoiceId=invoice.invoiceId,
        invoiceItemId=invoice_item_body["invoiceItemId"]
    )

    db.session.add(invoice_invoiceitem)
    db.session.commit()


def create_invoice_items(invoice, invoice_items_body):
    for item_body in invoice_items_body:
        create_invoice_item(invoice, item_body)


def create(body):
    invoice = Invoice(
        electionId=body["electionId"],
        issuingOfficeId=body["issuingOfficeId"],
        receivingOfficeId=body["receivingOfficeId"],
        issuedTo=body["issuedTo"]
    )

    # Add the entry to the database
    db.session.add(invoice)
    db.session.commit()

    create_invoice_items(invoice, body["invoiceItems"])

    return Invoice_Schema().dump(invoice).data, 201


def update(tallySheetId, body):
    """
        Append new version to the tally sheet.
    """
    # Get the tally sheet
    tallySheet = Invoice.query.filter(
        Invoice.invoiceId == tallySheetId
    ).one_or_none()

    if tallySheet is None:
        abort(
            404,
            "Tally Sheet not found for Id: {tallySheetId}".format(tallySheetId=tallySheetId),
        )

    create_tallysheet_version(body, tallySheet)

    schema = TallySheetVersionSchema()

    return schema.dump(new_tallysheet).data, 201
