from flask import render_template
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func
from app import db
from orm.entities import Candidate, Party, Area, Election
from orm.entities.Election import ElectionCandidate
from orm.entities.SubmissionVersion import TallySheetVersion
from orm.entities.TallySheetVersionRow import TallySheetVersionRow_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS, \
    TallySheetVersionRow_RejectedVoteCount
from util import to_comma_seperated_num, sqlalchemy_num_or_zero
from orm.enums import TallySheetCodeEnum, AreaTypeEnum
from sqlalchemy import and_


class TallySheetVersion_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS_Model(TallySheetVersion.Model):

    def __init__(self, tallySheetId):
        super(TallySheetVersion_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS_Model, self).__init__(
            tallySheetId=tallySheetId
        )

    __mapper_args__ = {
        'polymorphic_identity': TallySheetCodeEnum.PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS
    }

    def add_row(self, candidateId, electoralDistrictId, count):
        from orm.entities.TallySheetVersionRow import TallySheetVersionRow_PRE_ALL_ISLAND_RESULT

        TallySheetVersionRow_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS.create(
            tallySheetVersionId=self.tallySheetVersionId,
            candidateId=candidateId,
            electoralDistrictId=electoralDistrictId,
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

    def area_wise_rejected_vote_count_query(self):
        return db.session.query(
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
            Area.Model.areaId.in_([area.areaId for area in self.electoralDistricts])
        ).group_by(
            Area.Model.areaId
        ).order_by(
            Area.Model.areaName
        )

    def candidate_and_area_wise_valid_vote_count_query(self):
        return db.session.query(
            Election.Model.electionId,
            ElectionCandidate.Model.candidateId,
            Candidate.Model.candidateName,
            Area.Model.areaId,
            Area.Model.areaName,
            func.sum(
                TallySheetVersionRow_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS.Model.count
            ).label("validVoteCount"),
        ).join(
            ElectionCandidate.Model,
            ElectionCandidate.Model.electionId == Election.Model.electionId
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
                Area.Model.areaId.in_([area.areaId for area in self.electoralDistricts])
            )
        ).join(
            TallySheetVersionRow_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS.Model,
            and_(
                TallySheetVersionRow_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS.Model.tallySheetVersionId == self.tallySheetVersionId,
                TallySheetVersionRow_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS.Model.electoralDistrictId == Area.Model.areaId,
                TallySheetVersionRow_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS.Model.candidateId == ElectionCandidate.Model.candidateId
            ),
            isouter=True
        ).filter(
            Election.Model.electionId == self.submission.election.electionId
        ).group_by(
            ElectionCandidate.Model.candidateId,
            Area.Model.areaId
        ).order_by(
            ElectionCandidate.Model.candidateId,
            Area.Model.areaName
        )

    def area_wise_valid_vote_count_query(self):
        candidate_and_area_wise_valid_vote_count_subquery = self.candidate_and_area_wise_valid_vote_count_query().subquery()

        return db.session.query(
            candidate_and_area_wise_valid_vote_count_subquery.c.areaId,
            candidate_and_area_wise_valid_vote_count_subquery.c.areaName,
            func.sum(
                sqlalchemy_num_or_zero(candidate_and_area_wise_valid_vote_count_subquery.c.validVoteCount)
            ).label("validVoteCount"),
        ).group_by(
            candidate_and_area_wise_valid_vote_count_subquery.c.areaId
        ).order_by(
            candidate_and_area_wise_valid_vote_count_subquery.c.areaName
        )

    def area_wise_vote_count_query(self):
        area_wise_valid_vote_count_subquery = self.area_wise_valid_vote_count_query().subquery()
        area_wise_rejected_vote_count_subquery = self.area_wise_rejected_vote_count_query().subquery()

        return db.session.query(
            area_wise_valid_vote_count_subquery.c.areaId,
            area_wise_valid_vote_count_subquery.c.areaName,
            func.sum(
                sqlalchemy_num_or_zero(area_wise_valid_vote_count_subquery.c.validVoteCount)
            ).label(
                "validVoteCount"),
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
        ).order_by(
            area_wise_valid_vote_count_subquery.c.areaName
        )

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
            candidate_and_area_wise_valid_vote_count_subquery.c.candidateName
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

        electoralDistricts = db.session.query(
            Area.Model
        ).filter(
            Area.Model.areaType == AreaTypeEnum.ElectoralDistrict,
            Area.Model.electionId == self.submission.electionId
        ).all()

        return db.session.query(
            ElectionCandidate.Model.candidateId,
            Candidate.Model.candidateName,
            Party.Model.partySymbol,
            Area.Model.areaName.label("electoralDistrictName"),
            Area.Model.areaId.label("electoralDistrictId"),
            TallySheetVersionRow_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS.Model.count
        ).join(
            Area.Model,
            and_(
                Area.Model.electionId == ElectionCandidate.Model.electionId,
                Area.Model.areaId.in_([area.areaId for area in electoralDistricts])
            )
        ).join(
            TallySheetVersionRow_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS.Model,
            and_(
                TallySheetVersionRow_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS.Model.candidateId == ElectionCandidate.Model.candidateId,
                TallySheetVersionRow_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS.Model.electoralDistrictId == Area.Model.areaId,
                TallySheetVersionRow_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS.Model.tallySheetVersionId == self.tallySheetVersionId,
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
        ).order_by(
            ElectionCandidate.Model.candidateId,
            Area.Model.areaId
        ).all()

    def get_html_content_dict(self):
        candidate_and_area_wise_valid_vote_count_result = self.candidate_and_area_wise_valid_vote_count_query().all()
        candidate_wise_vote_count_result = self.candidate_wise_vote_count().all()
        area_wise_vote_count_result = self.area_wise_vote_count_query().all()
        vote_count_result = self.vote_count_query().one_or_none()

        stamp = self.stamp

        content = {
            "election": {
                "electionName": self.submission.election.get_official_name()
            },
            "stamp": {
                "createdAt": stamp.createdAt,
                "createdBy": stamp.createdBy,
                "barcodeString": stamp.barcodeString
            },
            "electoralDistricts": [],
            "data": [],
            "validVoteCounts": [],
            "rejectedVoteCounts": [],
            "totalVoteCounts": []
        }

        # Append the area wise column totals
        for area_wise_vote_count_result_item in area_wise_vote_count_result:
            content["electoralDistricts"].append(area_wise_vote_count_result_item.areaName)
            content["validVoteCounts"].append(to_comma_seperated_num(area_wise_vote_count_result_item.validVoteCount))
            content["rejectedVoteCounts"].append(
                to_comma_seperated_num(area_wise_vote_count_result_item.rejectedVoteCount))
            content["totalVoteCounts"].append(to_comma_seperated_num(area_wise_vote_count_result_item.totalVoteCount))

        # Append the grand totals
        content["validVoteCounts"].append(to_comma_seperated_num(vote_count_result.validVoteCount))
        content["rejectedVoteCounts"].append(to_comma_seperated_num(vote_count_result.rejectedVoteCount))
        content["totalVoteCounts"].append(to_comma_seperated_num(vote_count_result.totalVoteCount))

        number_of_electoral_districts = len(area_wise_vote_count_result)
        number_of_candidates = len(candidate_wise_vote_count_result)

        for candidate_wise_vote_count_result_item_index in range(number_of_candidates):
            candidate_wise_vote_count_result_item = candidate_wise_vote_count_result[
                candidate_wise_vote_count_result_item_index
            ]

            data_row = []

            # data_row_number = candidate_wise_vote_count_result_item_index + 1
            # data_row.append(data_row_number)

            data_row.append(candidate_wise_vote_count_result_item.candidateName)

            for electoral_district_index in range(number_of_electoral_districts):
                candidate_and_area_wise_valid_vote_count_result_item_index = \
                    (
                            number_of_electoral_districts * candidate_wise_vote_count_result_item_index) + electoral_district_index

                candidate_and_area_wise_valid_vote_count_result_item = candidate_and_area_wise_valid_vote_count_result[
                    candidate_and_area_wise_valid_vote_count_result_item_index
                ]

                data_row.append(
                    to_comma_seperated_num(candidate_and_area_wise_valid_vote_count_result_item.validVoteCount))

            data_row.append(to_comma_seperated_num(candidate_wise_vote_count_result_item.validVoteCount))

            content["data"].append(data_row)

        return content

    def html_letter(self):
        html = render_template(
            'PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS.html',
            content=self.get_html_content_dict()
        )

        return html

    def html(self):
        html = render_template(
            'PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS.html',
            content=self.get_html_content_dict()
        )

        return html


Model = TallySheetVersion_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS_Model
