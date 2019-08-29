from flask import render_template

from exception import NotFoundException
from orm.entities import ReportVersion

from orm.entities.Submission.Report import Report_PRE_30_PD
from orm.entities.SubmissionVersion.ReportVersion.util import get_PRE41_candidate_and_area_wise_aggregated_result
from orm.enums import ReportCodeEnum


class ReportVersion_PRE_30_PD_Model(ReportVersion.Model):

    def __init__(self, reportId):
        report = Report_PRE_30_PD.get_by_id(reportId=reportId)
        if report is None:
            raise NotFoundException("Report not found. (reportId=%d)" % reportId)

        content = {
            "data": [],
            "countingCentres": [],
            "validVotes": [],
            "rejectedVotes": [],
            "totalVotes": []
        }

        queryResult, countingCentres = get_PRE41_candidate_and_area_wise_aggregated_result(
            electionId=report.electionId,
            areas=report.area,
            subquery=False
        )

        content["countingCentres"] = [countingCentre.areaName for countingCentre in countingCentres]

        # Fill the validVotes, rejectedVotes and totalVotes with zeros.
        for i in range(0, len(countingCentres)):
            content["validVotes"].append(0)
            content["rejectedVotes"].append(0)
            content["totalVotes"].append(0)

        # Iterate by candidates.
        for i in range(int(len(queryResult) / len(countingCentres))):
            # Append candidate details.
            data_row = [i + 1, queryResult[i].candidateName]
            content["data"].append(data_row)
            total_count_per_candidate = 0

            # Iterate by counting centres.
            for j in range(len(countingCentres)):
                # Determine the result index mapping with the counting centre and candidate.
                query_result_index = (i * len(countingCentres)) + j

                count = queryResult[query_result_index].count

                if count is None:
                    data_row.append("")
                else:
                    # Append the count of votes of the counting centre.
                    data_row.append(count)

                    # Calculate the candidate wise total votes.
                    total_count_per_candidate = total_count_per_candidate + count

                    # Calculate valid votes count.
                    content["validVotes"][j] = content["validVotes"][j] + count

                    # Calculate validVotes count.
                    content["rejectedVotes"][j] = 0  # TODO

                    content["totalVotes"][j] = content["validVotes"][j] + content["rejectedVotes"][j]

            data_row.append(total_count_per_candidate)

        content["validVotes"].append(sum(content["validVotes"]))
        content["rejectedVotes"].append(sum(content["rejectedVotes"]))
        content["totalVotes"].append(sum(content["totalVotes"]))

        html = render_template(
            'PRE-30-PD.html',
            content=content
        )

        super(ReportVersion_PRE_30_PD_Model, self).__init__(reportId=reportId, html=html)

    __mapper_args__ = {
        'polymorphic_identity': ReportCodeEnum.PRE_30_PD
    }


Model = ReportVersion_PRE_30_PD_Model


def get_by_id(reportVersionId):
    result = Model.query.filter(
        Model.reportVersionId == reportVersionId
    ).one_or_none()

    return result


def create(reportId):
    result = Model(reportId=reportId)

    return result
