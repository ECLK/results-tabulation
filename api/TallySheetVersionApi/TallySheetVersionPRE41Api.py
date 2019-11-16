from app import db
from auth import authorize, EC_LEADERSHIP_ROLE, POLLING_DIVISION_REPORT_VERIFIER_ROLE
from auth.AuthConstants import DATA_EDITOR_ROLE
from exception import NotFoundException
from exception.messages import MESSAGE_CODE_TALLY_SHEET_NOT_FOUND
from orm.entities.Submission import TallySheet
from orm.entities.SubmissionVersion import TallySheetVersion
from orm.enums import TallySheetCodeEnum
from schemas import TallySheetVersionPRE41Schema, TallySheetVersionSchema
from util import RequestBody
from orm.entities.Dashboard import StatusPRE41
from orm.entities import Area
from orm.enums import AreaTypeEnum


@authorize(required_roles=[DATA_EDITOR_ROLE, POLLING_DIVISION_REPORT_VERIFIER_ROLE, EC_LEADERSHIP_ROLE])
def get_by_id(tallySheetId, tallySheetVersionId):
    tallySheet = TallySheet.get_by_id(tallySheetId=tallySheetId)
    if tallySheet is None:
        raise NotFoundException(
            message="Tally sheet not found (tallySheetId=%d)" % tallySheetId,
            code=MESSAGE_CODE_TALLY_SHEET_NOT_FOUND
        )

    result = TallySheetVersion.get_by_id(
        tallySheetId=tallySheetId,
        tallySheetVersionId=tallySheetVersionId
    )

    return TallySheetVersionPRE41Schema().dump(result).data


@authorize(required_roles=[DATA_EDITOR_ROLE])
def create(tallySheetId, body):
    request_body = RequestBody(body)
    tallySheet, tallySheetVersion = TallySheet.create_latest_version(
        tallySheetId=tallySheetId,
        tallySheetCode=TallySheetCodeEnum.PRE_41
    )

    election = tallySheet.submission.election
    voteType = election.electionName
    status = "Entered"
    electionId = election.parentElectionId
    countingCentreId = tallySheet.areaId
    area = Area.get_by_id(areaId=countingCentreId)
    electoralDistrictId = area.get_associated_areas(AreaTypeEnum.ElectoralDistrict, electionId=electionId)[0].areaId
    pollingDivisionId = None
    pollingDivisionResult = area.get_associated_areas(AreaTypeEnum.PollingDivision, electionId=electionId)
    if len(pollingDivisionResult) > 0:
        pollingDivisionId = area.get_associated_areas(AreaTypeEnum.PollingDivision, electionId=electionId)[0].areaId

    tally_sheet_content = request_body.get("content")
    is_complete = True
    if tally_sheet_content is not None:

        for row in tally_sheet_content:
            party_count_body = RequestBody(row)
            candidateId = party_count_body.get("candidateId")
            count = party_count_body.get("count")
            countInWords = party_count_body.get("countInWords")

            if (candidateId and count and countInWords) is not None:
                tallySheetVersion.add_row(
                    candidateId=candidateId,
                    count=count,
                    countInWords=countInWords
                )
            else:
                is_complete = False

            voteCount = party_count_body.get("count")
            pollingStationId = party_count_body.get("areaId")
            candidateId = party_count_body.get("candidateId")
            if election is not None:
                existingStatus = StatusPRE41.get_status_record(
                    electionId=electionId,
                    electoralDistrictId=electoralDistrictId,
                    pollingDivisionId=pollingDivisionId,
                    countingCentreId=countingCentreId,
                    pollingStationId=pollingStationId,
                    candidateId=candidateId
                )
                if existingStatus is None:
                    StatusPRE41.create(
                        voteType=voteType,
                        status=status,
                        electionId=electionId,
                        electoralDistrictId=electoralDistrictId,
                        pollingDivisionId=pollingDivisionId,
                        countingCentreId=countingCentreId,
                        pollingStationId=pollingStationId,
                        voteCount=voteCount,
                        candidateId=candidateId,

                    )
                else:
                    existingStatus.voteType = voteType,
                    existingStatus.electionId = electionId,
                    existingStatus.electoralDistrictId = electoralDistrictId,
                    existingStatus.pollingDivisionId = pollingDivisionId,
                    existingStatus.countingCentreId = countingCentreId,
                    existingStatus.pollingStationId = pollingStationId,
                    existingStatus.voteCount = voteCount,
                    existingStatus.candidateId = candidateId

    tally_sheet_summary_body = request_body.get("summary")
    if tally_sheet_summary_body is not None:
        rejectedVoteCount = tally_sheet_summary_body.get("rejectedVoteCount")

        if (electionId and rejectedVoteCount) is not None:
            tallySheetVersion.add_invalid_vote_count(
                electionId=electionId,
                rejectedVoteCount=rejectedVoteCount
            )
        else:
            is_complete = False

        voteCount = tally_sheet_summary_body.get("rejectedVoteCount")
        candidateId = None
        pollingStationId = None
        if election is not None:
            existingStatus = StatusPRE41.get_status_record(
                electionId=electionId,
                electoralDistrictId=electoralDistrictId,
                pollingDivisionId=pollingDivisionId,
                countingCentreId=countingCentreId,
                candidateId=candidateId
            )
            if existingStatus is None:
                StatusPRE41.create(
                    voteType=voteType,
                    status=status,
                    electionId=electionId,
                    electoralDistrictId=electoralDistrictId,
                    pollingDivisionId=pollingDivisionId,
                    countingCentreId=countingCentreId,
                    pollingStationId=pollingStationId,
                    voteCount=voteCount,
                    candidateId=candidateId,

                )
            else:
                existingStatus.voteType = voteType,
                existingStatus.electionId = electionId,
                existingStatus.electoralDistrictId = electoralDistrictId,
                existingStatus.pollingDivisionId = pollingDivisionId,
                existingStatus.countingCentreId = countingCentreId,
                existingStatus.voteCount = voteCount,
                existingStatus.pollingStationId = pollingStationId,
                existingStatus.candidateId = candidateId

    if is_complete:
        tallySheetVersion.set_complete()
    db.session.commit()

    return TallySheetVersionSchema().dump(tallySheetVersion).data
