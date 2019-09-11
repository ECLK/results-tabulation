import random

from flask import Response

from orm.entities.Submission.TallySheet import TallySheetModel
from util import get_tally_sheet_code


class TestTallySheetVersionPRE41Api:
    tally_sheets = []

    @classmethod
    def setup_class(cls):
        cls.tally_sheets = TallySheetModel.query.filter(
            TallySheetModel.tallySheetCode == get_tally_sheet_code("PRE-41")).all()

    def test_create(self, test_client):
        random_tally_sheet: TallySheetModel = self.tally_sheets[random.randint(0, len(self.tally_sheets))]
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

        response: Response = test_client.post(f"/tally-sheet/PRE-41/{tally_sheet_id}/version", json=payload)
        assert response.status_code == 200

    def test_get_by_id(self, test_client):
        random_tally_sheet: TallySheetModel = self.tally_sheets[random.randint(0, len(self.tally_sheets))]
        tally_sheet_id = random_tally_sheet.tallySheetId

        # create tally sheet and query for the same
        candidate_id = 2
        count = 200
        count_in_words = "Two hundred"

        payload = {
            "content": [
                {
                    "candidateId": candidate_id,
                    "count": count,
                    "countInWords": count_in_words
                }
            ]
        }

        response: Response = test_client.post(f"/tally-sheet/PRE-41/{tally_sheet_id}/version", json=payload)
        tally_sheet_version_id = response.get_json().get('tallySheetVersionId')

        response: Response = test_client.get(f"/tally-sheet/PRE-41/{tally_sheet_id}/version/{tally_sheet_version_id}")
        assert response.status_code == 200
        json_response = response.get_json()
        assert len(json_response) > 0
        match_element = [x for x in json_response.get('content') if x.get('candidateId') == candidate_id][0]
        assert match_element.get("count") == count
        assert match_element.get("countInWords") == count_in_words
