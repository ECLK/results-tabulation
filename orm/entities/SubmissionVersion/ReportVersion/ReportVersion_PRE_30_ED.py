from flask import render_template

from exception import NotFoundException
from orm.entities import ReportVersion
from orm.entities.Submission.Report import Report_PRE_30_ED
from orm.entities.SubmissionVersion.ReportVersion.util import get_PRE41_candidate_wise_aggregated_result
from orm.enums import ReportCodeEnum, AreaTypeEnum


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

        # Retrieve the mapped polling divisions list.
        pollingDivisions = report.area.get_associated_areas(AreaTypeEnum.PollingDivision)

        # Query the candidate wise results of each polling division separately.
        for pollingDivisionIndex in range(len(pollingDivisions)):
            pollingDivision = pollingDivisions[pollingDivisionIndex]

            content["pollingDivisions"].append(pollingDivision.areaName)

            divisionWiseResult, countingCentres = get_PRE41_candidate_wise_aggregated_result(
                electionId=report.electionId,
                areas=pollingDivision
            )

            total_valid_votes_from_division = 0
            total_invalid_votes_from_division = 0
            for divisionWiseResultIndex in range(len(divisionWiseResult)):

                # Append the candidateName and number (Only if it's not there already).
                if len(content["data"]) <= divisionWiseResultIndex:
                    candidate = divisionWiseResult[divisionWiseResultIndex]
                    content["data"].append([divisionWiseResultIndex + 1, candidate.candidateName])

                if divisionWiseResult[divisionWiseResultIndex].count is not None:
                    count = divisionWiseResult[divisionWiseResultIndex].count

                    # Append the aggregated vote count.
                    content["data"][divisionWiseResultIndex].append(count)

                    # To calculate the division wise total.
                    total_valid_votes_from_division = total_valid_votes_from_division + count
                else:
                    # If the candidate wise count hasn't been found.
                    # This could be not existing or not yet entered to the system.
                    content["data"][divisionWiseResultIndex].append("")

            # Append the division wise valid votes total.
            content["validVotes"].append(total_valid_votes_from_division)

            # TODO
            content["rejectedVotes"].append(total_invalid_votes_from_division)

            # Append the division wise total vote count which is the sum of valid and invalid votes.
            content["totalVotes"].append(total_valid_votes_from_division + total_invalid_votes_from_division)

        # Calculate the candidate wise totals.
        for data_row in content["data"]:
            valid_counts = [count for count in data_row[2:] if count is not ""]
            data_row.append(sum(valid_counts))

        # Append the total valid votes.
        content["validVotes"].append(sum(content["validVotes"]))

        # Append the total invalid votes.
        content["rejectedVotes"].append(sum(content["rejectedVotes"]))

        # Append the total votes.
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
