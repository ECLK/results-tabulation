from flask import render_template
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy import func, and_, or_

from app import db
from exception import NotFoundException
from orm.entities import Area, Candidate, Party, Submission
from orm.entities.Election import ElectionCandidate
from orm.entities.SubmissionVersion import TallySheetVersion
from orm.entities.TallySheetVersionRow import TallySheetVersionRow_PRE_30_PD, TallySheetVersionRow_RejectedVoteCount
from util import get_paginated_query, to_empty_string_or_value

from orm.entities.Submission import TallySheet
from orm.enums import TallySheetCodeEnum, AreaTypeEnum, VoteTypeEnum


class TallySheetVersion_PRE_30_PD_Model(TallySheetVersion.Model):

    def __init__(self, tallySheetId):
        super(TallySheetVersion_PRE_30_PD_Model, self).__init__(
            tallySheetId=tallySheetId
        )

    __mapper_args__ = {
        'polymorphic_identity': TallySheetCodeEnum.PRE_30_PD
    }

    def add_row(self, countingCentreId, candidateId, count):
        from orm.entities.TallySheetVersionRow import TallySheetVersionRow_PRE_30_PD

        TallySheetVersionRow_PRE_30_PD.create(
            tallySheetVersionId=self.tallySheetVersionId,
            candidateId=candidateId,
            countingCentreId=countingCentreId,
            count=count
        )

    # content = relationship("TallySheetVersionRow_PRE_30_PD_Model")

    @hybrid_property
    def countingCentres(self):
        return self.submission.area.get_associated_areas(
            areaType=AreaTypeEnum.CountingCentre, electionId=self.submission.electionId
        )

    @hybrid_property
    def content(self):
        countingCentres = self.countingCentres

        return db.session.query(
            ElectionCandidate.Model.candidateId,
            Candidate.Model.candidateName,
            Area.Model.areaId.label("countingCentreId"),
            Area.Model.areaName.label("countingCentreName"),
            func.sum(TallySheetVersionRow_PRE_30_PD.Model.count).label("count"),
        ).join(
            Candidate.Model,
            Candidate.Model.candidateId == ElectionCandidate.Model.candidateId
        ).join(
            Party.Model,
            Party.Model.partyId == ElectionCandidate.Model.partyId
        ).join(
            Area.Model,
            Area.Model.areaId.in_([area.areaId for area in countingCentres])
        ).join(
            TallySheetVersionRow_PRE_30_PD.Model,
            and_(
                TallySheetVersionRow_PRE_30_PD.Model.tallySheetVersionId == self.tallySheetVersionId,
                TallySheetVersionRow_PRE_30_PD.Model.countingCentreId == Area.Model.areaId,
                TallySheetVersionRow_PRE_30_PD.Model.candidateId == ElectionCandidate.Model.candidateId
            ),
            isouter=True
        ).filter(
            ElectionCandidate.Model.electionId.in_(self.submission.election.mappedElectionIds)
        ).group_by(
            ElectionCandidate.Model.candidateId,
            Area.Model.areaId
        ).order_by(
            ElectionCandidate.Model.candidateId,
            func.cast(Area.Model.areaName, db.Integer)
        ).all()

    def area_wise_valid_vote_count(self):
        return db.session.query(
            TallySheetVersionRow_PRE_30_PD.Model.countingCentreId.label("areaId"),
            func.sum(TallySheetVersionRow_PRE_30_PD.Model.count).label("validVoteCount")
        ).group_by(
            TallySheetVersionRow_PRE_30_PD.Model.countingCentreId
        ).filter(
            TallySheetVersionRow_PRE_30_PD.Model.tallySheetVersionId == self.tallySheetVersionId
        )

    def area_wise_rejected_vote_count(self):
        return db.session.query(
            TallySheetVersionRow_RejectedVoteCount.Model.areaId,
            func.sum(TallySheetVersionRow_RejectedVoteCount.Model.rejectedVoteCount).label("rejectedVoteCount"),
        ).group_by(
            TallySheetVersionRow_RejectedVoteCount.Model.areaId,
        ).filter(
            TallySheetVersionRow_RejectedVoteCount.Model.tallySheetVersionId == self.tallySheetVersionId,
            TallySheetVersionRow_RejectedVoteCount.Model.candidateId == None
        )

    @hybrid_property
    def areaWiseSummary(self):
        area_wise_valid_vote_count_subquery = self.area_wise_valid_vote_count().subquery()
        area_wise_rejected_vote_count_subquery = self.area_wise_rejected_vote_count().subquery()

        return db.session.query(
            Area.Model.areaId,
            Area.Model.areaName,
            func.sum(area_wise_valid_vote_count_subquery.c.validVoteCount).label("validVoteCount"),
            func.sum(area_wise_rejected_vote_count_subquery.c.rejectedVoteCount).label("rejectedVoteCount"),
            func.sum(
                area_wise_valid_vote_count_subquery.c.validVoteCount +
                area_wise_rejected_vote_count_subquery.c.rejectedVoteCount
            ).label("totalVoteCount")
        ).join(
            area_wise_valid_vote_count_subquery,
            area_wise_valid_vote_count_subquery.c.areaId == Area.Model.areaId,
            isouter=True
        ).join(
            area_wise_rejected_vote_count_subquery,
            area_wise_rejected_vote_count_subquery.c.areaId == Area.Model.areaId,
            isouter=True
        ).group_by(
            Area.Model.areaId
        ).order_by(
            func.cast(Area.Model.areaName, db.Integer)
        ).filter(
            Area.Model.areaId.in_([area.areaId for area in self.countingCentres])
        ).all()

    @hybrid_property
    def summary(self):
        area_wise_valid_vote_count_subquery = self.area_wise_valid_vote_count().subquery()
        area_wise_rejected_vote_count_subquery = self.area_wise_rejected_vote_count().subquery()

        return db.session.query(
            func.count(Area.Model.areaId).label("areaCount"),
            func.sum(area_wise_valid_vote_count_subquery.c.validVoteCount).label("validVoteCount"),
            func.sum(area_wise_rejected_vote_count_subquery.c.rejectedVoteCount).label("rejectedVoteCount"),
            func.sum(
                area_wise_valid_vote_count_subquery.c.validVoteCount +
                area_wise_rejected_vote_count_subquery.c.rejectedVoteCount
            ).label("totalVoteCount")
        ).join(
            area_wise_valid_vote_count_subquery,
            area_wise_valid_vote_count_subquery.c.areaId == Area.Model.areaId,
            isouter=True
        ).join(
            area_wise_rejected_vote_count_subquery,
            area_wise_rejected_vote_count_subquery.c.areaId == Area.Model.areaId,
            isouter=True
        ).filter(
            Area.Model.areaId.in_([area.areaId for area in self.countingCentres])
        ).one_or_none()

    def html(self):
        area_wise_summary = self.areaWiseSummary
        summary = self.summary

        content = {
            "tallySheetCode": "PRE/30/PD",
            "electoralDistrict": Area.get_associated_areas(
                self.submission.area, AreaTypeEnum.ElectoralDistrict)[0].areaName,
            "pollingDivision": self.submission.area.areaName,
            "data": [],
            "countingCentres": [],
            "validVoteCounts": [],
            "rejectedVoteCounts": [],
            "totalVoteCounts": []
        }

        # Append the area wise column totals
        for area_wise_summary_item in area_wise_summary:
            content["countingCentres"].append(to_empty_string_or_value(area_wise_summary_item.areaName))
            content["validVoteCounts"].append(to_empty_string_or_value(area_wise_summary_item.validVoteCount))
            content["rejectedVoteCounts"].append(to_empty_string_or_value(area_wise_summary_item.rejectedVoteCount))
            content["totalVoteCounts"].append(to_empty_string_or_value(area_wise_summary_item.totalVoteCount))

        # Append the grand totals
        content["validVoteCounts"].append(to_empty_string_or_value(summary.validVoteCount))
        content["rejectedVoteCounts"].append(to_empty_string_or_value(summary.rejectedVoteCount))
        content["totalVoteCounts"].append(to_empty_string_or_value(summary.totalVoteCount))

        if self.submission.election.voteType == VoteTypeEnum.Postal:
            content["tallySheetCode"] = "PRE/30/PV"

        countingCentreCount = len(content["countingCentres"])
        queryResult = self.content
        parties = int(len(queryResult) / countingCentreCount)

        # Iterate by candidates.
        for i in range(parties):
            # Append candidate details.
            data_row = [i + 1, queryResult[i * countingCentreCount].candidateName]
            content["data"].append(data_row)
            total_count_per_candidate = 0

            # Iterate by counting centres.
            for j in range(countingCentreCount):
                # Determine the result index mapping with the counting centre and candidate.
                query_result_index = (i * countingCentreCount) + j

                count = queryResult[query_result_index].count

                if count is None:
                    data_row.append("")
                else:
                    # Append the count of votes of the counting centre.
                    data_row.append(count)

                    # Calculate the candidate wise total votes.
                    total_count_per_candidate = total_count_per_candidate + count

            data_row.append(total_count_per_candidate)

        html = render_template(
            'PRE-30-PD.html',
            content=content
        )

        return html


Model = TallySheetVersion_PRE_30_PD_Model


def get_all(tallySheetId):
    query = Model.query.filter(Model.tallySheetId == tallySheetId)

    result = get_paginated_query(query).all()

    return result


def get_by_id(tallySheetId, tallySheetVersionId):
    tallySheet = TallySheet.get_by_id(tallySheetId=tallySheetId)
    if tallySheet is None:
        raise NotFoundException("Tally sheet not found. (tallySheetId=%d)" % tallySheetId)
    elif tallySheet.tallySheetCode is not TallySheetCodeEnum.PRE_30_PD:
        raise NotFoundException("Requested version not found. (tallySheetId=%d)" % tallySheetId)

    result = Model.query.filter(
        Model.tallySheetVersionId == tallySheetVersionId
    ).one_or_none()

    return result


def create(tallySheetId):
    result = Model(tallySheetId=tallySheetId)

    return result
