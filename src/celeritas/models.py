from datetime import datetime
from pydantic import BaseModel

class CombinedResult(BaseModel):
    id: int | None = None
    timestamp: datetime
    download_mbps: float | None = None
    upload_mbps: float | None = None
    speedtest_ping_ms: float | None = None
    gateway_ping_ms: float | None = None
    dns_ping_ms: float | None = None
    public_ip: str | None = None
    container_ip: str | None = None
    host_ip: str | None = None
    location: str | None = None

class TestState(BaseModel):
    is_running: bool = False
    progress: int = 0  # 0-100
    current_download: float | None = None
    current_upload: float | None = None
    current_ping: float | None = None
    message: str = "Idle"
