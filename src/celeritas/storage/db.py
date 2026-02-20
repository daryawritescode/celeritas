import sqlite3
import os
from contextlib import contextmanager
from celeritas.config import settings
from celeritas.models import CombinedResult

def init_db() -> None:
    os.makedirs(os.path.dirname(settings.celeritas_db_path), exist_ok=True)
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS test_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                download_mbps REAL,
                upload_mbps REAL,
                speedtest_ping_ms REAL,
                gateway_ping_ms REAL,
                dns_ping_ms REAL,
                public_ip TEXT,
                container_ip TEXT,
                host_ip TEXT,
                location TEXT
            )
        ''')
        conn.commit()

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(settings.celeritas_db_path, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def save_result(result: CombinedResult) -> int:
    init_db()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO test_results (
                timestamp, download_mbps, upload_mbps, speedtest_ping_ms,
                gateway_ping_ms, dns_ping_ms, public_ip, container_ip, host_ip, location
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            result.timestamp.isoformat(),
            result.download_mbps,
            result.upload_mbps,
            result.speedtest_ping_ms,
            result.gateway_ping_ms,
            result.dns_ping_ms,
            result.public_ip,
            result.container_ip,
            result.host_ip,
            result.location
        ))
        conn.commit()
        if cursor.lastrowid:
            return cursor.lastrowid
        return 0

def fetch_all_results() -> list[CombinedResult]:
    init_db()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM test_results ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        
    return [
        CombinedResult(**dict(row)) for row in rows
    ]
