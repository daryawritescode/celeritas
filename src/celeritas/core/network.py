import socket
import struct
import urllib.request
import json
from ping3 import ping  # type: ignore[import-untyped]
from loguru import logger


def get_default_gateway_linux() -> str | None:
    try:
        with open("/proc/net/route") as f:
            for line in f:
                fields = line.strip().split()
                # Check for default route (destination 00000000 and RTF_UP flag)
                if len(fields) < 4 or fields[1] != '00000000' or not int(fields[3], 16) & 2:
                    continue
                # The gateway is the 3rd field in hex format
                return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))
    except Exception as e:
        logger.warning(f"Could not read default gateway: {e}")
    return None


def measure_latency(host: str) -> float | None:
    try:
        delay: float | bool | None = ping(host, timeout=2)
        if delay is not None and isinstance(delay, float):
            return delay * 1000
    except Exception as e:
        logger.warning(f"Failed to ping {host}: {e}")
    return None


def get_dns_servers() -> list[str]:
    servers: list[str] = []
    try:
        with open("/etc/resolv.conf") as f:
            for line in f:
                if line.startswith("nameserver"):
                    parts = line.strip().split()
                    if len(parts) > 1:
                        servers.append(parts[1])
    except Exception as e:
        logger.warning(f"Could not read DNS servers: {e}")
    return servers


def get_ip_info() -> dict[str, str | None]:
    info: dict[str, str | None] = {
        "container_ip": None,
        "host_ip": get_default_gateway_linux(),
        "public_ip": None,
        "location": None
    }

    try:
        info["container_ip"] = socket.gethostbyname(socket.gethostname())
    except Exception as e:
        logger.warning(f"Could not get container IP: {e}")

    try:
        req = urllib.request.Request("https://ipinfo.io/json", headers={'User-Agent': 'curl/7.68.0'})
        with urllib.request.urlopen(req, timeout=2) as response:
            data: dict[str, str] = json.loads(response.read().decode())
            info["public_ip"] = data.get("ip")
            loc = [data.get("city"), data.get("region"), data.get("country")]
            loc_filtered = [x for x in loc if x]
            if loc_filtered:
                info["location"] = ", ".join(loc_filtered)
    except Exception as e:
        logger.warning(f"Failed to get public IP info: {e}")

    return info


def run_network_metrics() -> tuple[float | None, float | None, dict[str, str | None]]:
    gateway = get_default_gateway_linux()
    gateway_ping: float | None = None
    if gateway:
        logger.info(f"Pinging gateway {gateway}")
        gateway_ping = measure_latency(gateway)

    dns_servers = get_dns_servers()
    dns_ping: float | None = None
    if dns_servers:
        # Default to the first found DNS server for tracking
        dns_server = dns_servers[0]
        logger.info(f"Pinging DNS server {dns_server}")
        dns_ping = measure_latency(dns_server)

    ip_info = get_ip_info()

    return gateway_ping, dns_ping, ip_info
