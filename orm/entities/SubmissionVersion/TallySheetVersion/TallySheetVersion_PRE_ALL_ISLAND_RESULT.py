import datetime

from flask import render_template
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy import func

from app import db
from exception import NotFoundException
from orm.entities import Candidate, Party, Area
from orm.entities.Election import ElectionCandidate
from orm.entities.SubmissionVersion import TallySheetVersion
from orm.entities.TallySheetVersionRow import TallySheetVersionRow_PRE_ALL_ISLAND_RESULT, \
    TallySheetVersionRow_RejectedVoteCount
from util import get_paginated_query, to_comma_seperated_num, to_percentage

from orm.entities.Submission import TallySheet
from orm.enums import TallySheetCodeEnum, AreaTypeEnum
from sqlalchemy import and_


class TallySheetVersion_PRE_ALL_ISLAND_RESULT_Model(TallySheetVersion.Model):

    def __init__(self, tallySheetId):
        super(TallySheetVersion_PRE_ALL_ISLAND_RESULT_Model, self).__init__(
            tallySheetId=tallySheetId
        )

    __mapper_args__ = {
        'polymorphic_identity': TallySheetCodeEnum.PRE_ALL_ISLAND_RESULTS
    }

    def add_row(self, candidateId, count):
        from orm.entities.TallySheetVersionRow import TallySheetVersionRow_PRE_ALL_ISLAND_RESULT

        TallySheetVersionRow_PRE_ALL_ISLAND_RESULT.create(
            tallySheetVersionId=self.tallySheetVersionId,
            candidateId=candidateId,
            count=count
        )

    @hybrid_property
    def electoralDistricts(self):
        return self.submission.area.get_associated_areas(
            areaType=AreaTypeEnum.ElectoralDistrict, electionId=self.submission.electionId
        )

    def candidate_wise_valid_vote_count_query(self):
        valid_vote_count_result = self.valid_vote_count_query().one_or_none()

        return db.session.query(
            ElectionCandidate.Model.candidateId,
            Candidate.Model.candidateName,
            Party.Model.partySymbol,
            Party.Model.partyAbbreviation,
            func.sum(TallySheetVersionRow_PRE_ALL_ISLAND_RESULT.Model.count).label("validVoteCount"),
            func.sum(
                (TallySheetVersionRow_PRE_ALL_ISLAND_RESULT.Model.count / valid_vote_count_result.validVoteCount) * 100
            ).label("validVotePercentage")
        ).join(
            TallySheetVersionRow_PRE_ALL_ISLAND_RESULT.Model,
            and_(
                TallySheetVersionRow_PRE_ALL_ISLAND_RESULT.Model.candidateId == ElectionCandidate.Model.candidateId,
                TallySheetVersionRow_PRE_ALL_ISLAND_RESULT.Model.tallySheetVersionId == self.tallySheetVersionId,
            ),
            isouter=True
        ).join(
            Candidate.Model,
            Candidate.Model.candidateId == ElectionCandidate.Model.candidateId,
            isouter=True
        ).join(
            Party.Model,
            Party.Model.partyId == ElectionCandidate.Model.partyId,
            isouter=True
        ).group_by(
            ElectionCandidate.Model.candidateId
        ).filter(
            ElectionCandidate.Model.electionId == self.submission.electionId
        )

    def rejected_vote_count_query(self):
        return db.session.query(
            func.sum(TallySheetVersionRow_RejectedVoteCount.Model.rejectedVoteCount).label("rejectedVoteCount"),
        ).filter(
            TallySheetVersionRow_RejectedVoteCount.Model.tallySheetVersionId == self.tallySheetVersionId
        )

    def valid_vote_count_query(self):
        return db.session.query(
            func.count(ElectionCandidate.Model.candidateId).label("candidateCount"),
            func.sum(TallySheetVersionRow_PRE_ALL_ISLAND_RESULT.Model.count).label("validVoteCount")
        ).join(
            TallySheetVersionRow_PRE_ALL_ISLAND_RESULT.Model,
            and_(
                TallySheetVersionRow_PRE_ALL_ISLAND_RESULT.Model.candidateId == ElectionCandidate.Model.candidateId,
                TallySheetVersionRow_PRE_ALL_ISLAND_RESULT.Model.tallySheetVersionId == self.tallySheetVersionId,
            ),
            isouter=True
        ).filter(
            ElectionCandidate.Model.electionId == self.submission.electionId
        )

    def vote_count_result(self):
        registered_voters_count = self.submission.area.registeredVotersCount

        valid_vote_count_result = self.valid_vote_count_query().one_or_none()
        rejected_vote_count_result = self.rejected_vote_count_query().one_or_none()

        return {
            "validVoteCount": valid_vote_count_result.validVoteCount,
            "validVoteCountPercentage": (valid_vote_count_result.validVoteCount / registered_voters_count) * 100,
            "rejectedVoteCount": rejected_vote_count_result.rejectedVoteCount,
            "rejectedVoteCountPercentage": (rejected_vote_count_result.rejectedVoteCount /
                                            registered_voters_count) * 100,
            "totalVoteCount": (valid_vote_count_result.validVoteCount + rejected_vote_count_result.rejectedVoteCount),
            "totalVoteCountPercentage": ((valid_vote_count_result.validVoteCount +
                                          rejected_vote_count_result.rejectedVoteCount) / registered_voters_count) * 100
        }

        # valid_and_rejected_vote_count_subquery = self.valid_vote_count_query().union(
        #     self.rejected_vote_count_query()
        # ).subquery()
        #
        # return db.session.query(
        #     func.sum(valid_and_rejected_vote_count_subquery.c.validVoteCount).label("validVoteCount"),
        #     func.sum(
        #         (valid_and_rejected_vote_count_subquery.c.validVoteCount / registered_voters_count) * 100
        #     ).label("validVoteCountPercentage"),
        #     func.sum(valid_and_rejected_vote_count_subquery.c.rejectedVoteCount).label("rejectedVoteCount"),
        #     func.sum(
        #         (valid_and_rejected_vote_count_subquery.c.rejectedVoteCount / registered_voters_count) * 100
        #     ).label("validVoteCountPercentage"),
        #     func.sum(
        #         valid_and_rejected_vote_count_subquery.c.validVoteCount +
        #         valid_and_rejected_vote_count_subquery.c.rejectedVoteCount
        #     ).label("totalVoteCount"),
        #     func.sum(
        #         ((valid_and_rejected_vote_count_subquery.c.validVoteCount +
        #           valid_and_rejected_vote_count_subquery.c.rejectedVoteCount) / registered_voters_count) * 100
        #     ).label("totalVoteCountPercentage")
        # )

    @hybrid_property
    def content(self):
        return db.session.query(
            ElectionCandidate.Model.candidateId,
            Candidate.Model.candidateName,
            Party.Model.partySymbol,
            Party.Model.partyAbbreviation,
            TallySheetVersionRow_PRE_ALL_ISLAND_RESULT.Model.count
        ).join(
            TallySheetVersionRow_PRE_ALL_ISLAND_RESULT.Model,
            and_(
                TallySheetVersionRow_PRE_ALL_ISLAND_RESULT.Model.candidateId == ElectionCandidate.Model.candidateId,
                TallySheetVersionRow_PRE_ALL_ISLAND_RESULT.Model.tallySheetVersionId == self.tallySheetVersionId,
            ),
            isouter=True
        ).join(
            Candidate.Model,
            Candidate.Model.candidateId == ElectionCandidate.Model.candidateId,
            isouter=True
        ).join(
            Party.Model,
            Party.Model.partyId == ElectionCandidate.Model.partyId,
            isouter=True
        ).filter(
            ElectionCandidate.Model.electionId == self.submission.electionId
        ).all()

    def html(self):
        tallySheetContent = self.content

        content = {
            "date": self.submissionVersion.createdAt.strftime("%d/%m/%Y"),
            "time": self.submissionVersion.createdAt.strftime("%H:%M:%S %p"),
            "data": [
            ],
            "validVoteCounts": [0, 0],
            "rejectedVoteCounts": [0, 0],
            "totalVoteCounts": [0, 0],
            "registeredVoters": [
                to_comma_seperated_num(self.submission.area.registeredVotersCount),
                100
            ]
        }

        candidate_wise_valid_vote_count_result = self.candidate_wise_valid_vote_count_query().all()
        vote_count_result = self.vote_count_result()

        for candidate_wise_valid_vote_count_result_item in candidate_wise_valid_vote_count_result:
            content["data"].append([
                candidate_wise_valid_vote_count_result_item.candidateName,
                candidate_wise_valid_vote_count_result_item.partyAbbreviation,
                to_comma_seperated_num(candidate_wise_valid_vote_count_result_item.validVoteCount),
                to_percentage(candidate_wise_valid_vote_count_result_item.validVotePercentage)
            ])

        content["validVoteCounts"] = [
            to_comma_seperated_num(vote_count_result["validVoteCount"]),
            to_percentage(vote_count_result["validVoteCountPercentage"])
        ]

        content["rejectedVoteCounts"] = [
            to_comma_seperated_num(vote_count_result["rejectedVoteCount"]),
            to_percentage(vote_count_result["rejectedVoteCountPercentage"])
        ]

        content["totalVoteCounts"] = [
            to_comma_seperated_num(vote_count_result["totalVoteCount"]),
            to_percentage(vote_count_result["totalVoteCountPercentage"])
        ]

        # for row_index in range(len(tallySheetContent)):
        #     row = tallySheetContent[row_index]
        #     if row.count is not None:
        #         content["data"].append([
        #             row.candidateName,
        #             row.partyAbbreviation,
        #             row.count,
        #             0
        #         ])
        #         content["validVotes"][0] = content["validVotes"][0] + row.count
        #     else:
        #         content["data"].append([
        #             row.candidateName,
        #             row.partyAbbreviation,
        #             "",
        #             0
        #         ])

        # Calculate the candidate wise votes percentage based on total valid votes.
        # for row_index in range(len(content["data"])):
        #     if content["data"][row_index][2] is not "":
        #         content["data"][row_index][3] = round(
        #             (content["data"][row_index][2] / content["validVotes"][0]) * 100, 2
        #         )
        #         content["data"][row_index][2] = f'{content["data"][row_index][2]:,}'

        # TODO append the rejected votes count.
        # content["rejectedVotes"][0] = 0  # TODO

        # # Calculate the total polled.
        # content["totalPolled"][0] = content["validVotes"][0] + content["rejectedVotes"][0]
        #
        # # Calculate the percentage of valid votes based on total registered voters.
        # content["validVotes"][1] = round((content["validVotes"][0] / content["registeredVoters"][0]) * 100, 2)
        #
        # # Calculate the percentage of rejected votes based on total registered voters.
        # content["rejectedVotes"][1] = round((content["rejectedVotes"][0] / content["registeredVoters"][0]) * 100, 2)
        #
        # # Calculate the percentage of total polled based on total registered voters.
        # content["totalPolled"][1] = round((content["totalPolled"][0] / content["registeredVoters"][0]) * 100, 2)

        html = render_template(
            'PRE_ALL_ISLAND_RESULTS.html',
            content=content
        )

        return html


Model = TallySheetVersion_PRE_ALL_ISLAND_RESULT_Model


def get_all(tallySheetId):
    query = Model.query.filter(Model.tallySheetId == tallySheetId)

    result = get_paginated_query(query).all()

    return result


def get_by_id(tallySheetId, tallySheetVersionId):
    tallySheet = TallySheet.get_by_id(tallySheetId=tallySheetId)
    if tallySheet is None:
        raise NotFoundException("Tally sheet not found. (tallySheetId=%d)" % tallySheetId)
    elif tallySheet.tallySheetCode is not TallySheetCodeEnum.PRE_ALL_ISLAND_RESULTS:
        raise NotFoundException("Requested version not found. (tallySheetId=%d)" % tallySheetId)

    result = Model.query.filter(
        Model.tallySheetVersionId == tallySheetVersionId
    ).one_or_none()

    return result


def create(tallySheetId):
    result = Model(tallySheetId=tallySheetId)

    return result
