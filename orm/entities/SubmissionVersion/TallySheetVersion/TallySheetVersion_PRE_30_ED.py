from flask import render_template
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy import func, and_

from app import db
from exception import NotFoundException
from orm.entities import Area, Candidate, Party
from orm.entities.Election import ElectionCandidate
from orm.entities.SubmissionVersion import TallySheetVersion
from orm.entities.TallySheetVersionRow import TallySheetVersionRow_PRE_30_ED
from util import get_paginated_query

from orm.entities.Submission import TallySheet
from orm.enums import TallySheetCodeEnum, AreaTypeEnum


class TallySheetVersion_PRE_30_ED_Model(TallySheetVersion.Model):

    def __init__(self, tallySheetId):
        super(TallySheetVersion_PRE_30_ED_Model, self).__init__(
            tallySheetId=tallySheetId
        )

    __mapper_args__ = {
        'polymorphic_identity': TallySheetCodeEnum.PRE_30_ED
    }

    def add_row(self, pollingDivisionId, candidateId, count):
        from orm.entities.TallySheetVersionRow import TallySheetVersionRow_PRE_30_ED

        TallySheetVersionRow_PRE_30_ED.create(
            tallySheetVersionId=self.tallySheetVersionId,
            candidateId=candidateId,
            pollingDivisionId=pollingDivisionId,
            count=count
        )

    @hybrid_property
    def content(self):
        pollingDivisions = self.submission.area.get_associated_areas(AreaTypeEnum.PollingDivision)

        return db.session.query(
            ElectionCandidate.Model.candidateId,
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
                Area.Model.areaId.in_([area.areaId for area in pollingDivisions])
            )
        ).join(
            TallySheetVersionRow_PRE_30_ED.Model,
            and_(
                TallySheetVersionRow_PRE_30_ED.Model.tallySheetVersionId == self.tallySheetVersionId,
                TallySheetVersionRow_PRE_30_ED.Model.pollingDivisionId == Area.Model.areaId,
                TallySheetVersionRow_PRE_30_ED.Model.candidateId == ElectionCandidate.Model.candidateId
            ),
            isouter=True
        ).filter(
            ElectionCandidate.Model.electionId == self.submission.electionId
        ).group_by(
            ElectionCandidate.Model.candidateId,
            Area.Model.areaId
        ).order_by(
            ElectionCandidate.Model.candidateId,
            Area.Model.areaId
        ).all()

    def html(self):

        content = {
            "electoralDistrict": self.submission.area.areaName,
            "pollingDivisions": [],
            "data": [],
            "validVotes": [],
            "rejectedVotes": [],
            "totalVotes": []
        }

        parties = self.submission.election.parties
        queryResult = self.content
        countingCentreCount = int(len(queryResult) / len(parties))

        # Fill the validVotes, rejectedVotes and totalVotes with zeros.
        for i in range(0, countingCentreCount):
            content["pollingDivisions"].append(queryResult[i].pollingDivisionName)

            content["validVotes"].append(0)
            content["rejectedVotes"].append(0)
            content["totalVotes"].append(0)

        # Iterate by candidates.
        for i in range(len(parties)):
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

                    # Calculate valid votes count.
                    content["validVotes"][j] = content["validVotes"][j] + count

                    # Calculate validVotes count.
                    content["rejectedVotes"][j] = 0  # TODO

                    content["totalVotes"][j] = content["validVotes"][j] + content["rejectedVotes"][j]

            data_row.append(total_count_per_candidate)

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
    elif tallySheet.tallySheetCode is not TallySheetCodeEnum.PRE_30_PD:
        raise NotFoundException("Requested version not found. (tallySheetId=%d)" % tallySheetId)

    result = Model.query.filter(
        Model.tallySheetVersionId == tallySheetVersionId
    ).one_or_none()

    return result


def create(tallySheetId):
    result = Model(tallySheetId=tallySheetId)

    return result
