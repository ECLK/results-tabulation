import random

from flask import Response

from app import db
from orm.entities.Submission.TallySheet import TallySheetModel
from tests.util import get_tally_sheet_code


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
            f"/tally-sheet/{self.tally_sheet_code}/{tally_sheet_id}/version", json=payload)
        assert response.status_code == 200
        json_response = response.get_json()
        for key in ["contentUrl", "createdAt", "createdBy", "htmlUrl", "tallySheetId", "tallySheetVersionId"]:
            assert key in json_response.keys()

    def test_get_by_id(self, test_client):
        random_tally_sheet: TallySheetModel = random.choice(self.tally_sheets)
        tally_sheet_id = random_tally_sheet.tallySheetId

        count = 75
        invalid_vote_category_id = 2

        from orm.entities.SubmissionVersion import TallySheetVersion

        tally_sheet_version = random_tally_sheet.create_empty_version()

        response: Response = test_client.get(
            f"/tally-sheet/{self.tally_sheet_code}/{tally_sheet_id}/version/{tally_sheet_version.tallySheetVersionId}")
        assert response.status_code == 200
        json_response = response.get_json()
        assert len(json_response) > 0
        match_element = [x for x in json_response.get('content') if x.get(
            'invalidVoteCategoryId') == invalid_vote_category_id][0]
        assert match_element.get(
            "invalidVoteCategoryId") == invalid_vote_category_id
        assert match_element.get("count") == count
        assert "categoryDescription" in match_element.keys()
