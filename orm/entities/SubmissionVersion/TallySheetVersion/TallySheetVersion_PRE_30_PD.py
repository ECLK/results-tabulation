from flask import render_template
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func, and_
from app import db
from orm.entities import Area, Candidate, Party, Election
from orm.entities.Election import ElectionCandidate
from orm.entities.SubmissionVersion import TallySheetVersion
from orm.entities.TallySheetVersionRow import TallySheetVersionRow_PRE_30_PD, TallySheetVersionRow_RejectedVoteCount
from util import to_comma_seperated_num, sqlalchemy_num_or_zero
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

    @hybrid_property
    def countingCentres(self):
        return self.submission.area.get_associated_areas(
            areaType=AreaTypeEnum.CountingCentre, electionId=self.submission.electionId
        )

    def add_area_order_by(self, query, column):
        if self.submission.election.voteType is VoteTypeEnum.Postal:
            # Because the counting centre names are not numbers. eg:- "PV 41", "PV 42"
            return query.order_by(
                column
            )
        elif self.submission.election.voteType is VoteTypeEnum.NonPostal:
            # Counting centre names are numbers. eg:- "34", "35", "36"
            return query.order_by(
                func.cast(column, db.Integer)
            )

    def area_wise_rejected_vote_count_query(self):
        query = db.session.query(
            Area.Model.areaId,
            Area.Model.areaName,
            func.sum(
                TallySheetVersionRow_RejectedVoteCount.Model.rejectedVoteCount
            ).label("rejectedVoteCount"),
        ).join(
            TallySheetVersionRow_RejectedVoteCount.Model,
            and_(
                TallySheetVersionRow_RejectedVoteCount.Model.tallySheetVersionId == self.tallySheetVersionId,
                TallySheetVersionRow_RejectedVoteCount.Model.areaId == Area.Model.areaId,
                TallySheetVersionRow_RejectedVoteCount.Model.candidateId == None
            ),
            isouter=True
        ).filter(
            Area.Model.areaId.in_([area.areaId for area in self.countingCentres])
        ).group_by(
            Area.Model.areaId
        )

        return self.add_area_order_by(query, Area.Model.areaName)

    def candidate_and_area_wise_valid_vote_count_query(self):
        query = db.session.query(
            Election.Model.electionId,
            ElectionCandidate.Model.candidateId,
            Candidate.Model.candidateName,
            Area.Model.areaId,
            Area.Model.areaName,
            func.sum(
                TallySheetVersionRow_PRE_30_PD.Model.count
            ).label("validVoteCount"),
        ).join(
            ElectionCandidate.Model,
            ElectionCandidate.Model.electionId == Election.Model.parentElectionId
        ).join(
            Candidate.Model,
            Candidate.Model.candidateId == ElectionCandidate.Model.candidateId
        ).join(
            Party.Model,
            Party.Model.partyId == ElectionCandidate.Model.partyId
        ).join(
            Area.Model,
            and_(
                Area.Model.electionId == Election.Model.electionId,
                Area.Model.areaId.in_([area.areaId for area in self.countingCentres])
            )
        ).join(
            TallySheetVersionRow_PRE_30_PD.Model,
            and_(
                TallySheetVersionRow_PRE_30_PD.Model.tallySheetVersionId == self.tallySheetVersionId,
                TallySheetVersionRow_PRE_30_PD.Model.countingCentreId == Area.Model.areaId,
                TallySheetVersionRow_PRE_30_PD.Model.candidateId == ElectionCandidate.Model.candidateId
            ),
            isouter=True
        ).filter(
            Election.Model.electionId == self.submission.election.electionId
        ).group_by(
            ElectionCandidate.Model.candidateId,
            Area.Model.areaId
        ).order_by(
            ElectionCandidate.Model.candidateId
        )

        return self.add_area_order_by(query, Area.Model.areaName)

    def area_wise_valid_vote_count_query(self):
        candidate_and_area_wise_valid_vote_count_subquery = self.candidate_and_area_wise_valid_vote_count_query().subquery()

        query = db.session.query(
            candidate_and_area_wise_valid_vote_count_subquery.c.areaId,
            candidate_and_area_wise_valid_vote_count_subquery.c.areaName,
            func.sum(
                sqlalchemy_num_or_zero(candidate_and_area_wise_valid_vote_count_subquery.c.validVoteCount)
            ).label("validVoteCount"),
        ).group_by(
            candidate_and_area_wise_valid_vote_count_subquery.c.areaId
        )

        return self.add_area_order_by(query, candidate_and_area_wise_valid_vote_count_subquery.c.areaName)

    def area_wise_vote_count_query(self):
        area_wise_valid_vote_count_subquery = self.area_wise_valid_vote_count_query().subquery()
        area_wise_rejected_vote_count_subquery = self.area_wise_rejected_vote_count_query().subquery()

        query = db.session.query(
            area_wise_valid_vote_count_subquery.c.areaId,
            area_wise_valid_vote_count_subquery.c.areaName,
            func.sum(
                sqlalchemy_num_or_zero(area_wise_valid_vote_count_subquery.c.validVoteCount)
            ).label("validVoteCount"),
            func.sum(
                area_wise_rejected_vote_count_subquery.c.rejectedVoteCount
            ).label("rejectedVoteCount"),
            func.sum(
                sqlalchemy_num_or_zero(area_wise_valid_vote_count_subquery.c.validVoteCount) +
                sqlalchemy_num_or_zero(area_wise_rejected_vote_count_subquery.c.rejectedVoteCount)
            ).label("totalVoteCount")
        ).join(
            area_wise_rejected_vote_count_subquery,
            area_wise_rejected_vote_count_subquery.c.areaId == area_wise_valid_vote_count_subquery.c.areaId
        ).group_by(
            area_wise_valid_vote_count_subquery.c.areaId
        )

        return self.add_area_order_by(query, area_wise_valid_vote_count_subquery.c.areaName)

    def candidate_wise_vote_count(self):
        candidate_and_area_wise_valid_vote_count_subquery = self.candidate_and_area_wise_valid_vote_count_query().subquery()

        return db.session.query(
            candidate_and_area_wise_valid_vote_count_subquery.c.candidateId,
            candidate_and_area_wise_valid_vote_count_subquery.c.candidateName,
            func.sum(
                sqlalchemy_num_or_zero(candidate_and_area_wise_valid_vote_count_subquery.c.validVoteCount)
            ).label("validVoteCount")
        ).group_by(
            candidate_and_area_wise_valid_vote_count_subquery.c.candidateId
        ).group_by(
            candidate_and_area_wise_valid_vote_count_subquery.c.candidateId
        ).order_by(
            candidate_and_area_wise_valid_vote_count_subquery.c.candidateId
        )

    def vote_count_query(self):
        area_wise_vote_count_subquery = self.area_wise_vote_count_query().subquery()

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
        countingCentres = self.countingCentres

        return db.session.query(
            ElectionCandidate.Model.candidateId,
            Candidate.Model.candidateName,
            Area.Model.areaId.label("countingCentreId"),
            Area.Model.areaName.label("countingCentreName"),
            func.sum(
                TallySheetVersionRow_PRE_30_PD.Model.count
            ).label("count"),
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

    def html(self):

        candidate_and_area_wise_valid_vote_count_result = self.candidate_and_area_wise_valid_vote_count_query().all()
        candidate_wise_vote_count_result = self.candidate_wise_vote_count().all()
        area_wise_vote_count_result = self.area_wise_vote_count_query().all()
        vote_count_result = self.vote_count_query().one_or_none()
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
        for area_wise_vote_count_result_item in area_wise_vote_count_result:
            content["countingCentres"].append(area_wise_vote_count_result_item.areaName)
            content["validVoteCounts"].append(to_comma_seperated_num(area_wise_vote_count_result_item.validVoteCount))
            content["rejectedVoteCounts"].append(
                to_comma_seperated_num(area_wise_vote_count_result_item.rejectedVoteCount))
            content["totalVoteCounts"].append(to_comma_seperated_num(area_wise_vote_count_result_item.totalVoteCount))

        # Append the grand totals
        content["validVoteCounts"].append(to_comma_seperated_num(vote_count_result.validVoteCount))
        content["rejectedVoteCounts"].append(to_comma_seperated_num(vote_count_result.rejectedVoteCount))
        content["totalVoteCounts"].append(to_comma_seperated_num(vote_count_result.totalVoteCount))

        if self.submission.election.voteType == VoteTypeEnum.Postal:
            content["tallySheetCode"] = "PRE/30/PV"

        number_of_counting_centres = len(area_wise_vote_count_result)
        number_of_candidates = len(candidate_wise_vote_count_result)

        for candidate_wise_vote_count_result_item_index in range(number_of_candidates):
            candidate_wise_vote_count_result_item = candidate_wise_vote_count_result[
                candidate_wise_vote_count_result_item_index
            ]

            data_row = []

            data_row_number = candidate_wise_vote_count_result_item_index + 1
            data_row.append(data_row_number)

            data_row.append(candidate_wise_vote_count_result_item.candidateName)

            for counting_centre_index in range(number_of_counting_centres):
                candidate_and_area_wise_valid_vote_count_result_item_index = \
                    (number_of_counting_centres * candidate_wise_vote_count_result_item_index) + counting_centre_index

                candidate_and_area_wise_valid_vote_count_result_item = candidate_and_area_wise_valid_vote_count_result[
                    candidate_and_area_wise_valid_vote_count_result_item_index
                ]

                data_row.append(
                    to_comma_seperated_num(candidate_and_area_wise_valid_vote_count_result_item.validVoteCount))

            data_row.append(to_comma_seperated_num(candidate_wise_vote_count_result_item.validVoteCount))

            content["data"].append(data_row)

        html = render_template(
            'PRE-30-PD.html',
            content=content
        )

        return html


Model = TallySheetVersion_PRE_30_PD_Model
