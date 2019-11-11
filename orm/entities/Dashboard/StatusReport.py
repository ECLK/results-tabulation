from app import db


class StatusReportModel(db.Model):
    __tablename__ = 'dashboard_status_report'

    statusReportId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reportType = db.Column(db.String(100), nullable=False)
    electoralDistrictName = db.Column(db.String(100), nullable=False)
    pollingDivisionName = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False)

    def __init__(self, reportType, electoralDistrictName, pollingDivisionName, status):
        super(StatusReportModel, self).__init__(
            reportType=reportType,
            electoralDistrictName=electoralDistrictName,
            pollingDivisionName=pollingDivisionName,
            status=status
        )

        db.session.add(self)
        db.session.flush()

    def update_status(self, status):
        self.status = status
        db.session.flush()


Model = StatusReportModel


def create(reportType, electoralDistrictName, pollingDivisionName, status):
    result = Model(
        reportType=reportType,
        electoralDistrictName=electoralDistrictName,
        pollingDivisionName=pollingDivisionName,
        status=status
    )

    return result
