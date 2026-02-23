from datetime import datetime, timezone
from loguru import logger
from celeritas.core.speed import run_speedtest
from celeritas.core.network import run_network_metrics
from celeritas.models import CombinedResult
from celeritas.storage.db import save_result
from celeritas.core.state import current_state

def run_all_tests() -> CombinedResult:
    logger.info("Running all network and speed tests.")
    
    current_state.is_running = True
    current_state.progress = 10
    current_state.message = "Initializing speedtest..."
    
    dl, ul, sp_ping = None, None, None
    try:
        # We could enhance run_speedtest to provide progress, 
        # but for now we'll simulate steps.
        current_state.progress = 20
        current_state.message = "Running download test..."
        # In a real app we'd pass a callback to run_speedtest
        dl, ul, sp_ping = run_speedtest()
        
        current_state.progress = 60
        current_state.message = "Download/Upload complete. Checking latency..."
        current_state.current_download = dl
        current_state.current_upload = ul
        current_state.current_ping = sp_ping
    except Exception as e:
        logger.error(f"Speedtest failed: {e}")
        current_state.message = f"Speedtest failed: {e}"

    gw_ping, dns_ping, ip_info = run_network_metrics()
    current_state.progress = 90
    current_state.message = "Finalizing results..."

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
        
    current_state.progress = 100
    current_state.is_running = False
    current_state.message = "Idle"
    
    return result
