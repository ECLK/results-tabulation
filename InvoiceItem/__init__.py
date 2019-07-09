from flask import abort
from config import db
from models import InvoiceModel, ItemModel
from schemas import Invoice_Schema, InvoiceItem_Schema
from domain import ItemDomain


def get_all():
    invoice_items = ItemDomain.invoice_item.get_all()
    return InvoiceItem_Schema(many=True).dump(invoice_items).data


def create(body):
    invoice_item = ItemDomain.invoice_item.create(body)

    return InvoiceItem_Schema().dump(invoice_item).data, 201
