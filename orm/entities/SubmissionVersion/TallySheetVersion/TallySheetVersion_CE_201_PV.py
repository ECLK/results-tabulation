from flask import render_template
from sqlalchemy.ext.hybrid import hybrid_property

from app import db
from orm.entities import Area
from orm.entities.SubmissionVersion import TallySheetVersion
from orm.entities.TallySheetVersionRow import TallySheetVersionRow_CE_201_PV, TallySheetVersionRow_CE_201_PV_CC
from orm.enums import TallySheetCodeEnum, AreaTypeEnum
from util import to_comma_seperated_num


class TallySheetVersion_CE_201_PV_Model(TallySheetVersion.Model):

    def __init__(self, tallySheetId):
        super(TallySheetVersion_CE_201_PV_Model, self).__init__(
            tallySheetId=tallySheetId
        )

    __mapper_args__ = {
        'polymorphic_identity': TallySheetCodeEnum.CE_201_PV
    }

    def add_summary(self, situation, timeOfCommencementOfCount, numberOfAPacketsFound, numberOfACoversRejected,
                    numberOfBCoversRejected, numberOfValidBallotPapers):
        return TallySheetVersionRow_CE_201_PV_CC.create(
            tallySheetVersionId=self.tallySheetVersionId,
            countingCentreId=self.submission.area.areaId,
            situation=situation,
            timeOfCommencementOfCount=timeOfCommencementOfCount,
            numberOfAPacketsFound=numberOfAPacketsFound,
            numberOfACoversRejected=numberOfACoversRejected,
            numberOfBCoversRejected=numberOfBCoversRejected,
            numberOfValidBallotPapers=numberOfValidBallotPapers
        )

    def add_row(self, ballotBoxId, numberOfPacketsInserted, numberOfAPacketsFound):
        return TallySheetVersionRow_CE_201_PV.create(
            tallySheetVersionId=self.tallySheetVersionId,
            ballotBoxId=ballotBoxId,
            numberOfPacketsInserted=numberOfPacketsInserted,
            numberOfAPacketsFound=numberOfAPacketsFound
        )

    @hybrid_property
    def content(self):
        # return []
        return db.session.query(
            TallySheetVersionRow_CE_201_PV.Model
        ).filter(
            TallySheetVersionRow_CE_201_PV.Model.tallySheetVersionId == self.tallySheetVersionId
        )

    @hybrid_property
    def summary(self):
        return db.session.query(
            TallySheetVersionRow_CE_201_PV_CC.Model
        ).filter(
            TallySheetVersionRow_CE_201_PV_CC.Model.tallySheetVersionId == self.tallySheetVersionId
        ).one_or_none()

    def html(self):
        tallySheetContent = self.content.all()
        tallySheetContentSummary = self.summary
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
            "electoralDistrict": Area.get_associated_areas(
                self.submission.area, AreaTypeEnum.ElectoralDistrict)[0].areaName,
            "countingCentre": self.submission.area.areaName,
            "situation": tallySheetContentSummary.situation,
            "timeOfCommencementOfCount": tallySheetContentSummary.timeOfCommencementOfCount,
            "numberOfAPacketsFound": tallySheetContentSummary.numberOfAPacketsFound,
            "numberOfACoversRejected": to_comma_seperated_num(tallySheetContentSummary.numberOfACoversRejected),
            "numberOfBCoversRejected": to_comma_seperated_num(tallySheetContentSummary.numberOfBCoversRejected),
            "numberOfValidBallotPapers": to_comma_seperated_num(tallySheetContentSummary.numberOfValidBallotPapers),

            "data": [
            ],
        }

        for row_index in range(len(tallySheetContent)):
            row = tallySheetContent[row_index]
            data_row = []
            content["data"].append(data_row)

            data_row.append(row.ballotBoxId)
            data_row.append(to_comma_seperated_num(row.numberOfPacketsInserted))
            data_row.append(to_comma_seperated_num(row.numberOfAPacketsFound))

        html = render_template(
            'CE-201-PV.html',
            content=content
        )

        return html


Model = TallySheetVersion_CE_201_PV_Model
