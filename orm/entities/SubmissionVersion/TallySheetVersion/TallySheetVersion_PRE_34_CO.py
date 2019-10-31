from flask import render_template
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func, and_, or_
from app import db
from orm.entities import Area, Candidate, Party, Election
from orm.entities.Election import ElectionCandidate
from orm.entities.SubmissionVersion import TallySheetVersion
from util import to_comma_seperated_num, sqlalchemy_num_or_zero
from orm.enums import TallySheetCodeEnum, AreaTypeEnum, VoteTypeEnum


class TallySheetVersion_PRE_34_CO_Model(TallySheetVersion.Model):

    def __init__(self, tallySheetId):
        super(TallySheetVersion_PRE_34_CO_Model, self).__init__(
            tallySheetId=tallySheetId
        )

    __mapper_args__ = {
        'polymorphic_identity': TallySheetCodeEnum.PRE_34_CO
    }

    def add_row(self, preferenceNumber, preferenceCount, candidateId, electionId):
        from orm.entities.TallySheetVersionRow import TallySheetVersionRow_PRE_34_preference

        TallySheetVersionRow_PRE_34_preference.create(
            tallySheetVersionId=self.tallySheetVersionId,
            electionId=electionId,
            preferenceNumber=preferenceNumber,
            preferenceCount=preferenceCount,
            candidateId=candidateId
        )

    def html(self):
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
            'PRE-34-CO.html',
            content=content
        )

        return html


Model = TallySheetVersion_PRE_34_CO_Model
