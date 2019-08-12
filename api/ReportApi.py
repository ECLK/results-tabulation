from util import RequestBody

from flask import render_template, make_response
import pdfkit
from orm.entities import Report
from schemas import ReportSchema


def get_all():
    result = Report.get_all()

    return ReportSchema(many=True).dump(result).data


def create(reportCode, electionId, electorateId=None, officeId=None, parentReportId=None):
    Report.create(
        reportCode=reportCode,
        electionId=electionId,
        areaId=officeId,
        electorateId=electorateId,
        parentSubmissionId=parentReportId
    )
