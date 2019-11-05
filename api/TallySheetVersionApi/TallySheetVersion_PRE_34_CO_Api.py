from app import db
from auth import authorize, EC_LEADERSHIP_ROLE, POLLING_DIVISION_REPORT_VERIFIER_ROLE
from auth.AuthConstants import DATA_EDITOR_ROLE
from exception import NotFoundException
from exception.messages import MESSAGE_CODE_TALLY_SHEET_NOT_FOUND
from orm.entities.Submission import TallySheet
from orm.entities.SubmissionVersion import TallySheetVersion
from orm.enums import TallySheetCodeEnum
from schemas import TallySheetVersion_PRE_34_CO_Schema, TallySheetVersionSchema
from util import RequestBody
from orm.entities.Election import get_by_id as GetElectionById
from orm.entities.Dashboard import StatusPRE34
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

    return TallySheetVersion_PRE_34_CO_Schema().dump(result).data


@authorize(required_roles=[DATA_EDITOR_ROLE])
def create(tallySheetId, body):
    request_body = RequestBody(body)
    tallySheet, tallySheetVersion = TallySheet.create_latest_version(
        tallySheetId=tallySheetId,
        tallySheetCode=TallySheetCodeEnum.PRE_34_CO
    )

    election = tally_sheet.submission.election
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

    tallySheetVersion.set_complete()  # TODO: valid before setting complete. Refer to PRE_34_CO
    tally_sheet_content = request_body.get("content")
    if tally_sheet_content is not None:
        for row in tally_sheet_content:
            party_count_body = RequestBody(row)
            tallySheetVersion.add_row(
                electionId=tallySheetVersion.submission.electionId,
                candidateId=party_count_body.get("candidateId"),
                preferenceCount=party_count_body.get("preferenceCount"),
                preferenceNumber=party_count_body.get("preferenceNumber"),
            )
            pollingStationId = party_count_body.get("areaId")
            candidateId = party_count_body.get("candidateId")
            preferenceCount = party_count_body.get("preferenceCount")
            preferenceNumber = party_count_body.get("preferenceNumber")
            secondPreferenceCount = 0
            thirdPreferenceCount = 0

            if preferenceNumber == 2:
                secondPreferenceCount = preferenceCount
            if preferenceNumber == 3:
                thirdPreferenceCount = preferenceCount

            if election is not None:
                existingStatus = StatusPRE34.get_status_record(
                    electionId=electionId,
                    electoralDistrictId=electoralDistrictId,
                    pollingDivisionId=pollingDivisionId,
                    countingCentreId=countingCentreId,
                    pollingStationId=pollingStationId,
                    candidateId=candidateId
                )
                if existingStatus is None:
                    StatusPRE34.create(
                        voteType=voteType,
                        status=status,
                        electionId=electionId,
                        electoralDistrictId=electoralDistrictId,
                        pollingDivisionId=pollingDivisionId,
                        countingCentreId=countingCentreId,
                        secondPreferenceCount=secondPreferenceCount,
                        thirdPreferenceCount=thirdPreferenceCount,
                        candidateId=candidateId
                    )
                else:
                    existingStatus.voteType = voteType
                    existingStatus.electionId = electionId
                    existingStatus.electoralDistrictId = electoralDistrictId
                    existingStatus.pollingDivisionId = pollingDivisionId
                    existingStatus.countingCentreId = countingCentreId
                    existingStatus.pollingStationId = pollingStationId
                    if secondPreferenceCount is not 0:
                        existingStatus.secondPreferenceCount = secondPreferenceCount
                    if thirdPreferenceCount is not 0:
                        existingStatus.thirdPreferenceCount = thirdPreferenceCount
                    existingStatus.candidateId = candidateId

    db.session.commit()

    return TallySheetVersionSchema().dump(tallySheetVersion).data
