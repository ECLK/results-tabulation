from flask import Response


class TestTallySheet:

    def test_get_all(self, test_client):
        response: Response = test_client.get("/tally-sheet")
        assert response.status_code == 200
