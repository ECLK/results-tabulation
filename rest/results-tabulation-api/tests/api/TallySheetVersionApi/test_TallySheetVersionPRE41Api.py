import random

from flask import Response

from app import db
from orm.entities.Submission.TallySheet import TallySheetModel
from tests.util import get_tally_sheet_code


class TestTallySheetVersionPRE41Api:
    tally_sheet_code = "PRE-41"
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
                    "candidateId": 1,
                    "count": 100,
                    "countInWords": "One hundred"
                }
            ]
        }

        response: Response = test_client.post(f"/tally-sheet/{self.tally_sheet_code}/{tally_sheet_id}/version",
                                              json=payload)
        assert response.status_code == 200
        json_response = response.get_json()
        for key in ["contentUrl", "createdAt", "createdBy", "htmlUrl", "tallySheetId", "tallySheetVersionId"]:
            assert key in json_response.keys()

    def test_get_by_id(self, test_client):
        random_tally_sheet: TallySheetModel = random.choice(self.tally_sheets)
        tally_sheet_id = random_tally_sheet.tallySheetId

        candidate_id = 2
        count = 200
        count_in_words = "Two hundred"

        from orm.entities.SubmissionVersion import TallySheetVersion

        tally_sheet_version = random_tally_sheet.create_empty_version()

        db.session.commit()

        response: Response = test_client.get(
            f"/tally-sheet/{self.tally_sheet_code}/{tally_sheet_id}/version/{tally_sheet_version.tallySheetVersionId}")
        assert response.status_code == 200
        json_response = response.get_json()
        assert len(json_response) > 0
        match_element = [x for x in json_response.get('content') if x.get('candidateId') == candidate_id][0]
        assert match_element.get("candidateId") == candidate_id
        assert match_element.get("count") == count
        assert match_element.get("countInWords") == count_in_words
