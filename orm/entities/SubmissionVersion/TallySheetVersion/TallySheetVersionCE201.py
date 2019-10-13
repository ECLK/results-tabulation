from flask import render_template
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import and_

from app import db
from exception import NotFoundException
from orm.entities import Area
from orm.entities.SubmissionVersion import TallySheetVersion
from orm.entities.TallySheetVersionRow import TallySheetVersionRow_CE_201
from util import get_paginated_query, to_empty_string_or_value
from datetime import date
from datetime import datetime

from orm.entities.Submission import TallySheet
from orm.enums import TallySheetCodeEnum, AreaTypeEnum


class TallySheetVersionCE201Model(TallySheetVersion.Model):

    def __init__(self, tallySheetId):
        super(TallySheetVersionCE201Model, self).__init__(
            tallySheetId=tallySheetId
        )

    __mapper_args__ = {
        'polymorphic_identity': TallySheetCodeEnum.CE_201
    }

    def add_row(self, areaId, ballotsIssued, ballotsReceived, ballotsSpoilt,
                ballotsUnused,
                ordinaryBallotCountFromBoxCount, tenderedBallotCountFromBoxCount,
                ordinaryBallotCountFromBallotPaperAccount, tenderedBallotCountFromBallotPaperAccount):
        from orm.entities.TallySheetVersionRow import TallySheetVersionRow_CE_201

        return TallySheetVersionRow_CE_201.create(
            tallySheetVersion=self,
            areaId=areaId,
            ballotsIssued=ballotsIssued,
            ballotsReceived=ballotsReceived,
            ballotsSpoilt=ballotsSpoilt,
            ballotsUnused=ballotsUnused,
            ordinaryBallotCountFromBoxCount=ordinaryBallotCountFromBoxCount,
            tenderedBallotCountFromBoxCount=tenderedBallotCountFromBoxCount,
            ordinaryBallotCountFromBallotPaperAccount=ordinaryBallotCountFromBallotPaperAccount,
            tenderedBallotCountFromBallotPaperAccount=tenderedBallotCountFromBallotPaperAccount
        )

    def html(self):
        tallySheetContent = self.content

        content = {
            "date": date.today().strftime("%B %d, %Y"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "electionName": self.submission.election.electionName,
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

            # polling division
            data_row.append(
                ", ".join(
                    area.areaName for area in row.area.get_associated_areas(AreaTypeEnum.PollingDistrict)
                )
            )

            # polling station
            data_row.append(row.areaName)

            # three ballot boxes
            for ballotBoxIndex in range(3):
                if ballotBoxIndex < len(row.ballotBoxesReceived):
                    data_row.append(row.ballotBoxesReceived[ballotBoxIndex])
                else:
                    data_row.append("")

            data_row.append(to_empty_string_or_value(row.ballotsReceived))
            data_row.append(to_empty_string_or_value(row.ballotsSpoilt))
            data_row.append(to_empty_string_or_value(row.ballotsIssued))
            data_row.append(to_empty_string_or_value(row.ballotsUnused))

            data_row.append(to_empty_string_or_value(row.ordinaryBallotCountFromBallotPaperAccount))
            data_row.append(to_empty_string_or_value(row.ordinaryBallotCountFromBoxCount))
            data_row.append(abs(row.ordinaryBallotCountFromBallotPaperAccount - row.ordinaryBallotCountFromBoxCount))

            data_row.append(to_empty_string_or_value(row.tenderedBallotCountFromBallotPaperAccount))
            data_row.append(to_empty_string_or_value(row.tenderedBallotCountFromBoxCount))
            data_row.append(abs(row.tenderedBallotCountFromBallotPaperAccount - row.tenderedBallotCountFromBoxCount))

        html = render_template(
            'CE-201.html',
            content=content
        )

        return html

    @hybrid_property
    def content(self):
        pollingStations = self.submission.area.get_associated_areas(AreaTypeEnum.PollingStation)

        # TODO
        result = db.session.query(
            TallySheetVersionRow_CE_201.Model
        ).join(
            Area.Model,
            and_(
                TallySheetVersionRow_CE_201.Model.areaId == Area.Model.areaId,
                Area.Model.areaId.in_([area.areaId for area in pollingStations])
            )
        ).filter(
            TallySheetVersionRow_CE_201.Model.tallySheetVersionId == self.tallySheetVersionId
        ).order_by(
            Area.Model.areaId
        ).all()

        return result


Model = TallySheetVersionCE201Model


def get_all(tallySheetId):
    query = Model.query.filter(Model.tallySheetId == tallySheetId)

    result = get_paginated_query(query).all()

    return result


def get_by_id(tallySheetId, tallySheetVersionId):
    tallySheet = TallySheet.get_by_id(tallySheetId=tallySheetId)
    if tallySheet is None:
        raise NotFoundException("Tally sheet not found. (tallySheetId=%d)" % tallySheetId)
    elif tallySheet.tallySheetCode is not TallySheetCodeEnum.CE_201:
        raise NotFoundException("Requested version not found. (tallySheetId=%d)" % tallySheetId)

    result = Model.query.filter(
        Model.tallySheetVersionId == tallySheetVersionId
    ).one_or_none()

    return result


def create(tallySheetId):
    result = Model(tallySheetId=tallySheetId)

    return result
