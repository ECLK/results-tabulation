import datetime

from app import db
from util import RequestBody
from schemas import TallySheetVersion_CE_201_PV_Schema, TallySheetVersionSchema
from orm.entities.Submission import TallySheet
from orm.entities.SubmissionVersion.TallySheetVersion import TallySheetVersion_CE_201_PV
from exception import NotFoundException


def get_by_id(tallySheetId, tallySheetVersionId):
    result = TallySheetVersion_CE_201_PV.get_by_id(
        tallySheetId=tallySheetId,
        tallySheetVersionId=tallySheetVersionId
    )

    return TallySheetVersion_CE_201_PV_Schema().dump(result).data


def get_all(tallySheetId):
    tallySheet = TallySheet.get_by_id(tallySheetId=tallySheetId)
    if tallySheet is None:
        raise NotFoundException("Tally sheet not found. (tallySheetId=%d)" % tallySheetId)

    result = TallySheetVersion_CE_201_PV.get_all(
        tallySheetId=tallySheetId
    )

    return TallySheetVersion_CE_201_PV_Schema(many=True).dump(result).data


def create(tallySheetId, body):
    request_body = RequestBody(body)
    tallySheetVersion = TallySheetVersion_CE_201_PV.create(
        tallySheetId=tallySheetId
    )

    total_number_of_a_packets_found = 0
    tally_sheet_content = request_body.get("content")
    if tally_sheet_content is not None:
        for row in tally_sheet_content:
            tally_sheet_content_item = RequestBody(row)
            row = tallySheetVersion.add_row(
                ballotBoxStationaryItemId=tally_sheet_content_item.get("ballotBoxStationaryItemId"),
                numberOfPacketsInserted=tally_sheet_content_item.get("numberOfPacketsInserted"),
                numberOfAPacketsFound=tally_sheet_content_item.get("numberOfAPacketsFound")
            )

            total_number_of_a_packets_found = total_number_of_a_packets_found + row.numberOfAPacketsFound

    tally_sheet_summary = request_body.get("summary")
    time_of_commencement_of_count = tally_sheet_summary.get("timeOfCommencementOfCount")

    # To remove the colon between time zone comming from openapi date-time.
    # This is since the colon is not accepted in python datetime
    # if ":" == time_of_commencement_of_count[-3:-2]:
    #     time_of_commencement_of_count = time_of_commencement_of_count[:-3] + time_of_commencement_of_count[-2:]

    tallySheetVersion.add_summary(
        situation=tally_sheet_summary.get("situation"),
        timeOfCommencementOfCount=datetime.datetime.strptime(
            time_of_commencement_of_count,
            '%Y-%m-%dT%H:%M:%S.%fZ'
        ),
        numberOfAPacketsFound=total_number_of_a_packets_found,
        numberOfACoversRejected=tally_sheet_summary.get("numberOfACoversRejected"),
        numberOfBCoversRejected=tally_sheet_summary.get("numberOfBCoversRejected"),
        numberOfValidBallotPapers=tally_sheet_summary.get("numberOfValidBallotPapers")
    )

    db.session.commit()

    return TallySheetVersionSchema().dump(tallySheetVersion).data
