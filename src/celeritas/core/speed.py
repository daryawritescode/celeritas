import speedtest  # type: ignore[import-untyped]
from loguru import logger


def run_speedtest() -> tuple[float, float, float]:
    logger.info("Starting speedtest (this may take a minute)...")
    st = speedtest.Speedtest(secure=True)
    st.get_best_server()
    download: float = st.download() / 1_000_000  # Convert to Mbps
    upload: float = st.upload() / 1_000_000      # Convert to Mbps
    ping_ms: float = st.results.ping
    logger.info(f"Speedtest completed: {download:.2f} Mbps down, {upload:.2f} Mbps up, {ping_ms} ms ping")
    return download, upload, ping_ms
