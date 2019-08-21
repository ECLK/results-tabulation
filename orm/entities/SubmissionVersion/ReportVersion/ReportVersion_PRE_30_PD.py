from sqlalchemy import and_

from flask import render_template
from sqlalchemy.ext.hybrid import hybrid_property

from app import db
from sqlalchemy.orm import relationship
from sqlalchemy import func

from exception import NotFoundException
from orm.entities import ReportVersion, Party, Candidate, Submission, SubmissionVersion, Area
from orm.entities.Area.Office import CountingCentre
from orm.entities.Election import ElectionParty, ElectionCandidate
from orm.entities.Result import PartyWiseResult, CandidateWiseResult
from orm.entities.Result.CandidateWiseResult import CandidateCount
from orm.entities.Result.PartyWiseResult import PartyCount
from orm.entities.Submission import TallySheet
from orm.entities.Submission.Report import Report_PRE_30_PD, Report_PRE_41
from orm.entities.SubmissionVersion.ReportVersion.util import get_PRE41_candidate_and_area_wise_aggregated_result
from orm.entities.SubmissionVersion.TallySheetVersion import TallySheetVersionPRE41
from orm.enums import ReportCodeEnum, AreaTypeEnum


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

        aggregatedPartyCount, countingCentres, latestTallySheetVersions = get_PRE41_candidate_and_area_wise_aggregated_result(
            electionId=report.electionId,
            areas=report.area,
            subquery=True
        )

        content["countingCentres"] = [countingCentre.areaName for countingCentre in countingCentres]

        queryResult = db.session.query(
            Candidate.Model.candidateId,
            Candidate.Model.candidateName,
            Area.Model.areaId,
            Area.Model.areaName,
            aggregatedPartyCount.c.count
        ).join(
            ElectionCandidate.Model,
            ElectionCandidate.Model.candidateId == Candidate.Model.candidateId
        ).join(
            aggregatedPartyCount,
            aggregatedPartyCount.c.candidateId == Candidate.Model.candidateId,
            isouter=True
        ).join(
            Area.Model,
            Area.Model.areaId == aggregatedPartyCount.c.areaId,
            isouter=True
        ).filter(
            ElectionCandidate.Model.electionId == report.electionId,
        ).order_by(
            ElectionCandidate.Model.candidateId,
            Area.Model.areaId
        ).all()

        for i in range(0, len(countingCentres)):
            content["validVotes"].append(0)
            content["rejectedVotes"].append(0)
            content["totalVotes"].append(0)

        for i in range(int(len(queryResult) / len(countingCentres))):
            data_row = [i + 1, queryResult[i].candidateName]
            content["data"].append(data_row)
            total_count_per_candidate = 0

            for j in range(len(countingCentres)):
                query_result_index = (i * len(countingCentres)) + j
                count = queryResult[query_result_index].count
                if count is None:
                    data_row.append("")
                else:
                    content["validVotes"][j] = content["validVotes"][j] + count
                    content["rejectedVotes"][j] = 0  # TODO
                    content["totalVotes"][j] = content["validVotes"][j] + content["rejectedVotes"][j]

                    data_row.append(count)
                    total_count_per_candidate = total_count_per_candidate + count
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
