from exception import NotFoundException
from orm.entities import Report, ReportVersion
from orm.entities.ReportVersion import ReportVersion_PRE_41, ReportVersion_PRE_30_PD, ReportVersion_PRE_30_ED
from orm.enums import ReportCodeEnum
from util import RequestBody

from flask import render_template, make_response
import pdfkit
from schemas import ReportVersionSchema


def get_all():
    result = ReportVersion.get_all()

    return ReportVersionSchema(many=True).dump(result).data


def get_report_version_entity(reportCode):
    if reportCode == ReportCodeEnum.PRE_41:
        return ReportVersion_PRE_41
    elif reportCode == ReportCodeEnum.PRE_30_PD:
        return ReportVersion_PRE_30_PD
    elif reportCode == ReportCodeEnum.PRE_30_ED:
        return ReportVersion_PRE_30_ED
    else:
        raise NotFoundException("Report version not found (reportCode=%s)", reportCode)


def create(reportId):
    report = Report.get_by_id(reportId=reportId)
    result = get_report_version_entity(report.reportCode).create(reportId=reportId)

    return ReportVersionSchema().dump(result).data
