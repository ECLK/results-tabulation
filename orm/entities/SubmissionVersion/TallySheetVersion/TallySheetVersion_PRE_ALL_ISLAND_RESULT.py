from flask import render_template, url_for
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func
from app import db
from orm.entities import Candidate, Party, Area
from orm.entities.Election import ElectionCandidate
from orm.entities.SubmissionVersion import TallySheetVersion
from orm.entities.TallySheetVersionRow import TallySheetVersionRow_PRE_ALL_ISLAND_RESULT, \
    TallySheetVersionRow_RejectedVoteCount
from util import to_comma_seperated_num, to_percentage, sqlalchemy_num_or_zero, convert_image_to_data_uri
from orm.enums import TallySheetCodeEnum, AreaTypeEnum
from sqlalchemy import and_
from datetime import datetime
import operator


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
        electoralDistricts = db.session.query(
            Area.Model
        ).filter(
            Area.Model.areaType == AreaTypeEnum.ElectoralDistrict,
            Area.Model.electionId == self.submission.electionId
        ).all()

        return electoralDistricts

    def candidate_wise_valid_vote_count_query(self):
        valid_vote_count_result = self.valid_vote_count_query().one_or_none()

        return db.session.query(
            ElectionCandidate.Model.candidateId,
            Candidate.Model.candidateName,
            Party.Model.partySymbol,
            Party.Model.partyAbbreviation,
            Party.Model.partyName,
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
                                                             total_vote_count) * 100
            vote_count_result["totalVoteCountPercentage"] = (total_vote_count / registered_voters_count) * 100

            if rejected_vote_count_result.rejectedVoteCount is not None:
                vote_count_result["rejectedVoteCountPercentage"] = (rejected_vote_count_result.rejectedVoteCount /
                                                                    total_vote_count) * 100

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

    def get_html_content_dict(self):
        tallySheetContent = self.content
        stamp = self.stamp

        content = {
            "resultTitle": "ALL ISLAND RESULT",
            "election": {
                "electionName": self.submission.election.get_official_name()
            },
            "stamp": {
                "createdAt": stamp.createdAt,
                "createdBy": stamp.createdBy,
                "barcodeString": stamp.barcodeString
            },
            "date": stamp.createdAt.strftime("%d/%m/%Y"),
            "time": stamp.createdAt.strftime("%H:%M:%S %p"),
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
                to_percentage(candidate_wise_valid_vote_count_result_item.validVotePercentage),
                candidate_wise_valid_vote_count_result_item.validVoteCount
            ])

        content['data'] = sorted(content['data'], key=operator.itemgetter(4), reverse=True)
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

        content["logo"] = convert_image_to_data_uri("static/Emblem_of_Sri_Lanka.png")

        return content

    def html_letter(self):
        html = render_template(
            'PRE_ALL_ISLAND_RESULTS.html',
            content=self.get_html_content_dict()
        )

        return html

    def html(self):
        html = render_template(
            'PRE_ALL_ISLAND_RESULTS.html',
            content=self.get_html_content_dict()
        )

        return html

    def json_data(self):

        total_registered_voters = self.submission.area.registeredVotersCount

        candidate_wise_vote_count_result = self.candidate_wise_valid_vote_count_query().all()
        vote_count_result = self.vote_count_result()

        candidates = []
        for candidate_wise_valid_vote_count_result_item in candidate_wise_vote_count_result:
            candidates.append({
                "party_code": candidate_wise_valid_vote_count_result_item.partyAbbreviation,
                "votes": str(candidate_wise_valid_vote_count_result_item.validVoteCount),
                "percentage": f'{round(candidate_wise_valid_vote_count_result_item.validVotePercentage or 0,2)}',
                "party_name": candidate_wise_valid_vote_count_result_item.partyName,
                "candidate": candidate_wise_valid_vote_count_result_item.candidateName
            })

        validVoteCount = vote_count_result['validVoteCount'] or 0
        rejectedVoteCount = vote_count_result['rejectedVoteCount'] or 0
        totalVoteCount = vote_count_result['totalVoteCount'] or 0

        response = {
            "timestamp": str(datetime.now()),
            "level": "ALL-ISLAND",
            "by_party": candidates,
            "summary": {
                "valid": str(validVoteCount),
                "rejected": str(rejectedVoteCount),
                "polled": str(totalVoteCount),
                "electors": str(total_registered_voters),
                "percent_valid": f'{round((validVoteCount * 100 / total_registered_voters), 2)}',
                "percent_rejected": f'{round((rejectedVoteCount * 100 / total_registered_voters), 2)}',
                "percent_polled": f'{round((totalVoteCount * 100 / total_registered_voters), 2)}',
            }
        }

        return response, "FINAL"


Model = TallySheetVersion_PRE_ALL_ISLAND_RESULT_Model
