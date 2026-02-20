from datetime import datetime, timezone
from loguru import logger
from celeritas.core.speed import run_speedtest
from celeritas.core.network import run_network_metrics
from celeritas.models import CombinedResult
from celeritas.storage.db import save_result

def run_all_tests() -> CombinedResult:
    logger.info("Running all network and speed tests.")
    
    dl, ul, sp_ping = None, None, None
    try:
        dl, ul, sp_ping = run_speedtest()
    except Exception as e:
        logger.error(f"Speedtest failed: {e}")

    gw_ping, dns_ping, ip_info = run_network_metrics()

    result = CombinedResult(
        timestamp=datetime.now(timezone.utc),
        download_mbps=dl,
        upload_mbps=ul,
        speedtest_ping_ms=sp_ping,
        gateway_ping_ms=gw_ping,
        dns_ping_ms=dns_ping,
        public_ip=ip_info.get("public_ip"),
        container_ip=ip_info.get("container_ip"),
        host_ip=ip_info.get("host_ip"),
        location=ip_info.get("location")
    )
    
    try:
        save_result(result)
        logger.info("Test results saved to database.")
    except Exception as e:
        logger.error(f"Failed to save test results: {e}")
        
    return result
