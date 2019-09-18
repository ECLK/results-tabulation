from flask import render_template
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from app import db
from exception import NotFoundException
from orm.entities import Candidate, Party, Area
from orm.entities.Election import ElectionCandidate
from orm.entities.SubmissionVersion import TallySheetVersion
from orm.entities.TallySheetVersionRow import TallySheetVersionRow_PRE_ALL_ISLAND_RESULT, \
    TallySheetVersionRow_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS
from util import get_paginated_query

from orm.entities.Submission import TallySheet
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
    def content(self):

        electoralDistricts = self.submission.area.get_associated_areas(AreaTypeEnum.ElectoralDistrict)

        return db.session.query(
            ElectionCandidate.Model.candidateId,
            Candidate.Model.candidateName,
            Party.Model.partySymbol,
            TallySheetVersionRow_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS.Model.electoralDistrictId,
            Area.Model.areaName.label("electoralDistrictName"),
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

    def html(self):

        content = {
            "electoralDistricts": [],
            "data": [],
            "validVotes": [],
            "rejectedVotes": [],
            "totalVotes": []
        }

        parties = self.submission.election.parties
        queryResult = self.content
        electoralDistrictCount = int(len(queryResult) / len(parties))

        # Fill the validVotes, rejectedVotes and totalVotes with zeros.
        for i in range(0, electoralDistrictCount):
            content["electoralDistricts"].append(queryResult[i].electoralDistrictName)

            content["validVotes"].append(0)
            content["rejectedVotes"].append(0)
            content["totalVotes"].append(0)

        # Iterate by candidates.
        for i in range(len(parties)):
            # Append candidate details.
            data_row = [queryResult[i * electoralDistrictCount].candidateName]
            content["data"].append(data_row)
            total_count_per_candidate = 0

            # Iterate by counting centres.
            for j in range(electoralDistrictCount):
                # Determine the result index mapping with the counting centre and candidate.
                query_result_index = (i * electoralDistrictCount) + j

                count = queryResult[query_result_index].count

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

            data_row.append(total_count_per_candidate)

            # total_count_per_candidate in words
            data_row.append("")

        content["validVotes"].append(sum(content["validVotes"]))
        # total validVotes in words
        content["validVotes"].append("")

        content["rejectedVotes"].append(sum(content["rejectedVotes"]))
        # total rejectedVotes in words
        content["rejectedVotes"].append("")

        content["totalVotes"].append(sum(content["totalVotes"]))
        # totalVotes in words
        content["totalVotes"].append("")

        html = render_template(
            'PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS.html',
            content=content
        )

        return html


Model = TallySheetVersion_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS_Model


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
