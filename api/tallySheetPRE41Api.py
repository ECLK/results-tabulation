from config import db
from models import TallySheetPRE41Model, TallySheetPRE41PartyModel
from util import RequestBody


def create(body, tallysheetVersion):
    return _create_tallysheet_PRE_41(body, tallysheetVersion)


def _create_tallysheet_PRE_41__party_list_item(body, tallysheetVersion):
    request_body = RequestBody(body)
    new_tallysheet_PRE_41__party = TallySheetPRE41PartyModel(
        partyId=request_body.get("partyId"),
        voteCount=request_body.get("voteCount"),
        tallySheetVersionId=tallysheetVersion.tallySheetVersionId
    )

    db.session.add(new_tallysheet_PRE_41__party)
    db.session.commit()


def _create_tallysheet_PRE_41__party_list(body, tallysheetVersion):
    request_body = RequestBody(body)
    print("##########", body["party_wise_results"])

    for party_wise_entry_body in request_body.get("party_wise_results"):
        _create_tallysheet_PRE_41__party_list_item(party_wise_entry_body, tallysheetVersion)


def _create_tallysheet_PRE_41(body, tallysheetVersion):
    request_body = RequestBody(body)
    new_tallysheet_PRE_41 = TallySheetPRE41Model(
        tallySheetId=tallysheetVersion.tallySheetId,
        tallySheetVersionId=tallysheetVersion.tallySheetVersionId,
        electoralDistrictId=request_body.get("electoralDistrictId"),
        pollingDivisionId=request_body.get("pollingDivisionId"),
        countingCentreId=request_body.get("countingCentreId"),
    )

    db.session.add(new_tallysheet_PRE_41)
    db.session.commit()

    _create_tallysheet_PRE_41__party_list(body, tallysheetVersion)

    return new_tallysheet_PRE_41
