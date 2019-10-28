import random

from flask import Response

from api.TallySheetVersionApi import TallySheetVersionPRE21Api
from app import db
from orm.entities.Submission.TallySheet import TallySheetModel
from util import get_tally_sheet_code


class TestTallySheetVersionPRE21Api:
    tally_sheet_code = "PRE-21"
    tally_sheets = []

    @classmethod
    def setup_class(cls):
        cls.tally_sheets = TallySheetModel.query.filter(
            TallySheetModel.tallySheetCode == get_tally_sheet_code(f"{cls.tally_sheet_code}")).all()

    def test_create(self, test_client):
        random_tally_sheet: TallySheetModel = random.choice(self.tally_sheets)
        tally_sheet_id = random_tally_sheet.tallySheetId

        payload = {
            "content": [
                {
                    "count": 50,
                    "invalidVoteCategoryId": 1
                }
            ]
        }

        response: Response = test_client.post(
            f"/tally-sheet/{self.tally_sheet_code}/{tally_sheet_id}/version", json=payload,
            headers=test_client.http_headers)
        assert response.status_code == 200
        json_response = response.get_json()
        for key in ["contentUrl", "createdAt", "createdBy", "htmlUrl", "tallySheetId", "tallySheetVersionId"]:
            assert key in json_response.keys()

    def test_get_by_id(self, test_client):
        random_tally_sheet: TallySheetModel = random.choice(self.tally_sheets)
        tally_sheet_id = random_tally_sheet.tallySheetId

        # add tally sheet data
        tally_sheet_data = {
            "content": [
                {
                    "count": 75,
                    "invalidVoteCategoryId": 2
                }
            ]
        }

        tally_sheet_version_id = None

        with test_client.application.test_request_context(environ_base={'REMOTE_ADDR': '1.2.3.4'},
                                                          headers=test_client.http_headers) as test_request_ctx:
            test_request_ctx.connexion_context = {}
            tally_sheet = TallySheetVersionPRE21Api.create(tally_sheet_id, tally_sheet_data)
            tally_sheet_version_id = tally_sheet['tallySheetVersionId']

        response: Response = test_client.get(
            f"/tally-sheet/{self.tally_sheet_code}/{tally_sheet_id}/version/{tally_sheet_version_id}",
            headers=test_client.http_headers)
        assert response.status_code == 200
        json_response = response.get_json()
        assert len(json_response) > 0
        match_element = [x for x in json_response.get('content') if
                         x.get('invalidVoteCategoryId') == tally_sheet_data["content"][0]["invalidVoteCategoryId"]][0]
        assert match_element.get("invalidVoteCategoryId") == tally_sheet_data["content"][0]["invalidVoteCategoryId"]
        assert match_element.get("count") == tally_sheet_data["content"][0]["count"]
