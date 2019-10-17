from flask import render_template
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func, and_, or_
from app import db
from orm.entities import Area, Candidate, Party, Election
from orm.entities.Election import ElectionCandidate
from orm.entities.SubmissionVersion import TallySheetVersion
from orm.entities.TallySheetVersionRow import TallySheetVersionRow_PRE_30_ED, TallySheetVersionRow_RejectedVoteCount
from util import to_comma_seperated_num, sqlalchemy_num_or_zero
from orm.enums import TallySheetCodeEnum, AreaTypeEnum, VoteTypeEnum


class TallySheetVersion_PRE_30_ED_Model(TallySheetVersion.Model):

    def __init__(self, tallySheetId):
        super(TallySheetVersion_PRE_30_ED_Model, self).__init__(
            tallySheetId=tallySheetId
        )

    __mapper_args__ = {
        'polymorphic_identity': TallySheetCodeEnum.PRE_30_ED
    }

    def add_row(self, areaId, candidateId, count, electionId):
        from orm.entities.TallySheetVersionRow import TallySheetVersionRow_PRE_30_ED

        TallySheetVersionRow_PRE_30_ED.create(
            tallySheetVersionId=self.tallySheetVersionId,
            candidateId=candidateId,
            areaId=areaId,
            count=count,
            electionId=electionId
        )

    @hybrid_property
    def pollingDivisions(self):
        return self.submission.area.get_associated_areas(
            areaType=AreaTypeEnum.PollingDivision, electionId=self.submission.electionId
        )

    def polling_division_and_electoral_district_query(self):
        electoral_district = self.submission.area

        polling_divisions_query = electoral_district.get_associated_areas_query(
            AreaTypeEnum.PollingDivision).subquery()

        return db.session.query(
            Area.Model
        ).join(
            polling_divisions_query,
            polling_divisions_query.c.areaId == Area.Model.areaId,
            isouter=True
        ).filter(
            or_(
                Area.Model.areaId == electoral_district.areaId,
                Area.Model.areaId == polling_divisions_query.c.areaId
            )
        )

    def non_postal_area_wise_rejected_vote_count_query(self):
        return db.session.query(
            Election.Model.voteType,
            Area.Model.areaId,
            Area.Model.areaName,
            func.sum(TallySheetVersionRow_RejectedVoteCount.Model.rejectedVoteCount).label("rejectedVoteCount"),
        ).join(
            Area.Model,
            and_(
                Area.Model.electionId == Election.Model.parentElectionId,
                Area.Model.areaId.in_([area.areaId for area in self.pollingDivisions])
            )
        ).join(
            TallySheetVersionRow_RejectedVoteCount.Model,
            and_(
                TallySheetVersionRow_RejectedVoteCount.Model.electionId == Election.Model.electionId,
                TallySheetVersionRow_RejectedVoteCount.Model.tallySheetVersionId == self.tallySheetVersionId,
                TallySheetVersionRow_RejectedVoteCount.Model.areaId == Area.Model.areaId,
                TallySheetVersionRow_RejectedVoteCount.Model.candidateId == None
            ),
            isouter=True
        ).filter(
            Election.Model.parentElectionId == self.submission.electionId,
            Election.Model.voteType == VoteTypeEnum.NonPostal,
        ).group_by(
            Area.Model.areaId
        ).order_by(
            Area.Model.areaName
        )

    def postal_area_wise_rejected_vote_count_query(self):
        return db.session.query(
            Election.Model.voteType,
            Area.Model.areaId,
            Area.Model.areaName,
            func.sum(TallySheetVersionRow_RejectedVoteCount.Model.rejectedVoteCount).label("rejectedVoteCount"),
        ).join(
            Area.Model,
            and_(
                Area.Model.electionId == Election.Model.parentElectionId,
                Area.Model.areaId == self.submission.areaId
            )
        ).join(
            TallySheetVersionRow_RejectedVoteCount.Model,
            and_(
                TallySheetVersionRow_RejectedVoteCount.Model.electionId == Election.Model.electionId,
                TallySheetVersionRow_RejectedVoteCount.Model.tallySheetVersionId == self.tallySheetVersionId,
                TallySheetVersionRow_RejectedVoteCount.Model.areaId == Area.Model.areaId,
                TallySheetVersionRow_RejectedVoteCount.Model.candidateId == None
            ),
            isouter=True
        ).filter(
            Election.Model.parentElectionId == self.submission.electionId,
            Election.Model.voteType == VoteTypeEnum.Postal,
        ).group_by(
            Area.Model.areaId
        ).order_by(
            Area.Model.areaName
        )

    def non_postal_candidate_and_area_wise_valid_vote_count_query(self):
        return db.session.query(
            ElectionCandidate.Model.candidateId,
            Candidate.Model.candidateName,
            Area.Model.areaId,
            Area.Model.areaName,
            func.sum(TallySheetVersionRow_PRE_30_ED.Model.count).label("validVoteCount"),
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
                TallySheetVersionRow_PRE_30_ED.Model.areaId == Area.Model.areaId,
                TallySheetVersionRow_PRE_30_ED.Model.candidateId == ElectionCandidate.Model.candidateId
            ),
            isouter=True
        ).filter(
            ElectionCandidate.Model.electionId == self.submission.electionId,
            Election.Model.voteType == VoteTypeEnum.NonPostal,
        ).group_by(
            ElectionCandidate.Model.candidateId,
            Area.Model.areaId
        ).order_by(
            ElectionCandidate.Model.candidateId,
            Area.Model.areaName
        )

    def non_postal_area_wise_valid_vote_count_query(self):
        non_postal_candidate_and_area_wise_valid_vote_count_subquery = self.non_postal_candidate_and_area_wise_valid_vote_count_query().subquery()

        return db.session.query(
            non_postal_candidate_and_area_wise_valid_vote_count_subquery.c.areaId,
            non_postal_candidate_and_area_wise_valid_vote_count_subquery.c.areaName,
            func.sum(
                sqlalchemy_num_or_zero(non_postal_candidate_and_area_wise_valid_vote_count_subquery.c.validVoteCount)
            ).label("validVoteCount"),
        ).group_by(
            non_postal_candidate_and_area_wise_valid_vote_count_subquery.c.areaId
        ).order_by(
            non_postal_candidate_and_area_wise_valid_vote_count_subquery.c.areaName
        )

    def postal_candidate_and_area_wise_valid_vote_count_query(self):
        return db.session.query(
            ElectionCandidate.Model.candidateId,
            Candidate.Model.candidateName,
            Area.Model.areaId,
            Area.Model.areaName,
            func.sum(TallySheetVersionRow_PRE_30_ED.Model.count).label("validVoteCount"),
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
                Area.Model.areaId == self.submission.areaId
            )
        ).join(
            Election.Model,
            Election.Model.parentElectionId == ElectionCandidate.Model.electionId
        ).join(
            TallySheetVersionRow_PRE_30_ED.Model,
            and_(
                TallySheetVersionRow_PRE_30_ED.Model.electionId == Election.Model.electionId,
                TallySheetVersionRow_PRE_30_ED.Model.tallySheetVersionId == self.tallySheetVersionId,
                TallySheetVersionRow_PRE_30_ED.Model.areaId == Area.Model.areaId,
                TallySheetVersionRow_PRE_30_ED.Model.candidateId == ElectionCandidate.Model.candidateId
            ),
            isouter=True
        ).filter(
            ElectionCandidate.Model.electionId == self.submission.electionId,
            Election.Model.voteType == VoteTypeEnum.Postal,
        ).group_by(
            ElectionCandidate.Model.candidateId,
            Area.Model.areaId
        ).order_by(
            ElectionCandidate.Model.candidateId,
            Area.Model.areaName
        )

    def postal_area_wise_valid_vote_count_query(self):
        postal_candidate_and_area_wise_valid_vote_count_subquery = self.postal_candidate_and_area_wise_valid_vote_count_query().subquery()

        return db.session.query(
            postal_candidate_and_area_wise_valid_vote_count_subquery.c.areaId,
            postal_candidate_and_area_wise_valid_vote_count_subquery.c.areaName,
            func.sum(
                sqlalchemy_num_or_zero(postal_candidate_and_area_wise_valid_vote_count_subquery.c.validVoteCount)
            ).label("validVoteCount"),
        ).group_by(
            postal_candidate_and_area_wise_valid_vote_count_subquery.c.areaId
        ).order_by(
            postal_candidate_and_area_wise_valid_vote_count_subquery.c.areaName
        )

    def postal_area_wise_vote_count_query(self):
        postal_area_wise_valid_vote_count_subquery = self.postal_area_wise_valid_vote_count_query().subquery()
        postal_area_wise_rejected_vote_count_subquery = self.postal_area_wise_rejected_vote_count_query().subquery()

        return db.session.query(
            postal_area_wise_valid_vote_count_subquery.c.areaId,
            postal_area_wise_valid_vote_count_subquery.c.areaName,
            func.sum(
                sqlalchemy_num_or_zero(postal_area_wise_valid_vote_count_subquery.c.validVoteCount)
            ).label("validVoteCount"),
            func.sum(
                postal_area_wise_rejected_vote_count_subquery.c.rejectedVoteCount
            ).label("rejectedVoteCount"),
            func.sum(
                sqlalchemy_num_or_zero(postal_area_wise_valid_vote_count_subquery.c.validVoteCount) +
                sqlalchemy_num_or_zero(postal_area_wise_rejected_vote_count_subquery.c.rejectedVoteCount)
            ).label("totalVoteCount")
        ).join(
            postal_area_wise_rejected_vote_count_subquery,
            postal_area_wise_rejected_vote_count_subquery.c.areaId == postal_area_wise_valid_vote_count_subquery.c.areaId
        ).group_by(
            postal_area_wise_valid_vote_count_subquery.c.areaId
        )

    def non_postal_area_wise_vote_count_query(self):
        non_postal_area_wise_valid_vote_count_subquery = self.non_postal_area_wise_valid_vote_count_query().subquery()
        non_postal_area_wise_rejected_vote_count_subquery = self.non_postal_area_wise_rejected_vote_count_query().subquery()

        return db.session.query(
            non_postal_area_wise_valid_vote_count_subquery.c.areaId,
            non_postal_area_wise_valid_vote_count_subquery.c.areaName,
            func.sum(
                sqlalchemy_num_or_zero(non_postal_area_wise_valid_vote_count_subquery.c.validVoteCount)
            ).label("validVoteCount"),
            func.sum(
                non_postal_area_wise_rejected_vote_count_subquery.c.rejectedVoteCount
            ).label("rejectedVoteCount"),
            func.sum(
                sqlalchemy_num_or_zero(non_postal_area_wise_valid_vote_count_subquery.c.validVoteCount) +
                sqlalchemy_num_or_zero(non_postal_area_wise_rejected_vote_count_subquery.c.rejectedVoteCount)
            ).label("totalVoteCount")
        ).join(
            non_postal_area_wise_rejected_vote_count_subquery,
            non_postal_area_wise_rejected_vote_count_subquery.c.areaId == non_postal_area_wise_valid_vote_count_subquery.c.areaId
        ).group_by(
            non_postal_area_wise_valid_vote_count_subquery.c.areaId
        )

    def candidate_wise_vote_count(self):
        non_postal_candidate_and_area_wise_valid_vote_count_subquery = self.non_postal_candidate_and_area_wise_valid_vote_count_query().subquery()
        postal_candidate_and_area_wise_valid_vote_count_subquery = self.postal_candidate_and_area_wise_valid_vote_count_query().subquery()

        return db.session.query(
            non_postal_candidate_and_area_wise_valid_vote_count_subquery.c.candidateId,
            non_postal_candidate_and_area_wise_valid_vote_count_subquery.c.candidateName,
            func.sum(
                sqlalchemy_num_or_zero(non_postal_candidate_and_area_wise_valid_vote_count_subquery.c.validVoteCount)
            ).label("nonPostalValidVoteCount"),
            func.sum(
                sqlalchemy_num_or_zero(postal_candidate_and_area_wise_valid_vote_count_subquery.c.validVoteCount)
            ).label("postalValidVoteCount"),
            func.sum(
                sqlalchemy_num_or_zero(non_postal_candidate_and_area_wise_valid_vote_count_subquery.c.validVoteCount) +
                sqlalchemy_num_or_zero(postal_candidate_and_area_wise_valid_vote_count_subquery.c.validVoteCount)
            ).label("validVoteCount")
        ).join(
            postal_candidate_and_area_wise_valid_vote_count_subquery,
            postal_candidate_and_area_wise_valid_vote_count_subquery.c.candidateId == non_postal_candidate_and_area_wise_valid_vote_count_subquery.c.candidateId
        ).group_by(
            non_postal_candidate_and_area_wise_valid_vote_count_subquery.c.candidateId
        ).group_by(
            non_postal_candidate_and_area_wise_valid_vote_count_subquery.c.candidateId
        )

    def vote_count_query(self):
        area_wise_vote_count_subquery = self.non_postal_area_wise_vote_count_query().union(
            self.postal_area_wise_vote_count_query()).subquery()

        return db.session.query(
            func.sum(
                sqlalchemy_num_or_zero(area_wise_vote_count_subquery.c.validVoteCount)
            ).label("validVoteCount"),
            func.sum(
                sqlalchemy_num_or_zero(area_wise_vote_count_subquery.c.rejectedVoteCount)
            ).label("rejectedVoteCount"),
            func.sum(
                sqlalchemy_num_or_zero(area_wise_vote_count_subquery.c.totalVoteCount)
            ).label("totalVoteCount")
        )

    @hybrid_property
    def content(self):
        return db.session.query(
            ElectionCandidate.Model.candidateId,
            Election.Model.electionId,
            Election.Model.electionName,
            Candidate.Model.candidateName,
            Area.Model.areaId,
            Area.Model.areaName,
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
                TallySheetVersionRow_PRE_30_ED.Model.areaId == Area.Model.areaId,
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
            Area.Model.areaName
        )

    def html(self):
        stamp = self.stamp

        content = {
            "election": {
                "electionname": self.submission.election.electionName
            },
            "stamp": {
                "createdAt": stamp.createdAt,
                "createdBy": stamp.createdBy,
                "barcodeString": stamp.barcodeString
            },
            "electoralDistrict": self.submission.area.areaName,
            "pollingDivisions": [],
            "data": [],
            "validVoteCounts": [],
            "rejectedVoteCounts": [],
            "totalVoteCounts": []
        }

        non_postal_candidate_and_area_wise_valid_vote_count_result = self.non_postal_candidate_and_area_wise_valid_vote_count_query().all()
        postal_candidate_and_area_wise_valid_vote_count_result = self.postal_candidate_and_area_wise_valid_vote_count_query().all()
        candidate_wise_vote_count_result = self.candidate_wise_vote_count().all()
        non_postal_area_wise_vote_count_result = self.non_postal_area_wise_vote_count_query().all()
        postal_area_wise_vote_count_result = self.postal_area_wise_vote_count_query().all()
        vote_count_result = self.vote_count_query().one_or_none()

        polling_division_count = len(non_postal_area_wise_vote_count_result)
        postal_polling_division_count = len(postal_area_wise_vote_count_result)
        number_of_candidates = len(candidate_wise_vote_count_result)

        for polling_division_index in range(polling_division_count):
            non_postal_area_wise_vote_count_result_item = non_postal_area_wise_vote_count_result[
                polling_division_index]
            content["pollingDivisions"].append(non_postal_area_wise_vote_count_result_item.areaName)
            content["rejectedVoteCounts"].append(
                to_comma_seperated_num(non_postal_area_wise_vote_count_result_item.rejectedVoteCount)
            )
            content["validVoteCounts"].append(
                to_comma_seperated_num(non_postal_area_wise_vote_count_result_item.validVoteCount)
            )
            content["totalVoteCounts"].append(
                to_comma_seperated_num(non_postal_area_wise_vote_count_result_item.totalVoteCount)
            )

        for postal_polling_division_index in range(postal_polling_division_count):
            postal_area_wise_vote_count_result_item = postal_area_wise_vote_count_result[
                postal_polling_division_index]
            content["rejectedVoteCounts"].append(
                to_comma_seperated_num(postal_area_wise_vote_count_result_item.rejectedVoteCount)
            )
            content["validVoteCounts"].append(
                to_comma_seperated_num(postal_area_wise_vote_count_result_item.validVoteCount)
            )
            content["totalVoteCounts"].append(
                to_comma_seperated_num(postal_area_wise_vote_count_result_item.totalVoteCount)
            )

        content["rejectedVoteCounts"].append(to_comma_seperated_num(vote_count_result.rejectedVoteCount))
        content["validVoteCounts"].append(to_comma_seperated_num(vote_count_result.validVoteCount))
        content["totalVoteCounts"].append(to_comma_seperated_num(vote_count_result.totalVoteCount))

        for candidate_wise_vote_count_result_item_index in range(number_of_candidates):
            data_row = []

            data_row_number = candidate_wise_vote_count_result_item_index + 1
            data_row.append(data_row_number)

            candidate_wise_vote_count_result_item = candidate_wise_vote_count_result[
                candidate_wise_vote_count_result_item_index
            ]
            data_row.append(candidate_wise_vote_count_result_item.candidateName)

            for polling_division_index in range(polling_division_count):
                non_postal_area_wise_valid_vote_count_result_item_index = (
                                                                                  candidate_wise_vote_count_result_item_index *
                                                                                  polling_division_count) + polling_division_index
                non_postal_candidate_and_area_wise_valid_vote_count_result_item = \
                    non_postal_candidate_and_area_wise_valid_vote_count_result[
                        non_postal_area_wise_valid_vote_count_result_item_index
                    ]
                data_row.append(to_comma_seperated_num(
                    non_postal_candidate_and_area_wise_valid_vote_count_result_item.validVoteCount))

            postal_candidate_and_area_wise_valid_vote_count_result_item = \
                postal_candidate_and_area_wise_valid_vote_count_result[
                    candidate_wise_vote_count_result_item_index
                ]
            data_row.append(
                to_comma_seperated_num(postal_candidate_and_area_wise_valid_vote_count_result_item.validVoteCount))
            data_row.append(to_comma_seperated_num(candidate_wise_vote_count_result_item.validVoteCount))

            content["data"].append(data_row)

        html = render_template(
            'PRE-30-ED.html',
            content=content
        )

        return html


Model = TallySheetVersion_PRE_30_ED_Model
