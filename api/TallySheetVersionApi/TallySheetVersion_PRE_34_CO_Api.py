from app import db
from auth import authorize, EC_LEADERSHIP_ROLE
from auth.AuthConstants import DATA_EDITOR_ROLE
from exception import NotFoundException
from orm.enums import TallySheetCodeEnum
from orm.entities.Submission import TallySheet
from orm.entities.SubmissionVersion.TallySheetVersion import TallySheetVersion_PRE_34_CO
from orm.entities.TallySheetVersionRow import TallySheetVersionRow_PRE_34_CO_PREFERENCES
from schemas import TallySheetVersionPRE41Schema, TallySheetVersionSchema
from util import RequestBody


@authorize(required_roles=[DATA_EDITOR_ROLE, EC_LEADERSHIP_ROLE])
def get_by_id(tallySheetId, tallySheetVersionId):
    tallySheet = TallySheet.get_by_id(tallySheetId=tallySheetId)
    if tallySheet is None:
        raise NotFoundException("Tally sheet not found. (tallySheetId=%d)" % tallySheetId)

    result = TallySheetVersionPRE41.get_by_id(
        tallySheetId=tallySheetId,
        tallySheetVersionId=tallySheetVersionId
    )

    return TallySheetVersionPRE41Schema().dump(result).data


@authorize(required_roles=[DATA_EDITOR_ROLE, EC_LEADERSHIP_ROLE])
def get_all(tallySheetId):
    tallySheet = TallySheet.get_by_id(tallySheetId=tallySheetId)
    if tallySheet is None:
        raise NotFoundException("Tally sheet not found. (tallySheetId=%d)" % tallySheetId)

    result = TallySheetVersionPRE41.get_all(
        tallySheetId=tallySheetId
    )

    return TallySheetVersionPRE41Schema(many=True).dump(result).data


@authorize(required_roles=[DATA_EDITOR_ROLE])
def create(tallySheetId, body):
    tallySheet = TallySheet.get_by_id(tallySheetId=tallySheetId)
    if tallySheet is None:
        raise NotFoundException("Tally sheet not found. (tallySheetId=%d)" % tallySheetId)

    request_body = RequestBody(body)

    tallySheet, tallySheetVersion = TallySheet.create_latest_version(
        tallySheetId=tallySheetId,
        tallySheetCode=TallySheetCodeEnum.PRE_34_CO
    )


    tally_sheet_content = request_body.get("content")
    print(request_body.body)
    if tally_sheet_content is not None:
        for row in tally_sheet_content:
            party_count_body = RequestBody(row)
            row = tallySheetVersion.add_row(
                candidateId=party_count_body.get("candidateId"),
                notCountedBallotPapers=party_count_body.get("notCountedBallotPapers"),
                remainingBallotPapers=party_count_body.get("remainingBallotPapers")
            )
            # Lets add the preferences for the above row
            preferences = party_count_body.get("preferences")
            for preference in preferences:
                print(preference)
                TallySheetVersionRow_PRE_34_CO_PREFERENCES.create(
                    tallySheetVersionRowId=row.tallySheetVersionRowId,
                    candidateId=preference.get('candidateId'),
                    no2ndPreferences=preference.get('no2rdPreferences'),
                    no3rdPreferences=preference.get('no3rdPreferences')
                )


    tally_sheet_summary_body = request_body.get("summary")
    if tally_sheet_summary_body is not None:
        tallySheetVersion.add_invalid_vote_count(
            electionId=tallySheetVersion.submission.electionId,
            rejectedVoteCount=tally_sheet_summary_body.get("rejectedVoteCount")
        )


    db.session.commit()

    return TallySheetVersionSchema().dump(tallySheetVersion).data
