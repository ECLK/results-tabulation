from api import TallySheetVersionApi
from app import db
from auth import authorize, POLLING_DIVISION_REPORT_VERIFIER_ROLE
from auth.AuthConstants import DATA_EDITOR_ROLE, EC_LEADERSHIP_ROLE
from orm.entities.SubmissionVersion import TallySheetVersion
from orm.enums import TallySheetCodeEnum
from util import RequestBody
from schemas import TallySheetVersionCE201Schema, TallySheetVersionSchema
from orm.entities.Submission import TallySheet
from orm.entities.Dashboard import StatusCE201
from orm.entities import Area
from orm.enums import AreaTypeEnum


@authorize(required_roles=[DATA_EDITOR_ROLE, POLLING_DIVISION_REPORT_VERIFIER_ROLE, EC_LEADERSHIP_ROLE])
def get_by_id(tallySheetId, tallySheetVersionId):
    result = TallySheetVersion.get_by_id(
        tallySheetId=tallySheetId,
        tallySheetVersionId=tallySheetVersionId
    )

    return TallySheetVersionCE201Schema().dump(result).data


@authorize(required_roles=[DATA_EDITOR_ROLE])
def create(tallySheetId, body):
    request_body = RequestBody(body)

    tallySheet, tallySheetVersion = TallySheet.create_latest_version(
        tallySheetId=tallySheetId,
        tallySheetCode=TallySheetCodeEnum.CE_201
    )
    election = tallySheet.submission.election
    voteType = election.electionName
    status = "Entered"
    electionId = election.parentElectionId
    countingCentreId = tallySheet.areaId
    area = Area.get_by_id(areaId=countingCentreId)
    electoralDistrictId = area.get_associated_areas(AreaTypeEnum.ElectoralDistrict, electionId=electionId)[0].areaId
    pollingDivisionId = area.get_associated_areas(AreaTypeEnum.PollingDivision, electionId=electionId)[0].areaId

    tallySheetVersion.set_complete()  # TODO: valid before setting complete. Refer to PRE_30_PD
    tally_sheet_content = request_body.get("content")
    if tally_sheet_content is not None:
        for party_count_body in tally_sheet_content:
            party_count_body = RequestBody(party_count_body)
            tallySheetVersionRow = tallySheetVersion.add_row(
                areaId=party_count_body.get("areaId"),
                ballotsIssued=party_count_body.get("ballotsIssued"),
                ballotsReceived=party_count_body.get("ballotsReceived"),
                ballotsSpoilt=party_count_body.get("ballotsSpoilt"),
                ballotsUnused=party_count_body.get("ballotsUnused"),
                ordinaryBallotCountFromBoxCount=party_count_body.get("ordinaryBallotCountFromBoxCount"),
                tenderedBallotCountFromBoxCount=party_count_body.get("tenderedBallotCountFromBoxCount"),
                ordinaryBallotCountFromBallotPaperAccount=party_count_body.get(
                    "ordinaryBallotCountFromBallotPaperAccount"),
                tenderedBallotCountFromBallotPaperAccount=party_count_body.get(
                    "tenderedBallotCountFromBallotPaperAccount")
            )

            for issued_ballot_box_id in party_count_body.get("ballotBoxesIssued"):
                tallySheetVersionRow.add_issued_ballot_box(issued_ballot_box_id)

            for received_ballot_box_id in party_count_body.get("ballotBoxesReceived"):
                tallySheetVersionRow.add_received_ballot_box(received_ballot_box_id)

            ballotCount = party_count_body.get("ordinaryBallotCountFromBoxCount")
            pollingStationId = party_count_body.get("areaId")
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

        db.session.commit()

        return TallySheetVersionSchema().dump(tallySheetVersion).data
