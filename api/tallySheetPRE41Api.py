from config import db
from models import TallySheetPRE41Model, TallySheetPRE41PartyModel


def create(body, tallysheetVersion):
    return _create_tallysheet_PRE_41(body, tallysheetVersion)


def _create_tallysheet_PRE_41__party(body, tallysheetVersion):
    print("##########", body["party_wise_results"])

    for party_wise_entry_body in body["party_wise_results"]:
        new_tallysheet_PRE_41__party = TallySheetPRE41PartyModel(
            partyId=party_wise_entry_body["partyId"],
            voteCount=party_wise_entry_body["voteCount"],
            tallySheetVersionId=tallysheetVersion.tallySheetVersionId
        )

        db.session.add(new_tallysheet_PRE_41__party)
        db.session.commit()


def _create_tallysheet_PRE_41(body, tallysheetVersion):
    new_tallysheet_PRE_41 = TallySheetPRE41Model(
        tallySheetId=tallysheetVersion.tallySheetId,
        tallySheetVersionId=tallysheetVersion.tallySheetVersionId,
        electoralDistrictId=body["electoralDistrictId"],
        pollingDivisionId=body["pollingDivisionId"],
        countingCentreId=body["countingCentreId"],
    )

    db.session.add(new_tallysheet_PRE_41)
    db.session.commit()

    _create_tallysheet_PRE_41__party(body, tallysheetVersion)

    return new_tallysheet_PRE_41
