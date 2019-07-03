from flask import abort
from config import db
from models import InvoiceModel, InvoiceItemModel
from schemas import Invoice_Schema, InvoiceItem_Schema
from domain import InvoiceItemDomain


def get_all():
    invoice_items = InvoiceItemDomain.invoice_item.get_all()
    return InvoiceItem_Schema(many=True).dump(invoice_items).data


def create(body):
    invoice_item = InvoiceItemDomain.invoice_item.create(body)

    return InvoiceItem_Schema().dump(invoice_item).data, 201
