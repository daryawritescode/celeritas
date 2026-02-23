from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from celeritas.server.app import api
from datetime import datetime, timezone
from celeritas.models import CombinedResult

client = TestClient(api)


def test_read_root() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


@patch("celeritas.server.app.fetch_all_results")
def test_get_results(mock_fetch: MagicMock) -> None:
    mock_fetch.return_value = [
        CombinedResult(timestamp=datetime.now(timezone.utc), download_mbps=100.0)
    ]
    response = client.get("/api/results")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["download_mbps"] == 100.0


def test_get_state() -> None:
    response = client.get("/api/state")
    assert response.status_code == 200
    data = response.json()
    assert "is_running" in data
    assert "progress" in data
    assert "message" in data


@patch("celeritas.server.app.run_all_tests")
def test_trigger_run(mock_run: MagicMock) -> None:
    response = client.post("/api/run")
    assert response.status_code == 200
    assert response.json()["status"] == "Test started in background."
