from util import RequestBody

from flask import render_template, make_response
import pdfkit
from orm.entities import ReportVersion
from schemas import ReportVersionSchema


def get_all():
    result = ReportVersion.get_all()

    return ReportVersionSchema(many=True).dump(result).data


def create(reportId):
    result = ReportVersion.create(reportId=reportId)

    return ReportVersionSchema().dump(result).data
