from flask import render_template

from exception import NotFoundException
from orm.entities import ReportVersion
from orm.entities.Submission.Report import Report_PRE_ALL_ISLAND_RESULTS
from orm.entities.SubmissionVersion.ReportVersion.util import get_PRE41_candidate_wise_aggregated_result
from orm.enums import ReportCodeEnum, AreaTypeEnum


class ReportVersion_PRE_ALL_ISLAND_RESULTS_Model(ReportVersion.Model):

    def __init__(self, reportId):
        report = Report_PRE_ALL_ISLAND_RESULTS.get_by_id(reportId=reportId)
        if report is None:
            raise NotFoundException("Report not found. (reportId=%d)" % reportId)

        content = {
            "data": [],
            "validVotes": 0,
            "rejectedVotes": 0,
            "totalVotes": 0
        }
        candidateWiseResult, countingCentres = get_PRE41_candidate_wise_aggregated_result(
            electionId=report.electionId,
            areas=report.area
        )

        for candidateWiseResultIndex in range(len(candidateWiseResult)):
            candidate = candidateWiseResult[candidateWiseResultIndex]
            content["data"].append([candidateWiseResultIndex + 1, candidate.candidateName])

            if candidateWiseResult[candidateWiseResultIndex].count is not None:
                count = candidateWiseResult[candidateWiseResultIndex].count

                # Append the aggregated vote count.
                content["data"][candidateWiseResultIndex].append(count)

                # To calculate the valid votes total.
                content["validVotes"] = content["validVotes"] + count

            else:
                # If the candidate wise count hasn't been found.
                # This could be not existing or not yet entered to the system.
                content["data"][candidateWiseResultIndex].append("")

        content["totalVotes"] = content["validVotes"] + content["rejectedVotes"]

        html = render_template(
            'PRE_ALL_ISLAND_RESULTS.html',
            content=content
        )

        super(ReportVersion_PRE_ALL_ISLAND_RESULTS_Model, self).__init__(reportId=reportId, html=html)

    __mapper_args__ = {
        'polymorphic_identity': ReportCodeEnum.PRE_ALL_ISLAND_RESULTS
    }


Model = ReportVersion_PRE_ALL_ISLAND_RESULTS_Model


def get_by_id(reportVersionId):
    result = Model.query.filter(
        Model.reportVersionId == reportVersionId
    ).one_or_none()

    return result


def create(reportId):
    result = Model(reportId=reportId)

    return result
