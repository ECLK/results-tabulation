import datetime
from app import db
from auth import authorize, POLLING_DIVISION_REPORT_VERIFIER_ROLE
from auth.AuthConstants import DATA_EDITOR_ROLE, EC_LEADERSHIP_ROLE
from exception.messages import MESSAGE_CODE_TALLY_SHEET_NOT_FOUND
from orm.entities.SubmissionVersion import TallySheetVersion
from orm.enums import TallySheetCodeEnum
from util import RequestBody, get_paginated_query
from schemas import TallySheetVersion_CE_201_PV_Schema, TallySheetVersionSchema
from orm.entities.Submission import TallySheet
from exception import NotFoundException
from orm.entities.Dashboard import StatusCE201
from orm.entities import Area
from orm.enums import AreaTypeEnum


@authorize(required_roles=[DATA_EDITOR_ROLE, POLLING_DIVISION_REPORT_VERIFIER_ROLE, EC_LEADERSHIP_ROLE])
def get_by_id(tallySheetId, tallySheetVersionId):
    result = TallySheetVersion.get_by_id(
        tallySheetId=tallySheetId,
        tallySheetVersionId=tallySheetVersionId
    )

    return TallySheetVersion_CE_201_PV_Schema().dump(result).data


@authorize(required_roles=[DATA_EDITOR_ROLE, EC_LEADERSHIP_ROLE])
def get_all(tallySheetId):
    tallySheet = TallySheet.get_by_id(tallySheetId=tallySheetId)
    if tallySheet is None:
        raise NotFoundException(
            message="Tally sheet not found (tallySheetId=%d)" % tallySheetId,
            code=MESSAGE_CODE_TALLY_SHEET_NOT_FOUND
        )

    result = TallySheetVersion.get_all(
        tallySheetId=tallySheetId
    )

    result = get_paginated_query(result).all()

    return TallySheetVersion_CE_201_PV_Schema(many=True).dump(result).data


@authorize(required_roles=[DATA_EDITOR_ROLE])
def create(tallySheetId, body):
    request_body = RequestBody(body)
    tallySheet, tallySheetVersion = TallySheet.create_latest_version(
        tallySheetId=tallySheetId,
        tallySheetCode=TallySheetCodeEnum.CE_201_PV
    )
    election = tally_sheet.submission.election
    voteType = election.electionName
    status = "Entered"
    electionId = election.parentElectionId
    countingCentreId = tallySheet.areaId
    area = Area.get_by_id(areaId=countingCentreId)
    electoralDistrictId = area.get_associated_areas(AreaTypeEnum.ElectoralDistrict, electionId=electionId)[0].areaId
    pollingDivisionId = None

    tallySheetVersion.set_complete()  # TODO: valid before setting complete. Refer to PRE_30_PD
    total_number_of_a_packets_found = 0
    tally_sheet_content = request_body.get("content")
    if tally_sheet_content is not None:
        for row in tally_sheet_content:
            tally_sheet_content_item = RequestBody(row)
            row = tallySheetVersion.add_row(
                ballotBoxId=tally_sheet_content_item.get("ballotBoxId"),
                numberOfPacketsInserted=tally_sheet_content_item.get("numberOfPacketsInserted"),
                numberOfAPacketsFound=tally_sheet_content_item.get("numberOfAPacketsFound")
            )

            total_number_of_a_packets_found = total_number_of_a_packets_found + row.numberOfAPacketsFound

        # for postal votes pollingStation is not available there for all results aggregated
        ballotCount = total_number_of_a_packets_found
        pollingStationId = None
        if election is not None:
            existingStatus = StatusCE201.get_status_record(
                electionId=electionId,
                electoralDistrictId=electoralDistrictId,
                pollingDivisionId=pollingDivisionId,
                countingCentreId=countingCentreId,
                pollingStationId=pollingStationId,
            )
            if existingStatus is None:
                StatusCE201.create(
                    voteType=voteType,
                    status=status,
                    electionId=electionId,
                    electoralDistrictId=electoralDistrictId,
                    pollingDivisionId=pollingDivisionId,
                    countingCentreId=countingCentreId,
                    pollingStationId=pollingStationId,
                    ballotCount=ballotCount
                )
            else:
                existingStatus.voteType = voteType,
                existingStatus.electionId = electionId,
                existingStatus.electoralDistrictId = electoralDistrictId,
                existingStatus.pollingDivisionId = pollingDivisionId,
                existingStatus.countingCentreId = countingCentreId,
                existingStatus.pollingStationId = pollingStationId,
                existingStatus.ballotCount = ballotCount

    tally_sheet_summary = request_body.get("summary")
    time_of_commencement_of_count = tally_sheet_summary.get("timeOfCommencementOfCount")

    if time_of_commencement_of_count is not None:

        # Remove the colon from %z [1] following [2]
        #   [1] http://strftime.org/
        #   [2] https://stackoverflow.com/questions/30999230/parsing-timezone-with-colon
        if ":" == time_of_commencement_of_count[-3:-2]:
            time_of_commencement_of_count = time_of_commencement_of_count[:-3] + time_of_commencement_of_count[-2:]

        try:
            time_of_commencement_of_count = datetime.datetime.strptime(
                time_of_commencement_of_count,
                '%Y-%m-%dT%H:%M:%S%z'
            )
        except  Exception as e:
            time_of_commencement_of_count = None
    else:
        time_of_commencement_of_count = None

    # To remove the colon between time zone comming from openapi date-time.
    # This is since the colon is not accepted in python datetime
    # if ":" == time_of_commencement_of_count[-3:-2]:
    #     time_of_commencement_of_count = time_of_commencement_of_count[:-3] + time_of_commencement_of_count[-2:]

    tallySheetVersion.add_summary(
        situation=tally_sheet_summary.get("situation"),
        timeOfCommencementOfCount=time_of_commencement_of_count,
        numberOfAPacketsFound=total_number_of_a_packets_found,
        numberOfACoversRejected=tally_sheet_summary.get("numberOfACoversRejected"),
        numberOfBCoversRejected=tally_sheet_summary.get("numberOfBCoversRejected"),
        numberOfValidBallotPapers=tally_sheet_summary.get("numberOfValidBallotPapers")
    )

    db.session.commit()

    return TallySheetVersionSchema().dump(tallySheetVersion).data
