from fastapi.testclient import TestClient
from celeritas.server.app import api
from unittest.mock import patch
from datetime import datetime, timezone
from celeritas.models import CombinedResult

client = TestClient(api)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

@patch("celeritas.server.app.fetch_all_results")
def test_get_results(mock_fetch):
    mock_fetch.return_value = [
        CombinedResult(timestamp=datetime.now(timezone.utc), download_mbps=100.0)
    ]
    response = client.get("/api/results")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["download_mbps"] == 100.0

@patch("celeritas.server.app.run_all_tests")
def test_trigger_run(mock_run):
    # Testing the async background task execution manually relies on starlette BackgroundTask tests
    # We just ensure the endpoint returns the correct status.
    response = client.post("/api/run")
    assert response.status_code == 200
    assert response.json()["status"] == "Test started in background."
