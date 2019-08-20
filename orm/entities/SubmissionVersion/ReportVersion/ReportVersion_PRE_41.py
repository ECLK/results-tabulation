import numpy
from flask import render_template
from app import db

from exception import NotFoundException, ForbiddenException
from orm.entities import ReportVersion, Area, Candidate, Party
from orm.entities.Election import ElectionParty, ElectionCandidate
from orm.entities.Result.PartyWiseResult import PartyCount
from orm.entities.Submission.Report import Report_PRE_41
from orm.entities.SubmissionVersion.TallySheetVersion import TallySheetVersionPRE41
from orm.enums import ReportCodeEnum, AreaTypeEnum


class ReportVersion_PRE_41_Model(ReportVersion.Model):

    def __init__(self, reportId):
        report = Report_PRE_41.get_by_id(reportId=reportId)
        if report is None:
            raise NotFoundException("Report not found. (reportId=%d)" % reportId)

        if len(report.area.tallySheets_PRE_41) is 0:
            raise ForbiddenException(
                "There's no PRE-41 tally sheet for the counting centre (officeId)" % report.area.areaId)
        elif len(report.area.tallySheets_PRE_41) > 1:
            raise ForbiddenException(
                "There's more than one PRE-41 tally sheet for the counting centre (officeId)" % report.area.areaId)

        partyWiseResultIds = []
        for tallySheet in report.area.tallySheets_PRE_41:
            partyWiseResultIds.append(tallySheet.latestVersion.partyWiseResultId)

        tallySheetContent = db.session.query(
            ElectionParty.Model.partyId,
            PartyCount.Model.count,
            PartyCount.Model.countInWords,
            Candidate.Model.candidateName,
            Party.Model.partySymbol,
        ).join(
            PartyCount.Model,
            PartyCount.Model.partyId == ElectionParty.Model.partyId,
        ).join(
            Party.Model,
            Party.Model.partyId == ElectionParty.Model.partyId,
        ).join(
            ElectionCandidate.Model,
            ElectionCandidate.Model.partyId == ElectionParty.Model.partyId,
        ).join(
            Candidate.Model,
            Candidate.Model.candidateId == ElectionCandidate.Model.candidateId,
        ).filter(
            PartyCount.Model.partyWiseResultId.in_(partyWiseResultIds),
            ElectionParty.Model.electionId == report.submission.electionId
        ).all()

        content = {
            "title": "PRESIDENTIAL ELECTION ACT NO. 15 OF 1981",
            "electoralDistrict": Area.get_associated_areas(report.area, AreaTypeEnum.ElectoralDistrict)[0].areaName,
            "pollingDivision": Area.get_associated_areas(report.area, AreaTypeEnum.PollingDivision)[0].areaName,
            "pollingDistrictNos": ", ".join([
                pollingDistrict.areaName for pollingDistrict in
                Area.get_associated_areas(report.area, AreaTypeEnum.PollingDistrict)
            ]),
            "countingHallNo": report.area.areaName,
            "data": [
            ],
            "total": 3000,
            "rejectedVotes": 50,
            "grandTotal": 3050
        }

        for row_index in range(len(tallySheetContent)):
            row = tallySheetContent[row_index]
            content["data"].append([
                row_index + 1,
                row.candidateName,
                row.partySymbol,
                row.countInWords,
                row.count,
                ""
            ])

        content["data"] = numpy.array(content["data"], dtype='object')

        content["total"] = sum(content["data"][:, 4])

        content["rejectedVotes"] = 0  # TODO

        content["grandTotal"] = content["total"] + content["rejectedVotes"]

        html = render_template(
            'pre-41.html',
            content=content
        )

        # html = render_template(
        #     'test-report-template.html',
        #     title="Test Template PRE-41",
        #     data=data
        # )

        super(ReportVersion_PRE_41_Model, self).__init__(reportId=reportId, html=html)

    __mapper_args__ = {
        'polymorphic_identity': ReportCodeEnum.PRE_41
    }


Model = ReportVersion_PRE_41_Model


def get_by_id(reportVersionId):
    result = Model.query.filter(
        Model.reportVersionId == reportVersionId
    ).one_or_none()

    return result


def create(reportId):
    result = Model(reportId=reportId)

    return result
