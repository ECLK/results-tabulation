import numpy
from flask import render_template
from sqlalchemy import func, and_
from sqlalchemy.sql import select

from app import db
from exception import NotFoundException
from orm.entities import ReportVersion, Party, Candidate, Submission, SubmissionVersion
from orm.entities.Area.Office import CountingCentre
from orm.entities.Election import ElectionParty, ElectionCandidate
from orm.entities.Result import CandidateWiseResult
from orm.entities.Result.CandidateWiseResult import CandidateCount
from orm.entities.Result.PartyWiseResult import PartyCount
from orm.entities.Submission.Report import Report_PRE_30_ED
from orm.entities.SubmissionVersion.ReportVersion.util import get_PRE41_candidate_wise_aggregated_result
from orm.entities.SubmissionVersion.TallySheetVersion import TallySheetVersionPRE41
from orm.enums import ReportCodeEnum, AreaTypeEnum
from util import get_array


class ReportVersion_PRE_30_ED_Model(ReportVersion.Model):

    def __init__(self, reportId):
        report = Report_PRE_30_ED.get_by_id(reportId=reportId)
        if report is None:
            raise NotFoundException("Report not found. (reportId=%d)" % reportId)

        content = {
            "electoralDistrict": report.area.areaName,
            "pollingDivisions": [],
            "data": [],
            "validVotes": [],
            "rejectedVotes": [],
            "totalVotes": []
        }

        pollingDivisions = report.area.get_associated_areas(AreaTypeEnum.PollingDivision)

        candidates = db.session.query(
            ElectionCandidate.Model.candidateId,
            Candidate.Model.candidateName
        ).join(
            Candidate.Model,
            Candidate.Model.candidateId == ElectionCandidate.Model.candidateId
        ).order_by(
            ElectionCandidate.Model.candidateId
        ).all()

        for candidateIndex in range(len(candidates)):
            candidate = candidates[candidateIndex]
            content["data"].append([candidateIndex + 1, candidate.candidateName])

        for pollingDivisionIndex in range(len(pollingDivisions)):
            pollingDivision = pollingDivisions[pollingDivisionIndex]

            content["pollingDivisions"].append(pollingDivision.areaName)

            divisionWiseResult, countingCentres, latestTallySheetVersions = get_PRE41_candidate_wise_aggregated_result(
                electionId=report.electionId,
                areas=pollingDivision
            )

            total_valid_votes_from_division = 0
            total_invalid_votes_from_division = 0
            for divisionWiseResultIndex in range(len(divisionWiseResult)):
                if divisionWiseResult[divisionWiseResultIndex].count is not None:
                    count = divisionWiseResult[divisionWiseResultIndex].count
                    content["data"][divisionWiseResultIndex].append(count)
                    total_valid_votes_from_division = total_valid_votes_from_division + count
                else:
                    content["data"][divisionWiseResultIndex].append("")

            content["validVotes"].append(total_valid_votes_from_division)
            content["rejectedVotes"].append(total_invalid_votes_from_division)  # TODO
            content["totalVotes"].append(total_valid_votes_from_division + total_invalid_votes_from_division)

        for data_row in content["data"]:
            valid_counts = [count for count in data_row[2:] if count is not ""]
            data_row.append(sum(valid_counts))

        content["validVotes"].append(sum(content["validVotes"]))
        content["rejectedVotes"].append(sum(content["rejectedVotes"]))
        content["totalVotes"].append(sum(content["totalVotes"]))

        html = render_template(
            'PRE-30-ED.html',
            content=content
        )

        super(ReportVersion_PRE_30_ED_Model, self).__init__(reportId=reportId, html=html)

    __mapper_args__ = {
        'polymorphic_identity': ReportCodeEnum.PRE_30_ED
    }


Model = ReportVersion_PRE_30_ED_Model


def get_by_id(reportVersionId):
    result = Model.query.filter(
        Model.reportVersionId == reportVersionId
    ).one_or_none()

    return result


def create(reportId):
    result = Model(reportId=reportId)

    return result
