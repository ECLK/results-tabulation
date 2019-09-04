from api import FileApi
from app import db
from exception import NotFoundException
from orm.entities.SubmissionVersion import ReportVersion, TallySheetVersion
from orm.entities.Submission import Report, TallySheet
from orm.entities.SubmissionVersion.ReportVersion import ReportVersion_PRE_41, ReportVersion_PRE_30_PD, \
    ReportVersion_PRE_ALL_ISLAND_RESULTS
from orm.entities.SubmissionVersion.ReportVersion import ReportVersion_PRE_30_ED
from orm.enums import ReportCodeEnum

from schemas import ReportVersionSchema
from flask import Response


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
    elif reportCode == ReportCodeEnum.PRE_ALL_ISLAND_RESULTS:
        return ReportVersion_PRE_ALL_ISLAND_RESULTS
    else:
        raise NotFoundException("Report version not found (reportCode=%s)", reportCode)


def create(reportId):
    report = Report.get_by_id(reportId=reportId)
    result = get_report_version_entity(report.reportCode).create(reportId=reportId)

    db.session.commit()

    return ReportVersionSchema().dump(result).data


def html(reportId, reportVersionId):
    tallySheetVersion = TallySheetVersion.get_by_id(tallySheetVersionId=reportVersionId)

    db.session.commit()

    return Response(tallySheetVersion.html(), mimetype='text/html')
