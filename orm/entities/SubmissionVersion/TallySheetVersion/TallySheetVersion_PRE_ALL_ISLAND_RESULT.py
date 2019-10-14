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
from util import get_paginated_query, to_comma_seperated_num, to_percentage, sqlalchemy_num_or_zero

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
            func.sum(
                TallySheetVersionRow_PRE_ALL_ISLAND_RESULT.Model.count
            ).label("validVoteCount"),
            func.sum(
                (TallySheetVersionRow_PRE_ALL_ISLAND_RESULT.Model.count / valid_vote_count_result.validVoteCount) * 100
                # (sqlalchemy_num_or_zero(TallySheetVersionRow_PRE_ALL_ISLAND_RESULT.Model.count) /
                #  sqlalchemy_num_or_zero(valid_vote_count_result.validVoteCount)) * 100
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
            func.sum(
                sqlalchemy_num_or_zero(TallySheetVersionRow_RejectedVoteCount.Model.rejectedVoteCount)
            ).label("rejectedVoteCount"),
        ).filter(
            TallySheetVersionRow_RejectedVoteCount.Model.tallySheetVersionId == self.tallySheetVersionId
        )

    def valid_vote_count_query(self):
        return db.session.query(
            func.count(ElectionCandidate.Model.candidateId).label("candidateCount"),
            func.sum(
                sqlalchemy_num_or_zero(TallySheetVersionRow_PRE_ALL_ISLAND_RESULT.Model.count)
            ).label("validVoteCount")
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

        total_vote_count = valid_vote_count_result.validVoteCount
        if rejected_vote_count_result.rejectedVoteCount is not None:
            total_vote_count = total_vote_count + rejected_vote_count_result.rejectedVoteCount

        vote_count_result = {
            "validVoteCount": valid_vote_count_result.validVoteCount,
            "validVoteCountPercentage": None,
            "rejectedVoteCount": rejected_vote_count_result.rejectedVoteCount,
            "rejectedVoteCountPercentage": None,
            "totalVoteCount": total_vote_count,
            "totalVoteCountPercentage": None
        }

        if registered_voters_count > 0:
            vote_count_result["validVoteCountPercentage"] = (valid_vote_count_result.validVoteCount /
                                                             registered_voters_count) * 100
            vote_count_result["totalVoteCountPercentage"] = (total_vote_count / registered_voters_count) * 100

            if rejected_vote_count_result.rejectedVoteCount is not None:
                vote_count_result["rejectedVoteCountPercentage"] = (rejected_vote_count_result.rejectedVoteCount /
                                                                    registered_voters_count) * 100

        return vote_count_result

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

        html = render_template(
            'PRE_ALL_ISLAND_RESULTS.html',
            content=content
        )

        return html


Model = TallySheetVersion_PRE_ALL_ISLAND_RESULT_Model
