import speedtest
from loguru import logger

def run_speedtest() -> tuple[float, float, float]:
    logger.info("Starting speedtest (this may take a minute)...")
    st = speedtest.Speedtest(secure=True)
    st.get_best_server()
    download = st.download() / 1_000_000  # Convert to Mbps
    upload = st.upload() / 1_000_000      # Convert to Mbps
    ping = st.results.ping
    logger.info(f"Speedtest completed: {download:.2f} Mbps down, {upload:.2f} Mbps up, {ping} ms ping")
    return download, upload, ping
