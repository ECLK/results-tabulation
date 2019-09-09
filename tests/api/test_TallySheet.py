from flask import Response


class TestTallySheet:

    def test_get_all(self, test_client):
        response: Response = test_client.get("/tally-sheet")
        assert response.status_code == 200
        assert len(response.get_json()) > 0

    def test_get_all_PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS(self, test_client):
        response: Response = test_client.get(
            "/tally-sheet?tallySheetCode=PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS"
        )
        assert response.status_code == 200
        assert len(response.get_json()) > 0

    def test_get_all_PRE_ALL_ISLAND_RESULTS(self, test_client):
        response: Response = test_client.get(
            "/tally-sheet?tallySheetCode=PRE_ALL_ISLAND_RESULTS"
        )
        assert response.status_code == 200
        assert len(response.get_json()) > 0

    def test_get_all_PRE_30_ED(self, test_client):
        response: Response = test_client.get(
            "/tally-sheet?tallySheetCode=PRE-30-ED"
        )
        assert response.status_code == 200
        assert len(response.get_json()) > 0

    def test_get_all_PRE_30_PD(self, test_client):
        response: Response = test_client.get(
            "/tally-sheet?tallySheetCode=PRE-30-PD"
        )
        assert response.status_code == 200
        assert len(response.get_json()) > 0

    def test_get_all_PRE_41(self, test_client):
        response: Response = test_client.get(
            "/tally-sheet?tallySheetCode=PRE-41"
        )
        assert response.status_code == 200
        assert len(response.get_json()) > 0

    def test_get_all_CE_201(self, test_client):
        response: Response = test_client.get(
            "/tally-sheet?tallySheetCode=CE-201"
        )
        assert response.status_code == 200
        assert len(response.get_json()) > 0

    def test_get_all_PRE_21(self, test_client):
        response: Response = test_client.get(
            "/tally-sheet?tallySheetCode=PRE-21"
        )
        assert response.status_code == 200
        assert len(response.get_json()) > 0
