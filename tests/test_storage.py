import pytest
from datetime import datetime, timezone
import os
from unittest.mock import MagicMock, patch
from celeritas.models import CombinedResult
from celeritas.storage.db import init_db, save_result, fetch_all_results, get_db_connection
from celeritas.config import settings

@pytest.fixture(autouse=True)
def setup_test_db(tmp_path):
    db_path = tmp_path / "test.db"
    settings.celeritas_db_path = str(db_path)
    init_db()
    yield
    if os.path.exists(db_path):
        os.remove(db_path)

def test_init_db():
    init_db()
    assert os.path.exists(settings.celeritas_db_path)

def test_get_db_connection_close(tmp_path):
    with get_db_connection() as conn:
        assert conn is not None

def test_save_and_fetch():
    result = CombinedResult(
        timestamp=datetime.now(timezone.utc),
        download_mbps=100.0,
        upload_mbps=50.0,
        speedtest_ping_ms=10.0,
        gateway_ping_ms=1.5,
        dns_ping_ms=12.3,
        public_ip="1.2.3.4",
        container_ip="172.17.0.2",
        host_ip="172.17.0.1",
        location="Seattle, WA, US"
    )
    
    row_id = save_result(result)
    assert row_id > 0
    
    results = fetch_all_results()
    assert len(results) == 1
    assert results[0].download_mbps == 100.0
    assert results[0].upload_mbps == 50.0


@patch("celeritas.storage.db.get_db_connection")
@patch("celeritas.storage.db.init_db")
def test_save_result_no_rowid(mock_init_db, mock_get_conn):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.lastrowid = 0
    mock_conn.cursor.return_value = mock_cursor
    
    mock_ctx = MagicMock()
    mock_ctx.__enter__.return_value = mock_conn
    mock_get_conn.return_value = mock_ctx

    result = CombinedResult(
        timestamp=datetime.now(timezone.utc),
        download_mbps=100.0,
        upload_mbps=50.0,
        speedtest_ping_ms=10.0,
        gateway_ping_ms=1.5,
        dns_ping_ms=12.3,
        public_ip="1.2.3.4",
        container_ip="172.17.0.2",
        host_ip="172.17.0.1",
        location="Seattle, WA, US"
    )
    
    row_id = save_result(result)
    assert row_id == 0
