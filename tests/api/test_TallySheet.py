from flask import Response


class TestTallySheet:

    def test_get_all(self, test_client):
        response: Response = test_client.get("/tally-sheet")
        assert response.status_code == 200
        assert len(response.get_json()) > 0

    def test_get_all_pre_all_island_results_by_electoral_districts(self, test_client):
        response: Response = test_client.get(
            "/tally-sheet?tallySheetCode=PRE_ALL_ISLAND_RESULTS_BY_ELECTORAL_DISTRICTS",
            headers=test_client.http_headers
        )
        assert response.status_code == 200
        assert len(response.get_json()) > 0

    def test_get_all_pre_all_island_results(self, test_client):
        response: Response = test_client.get(
            "/tally-sheet?tallySheetCode=PRE_ALL_ISLAND_RESULTS", headers=test_client.http_headers
        )
        assert response.status_code == 200
        assert len(response.get_json()) > 0

    def test_get_all_pre_30_ed(self, test_client):
        response: Response = test_client.get(
            "/tally-sheet?tallySheetCode=PRE-30-ED", headers=test_client.http_headers
        )
        assert response.status_code == 200
        assert len(response.get_json()) > 0

    def test_get_all_pre_30_pd(self, test_client):
        response: Response = test_client.get(
            "/tally-sheet?tallySheetCode=PRE-30-PD", headers=test_client.http_headers
        )
        assert response.status_code == 200
        assert len(response.get_json()) > 0

    def test_get_all_pre_41(self, test_client):
        response: Response = test_client.get(
            "/tally-sheet?tallySheetCode=PRE-41", headers=test_client.http_headers
        )
        assert response.status_code == 200
        assert len(response.get_json()) > 0

    def test_get_all_ce_201(self, test_client):
        response: Response = test_client.get(
            "/tally-sheet?tallySheetCode=CE-201", headers=test_client.http_headers
        )
        assert response.status_code == 200
        assert len(response.get_json()) > 0

    def test_get_all_pre_21(self, test_client):
        response: Response = test_client.get(
            "/tally-sheet?tallySheetCode=PRE-21", headers=test_client.http_headers
        )
        assert response.status_code == 200
        assert len(response.get_json()) > 0
