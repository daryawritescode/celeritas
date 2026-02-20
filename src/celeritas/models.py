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
    tailscale_ping_ms: float | None = None
