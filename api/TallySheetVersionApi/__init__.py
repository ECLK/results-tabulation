from util import RequestBody
from schemas import Ballot_Schema as Schema, TallySheetVersionPRE41Schema
from orm.entities import TallySheetVersion
from orm.entities.TallySheetVersion import TallySheetVersionPRE41
from orm.entities.Result.PartyWiseResult import PartyCount
from orm.enums import TallySheetCodeEnum



def get_all(tallySheetId):
    result = TallySheetVersion.get_all(tallySheetId=tallySheetId)

    return Schema(many=True).dump(result).data


def create(body):
    request_body = RequestBody(body)
    result = TallySheetVersion.create(
        tallySheetId=request_body.get("tallySheetId")
    )

    return Schema().dump(result).data, 201
