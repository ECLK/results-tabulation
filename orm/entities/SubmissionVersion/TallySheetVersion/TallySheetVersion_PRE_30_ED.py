from flask import render_template
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy import func, and_

from app import db
from exception import NotFoundException
from orm.entities import Area, Candidate, Party, Election, Submission, SubmissionVersion
from orm.entities.Election import ElectionCandidate
from orm.entities.SubmissionVersion import TallySheetVersion
from orm.entities.TallySheetVersionRow import TallySheetVersionRow_PRE_30_ED, TallySheetVersionRow_RejectedVoteCount
from util import get_paginated_query

from orm.entities.Submission import TallySheet
from orm.enums import TallySheetCodeEnum, AreaTypeEnum, VoteTypeEnum


class TallySheetVersion_PRE_30_ED_Model(TallySheetVersion.Model):

    def __init__(self, tallySheetId):
        super(TallySheetVersion_PRE_30_ED_Model, self).__init__(
            tallySheetId=tallySheetId
        )

    __mapper_args__ = {
        'polymorphic_identity': TallySheetCodeEnum.PRE_30_ED
    }

    def add_row(self, pollingDivisionId, candidateId, count, electionId):
        from orm.entities.TallySheetVersionRow import TallySheetVersionRow_PRE_30_ED

        TallySheetVersionRow_PRE_30_ED.create(
            tallySheetVersionId=self.tallySheetVersionId,
            candidateId=candidateId,
            pollingDivisionId=pollingDivisionId,
            count=count,
            electionId=electionId
        )

    @hybrid_property
    def pollingDivisions(self):
        return self.submission.area.get_associated_areas(
            areaType=AreaTypeEnum.PollingDivision, electionId=self.submission.electionId
        )

    def area_wise_valid_vote_count(self):
        return db.session.query(
            TallySheetVersionRow_PRE_30_ED.Model.pollingDivisionId.label("areaId"),
            func.sum(TallySheetVersionRow_PRE_30_ED.Model.count).label("validVoteCount")
        ).group_by(
            TallySheetVersionRow_PRE_30_ED.Model.pollingDivisionId
        ).filter(
            TallySheetVersionRow_PRE_30_ED.Model.tallySheetVersionId == self.tallySheetVersionId
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
        ).filter(
            Area.Model.areaId.in_([area.areaId for area in self.pollingDivisions])
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
            Area.Model.areaId.in_([area.areaId for area in self.pollingDivisions])
        ).one_or_none()

    @hybrid_property
    def content(self):
        return db.session.query(
            ElectionCandidate.Model.candidateId,
            Election.Model.electionId,
            Election.Model.electionName,
            Election.Model.voteType,
            Candidate.Model.candidateName,
            Area.Model.areaId.label("pollingDivisionId"),
            Area.Model.areaName.label("pollingDivisionName"),
            func.sum(TallySheetVersionRow_PRE_30_ED.Model.count).label("count"),
        ).join(
            Candidate.Model,
            Candidate.Model.candidateId == ElectionCandidate.Model.candidateId
        ).join(
            Party.Model,
            Party.Model.partyId == ElectionCandidate.Model.partyId
        ).join(
            Area.Model,
            and_(
                Area.Model.electionId == ElectionCandidate.Model.electionId,
                Area.Model.areaId.in_([area.areaId for area in self.pollingDivisions])
            )
        ).join(
            Election.Model,
            Election.Model.parentElectionId == ElectionCandidate.Model.electionId
        ).join(
            TallySheetVersionRow_PRE_30_ED.Model,
            and_(
                TallySheetVersionRow_PRE_30_ED.Model.electionId == Election.Model.electionId,
                TallySheetVersionRow_PRE_30_ED.Model.tallySheetVersionId == self.tallySheetVersionId,
                TallySheetVersionRow_PRE_30_ED.Model.pollingDivisionId == Area.Model.areaId,
                TallySheetVersionRow_PRE_30_ED.Model.candidateId == ElectionCandidate.Model.candidateId
            ),
            isouter=True
        ).filter(
            ElectionCandidate.Model.electionId == self.submission.electionId
        ).group_by(
            ElectionCandidate.Model.candidateId,
            Election.Model.electionId,
            Area.Model.areaId
        ).order_by(
            Election.Model.electionName,
            ElectionCandidate.Model.candidateId,
            Area.Model.areaId
        )

    def html(self):

        content = {
            "electoralDistrict": self.submission.area.areaName,
            "pollingDivisions": [],
            "data": [],
            "validVotes": [],
            "rejectedVotes": [],
            "totalVotes": []
        }

        tally_sheet_content_subquery = self.content.subquery()

        postal_vote_results = db.session.query(
            tally_sheet_content_subquery.c.candidateId,
            tally_sheet_content_subquery.c.candidateName,
            func.sum(tally_sheet_content_subquery.c.count).label("count")
        ).group_by(
            tally_sheet_content_subquery.c.candidateId
        ).filter(
            tally_sheet_content_subquery.c.voteType == VoteTypeEnum.Postal
        ).order_by(
            tally_sheet_content_subquery.c.candidateId
        ).all()

        non_postal_vote_results = db.session.query(
            tally_sheet_content_subquery.c.candidateId,
            tally_sheet_content_subquery.c.candidateName,
            tally_sheet_content_subquery.c.pollingDivisionId,
            tally_sheet_content_subquery.c.pollingDivisionName,
            func.sum(tally_sheet_content_subquery.c.count).label("count")
        ).group_by(
            tally_sheet_content_subquery.c.candidateId,
            tally_sheet_content_subquery.c.pollingDivisionId
        ).filter(
            tally_sheet_content_subquery.c.voteType == VoteTypeEnum.NonPostal
        ).order_by(
            tally_sheet_content_subquery.c.candidateId,
            tally_sheet_content_subquery.c.pollingDivisionId
        ).all()

        countingCentreCount = int(len(non_postal_vote_results) / len(postal_vote_results))

        # Fill the validVotes, rejectedVotes and totalVotes with zeros.
        for i in range(0, countingCentreCount):
            content["pollingDivisions"].append(non_postal_vote_results[i].pollingDivisionName)

            content["validVotes"].append(0)
            content["rejectedVotes"].append(0)
            content["totalVotes"].append(0)

        total_postal_vote_count = 0
        # Iterate by candidates.
        for i in range(len(postal_vote_results)):
            postal_vote_counts_row = postal_vote_results[i]

            # Append candidate details.
            data_row = [
                i + 1,
                postal_vote_counts_row.candidateName
            ]
            content["data"].append(data_row)
            total_count_per_candidate = 0

            # Iterate by counting centres.
            for j in range(countingCentreCount):
                # Determine the result index mapping with the counting centre and candidate.
                query_result_index = (i * countingCentreCount) + j

                count = non_postal_vote_results[query_result_index].count

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

            total_postal_vote_count_per_candidate = ""
            if postal_vote_counts_row.count is not None:
                total_postal_vote_count_per_candidate = postal_vote_counts_row.count
                total_count_per_candidate = total_count_per_candidate + total_postal_vote_count_per_candidate
                total_postal_vote_count = total_postal_vote_count + total_postal_vote_count_per_candidate
            data_row.append(total_postal_vote_count_per_candidate)

            data_row.append(total_count_per_candidate)

        content["validVotes"].append(total_postal_vote_count)
        content["rejectedVotes"].append(0)  # TODO
        content["totalVotes"].append(total_postal_vote_count + 0)  # TODO

        content["validVotes"].append(sum(content["validVotes"]))
        content["rejectedVotes"].append(sum(content["rejectedVotes"]))
        content["totalVotes"].append(sum(content["totalVotes"]))

        html = render_template(
            'PRE-30-ED.html',
            content=content
        )

        return html


Model = TallySheetVersion_PRE_30_ED_Model


def get_all(tallySheetId):
    query = Model.query.filter(Model.tallySheetId == tallySheetId)

    result = get_paginated_query(query).all()

    return result


def get_by_id(tallySheetId, tallySheetVersionId):
    tallySheet = TallySheet.get_by_id(tallySheetId=tallySheetId)
    if tallySheet is None:
        raise NotFoundException("Tally sheet not found. (tallySheetId=%d)" % tallySheetId)
    elif tallySheet.tallySheetCode is not TallySheetCodeEnum.PRE_30_ED:
        raise NotFoundException("Requested version not found. (tallySheetId=%d)" % tallySheetId)

    result = Model.query.filter(
        Model.tallySheetVersionId == tallySheetVersionId
    ).one_or_none()

    return result


def create(tallySheetId):
    result = Model(tallySheetId=tallySheetId)

    return result
