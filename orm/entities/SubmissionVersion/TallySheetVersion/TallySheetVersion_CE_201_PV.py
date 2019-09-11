from flask import render_template
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from app import db
from exception import NotFoundException
from orm.entities import Candidate, Party, Area
from orm.entities.Election import ElectionCandidate, InvalidVoteCategory
from orm.entities.SubmissionVersion import TallySheetVersion
from orm.entities.TallySheetVersionRow import TallySheetVersionRow_CE_201_PV
from util import get_paginated_query, to_empty_string_or_value

from orm.entities.Submission import TallySheet
from orm.enums import TallySheetCodeEnum, AreaTypeEnum
from sqlalchemy import and_


class TallySheetVersion_CE_201_PV_Model(TallySheetVersion.Model):

    def __init__(self, tallySheetId):
        super(TallySheetVersion_CE_201_PV_Model, self).__init__(
            tallySheetId=tallySheetId
        )

    __mapper_args__ = {
        'polymorphic_identity': TallySheetCodeEnum.CE_201_PV
    }

    def add_row(self, serialNumber, numberOfBPacketsInserted, numberOfAPacketsFound):
        from orm.entities.TallySheetVersionRow import TallySheetVersionRow_CE_201_PV

        TallySheetVersionRow_CE_201_PV.create(
            tallySheetVersionId=self.tallySheetVersionId,
            serialNumber=serialNumber,
            numberOfBPacketsInserted=numberOfBPacketsInserted,
            numberOfAPacketsFound=numberOfAPacketsFound
        )

    @hybrid_property
    def content(self):
        return db.session.query(
            InvalidVoteCategory.Model.invalidVoteCategoryId,
            InvalidVoteCategory.Model.categoryDescription,
            TallySheetVersionRow_CE_201_PV.Model.count
        ).join(
            TallySheetVersionRow_CE_201_PV.Model,
            and_(
                TallySheetVersionRow_CE_201_PV.Model.invalidVoteCategoryId == InvalidVoteCategory.Model.invalidVoteCategoryId,
                TallySheetVersionRow_CE_201_PV.Model.tallySheetVersionId == self.tallySheetVersionId
            ),
            isouter=True
        ).filter(
            InvalidVoteCategory.Model.electionId == self.submission.electionId
        )

    def html(self):
        tallySheetContent = self.content.all()

        content = {
            "electoralDistrict": Area.get_associated_areas(
                self.submission.area, AreaTypeEnum.ElectoralDistrict)[0].areaName,
            "pollingDivision": Area.get_associated_areas(
                self.submission.area, AreaTypeEnum.PollingDivision)[0].areaName,
            "countingCentre": self.submission.area.areaName,
            "pollingDistrictNos": ", ".join([
                pollingDistrict.areaName for pollingDistrict in
                Area.get_associated_areas(self.submission.area, AreaTypeEnum.PollingDistrict)
            ]),
            "data": [
            ]
        }

        for row_index in range(len(tallySheetContent)):
            row = tallySheetContent[row_index]
            data_row = []
            content["data"].append(data_row)

            data_row.append(row.categoryDescription)
            data_row.append(to_empty_string_or_value(row.count))

        html = render_template(
            'PRE-21.html',
            content=content
        )

        return html


Model = TallySheetVersion_CE_201_PV_Model


def get_all(tallySheetId):
    query = Model.query.filter(Model.tallySheetId == tallySheetId)

    result = get_paginated_query(query).all()

    return result


def get_by_id(tallySheetId, tallySheetVersionId):
    tallySheet = TallySheet.get_by_id(tallySheetId=tallySheetId)
    if tallySheet is None:
        raise NotFoundException("Tally sheet not found. (tallySheetId=%d)" % tallySheetId)
    elif tallySheet.tallySheetCode is not TallySheetCodeEnum.CE_201_PV:
        raise NotFoundException("Requested version not found. (tallySheetId=%d)" % tallySheetId)

    result = Model.query.filter(
        Model.tallySheetVersionId == tallySheetVersionId
    ).one_or_none()

    return result


def create(tallySheetId):
    result = Model(tallySheetId=tallySheetId)

    return result
