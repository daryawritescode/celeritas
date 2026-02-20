import socket
import struct
import subprocess
from ping3 import ping
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
        delay = ping(host, timeout=2)
        if delay is not None:
            return delay * 1000
    except Exception as e:
        logger.warning(f"Failed to ping {host}: {e}")
    return None

def get_dns_servers() -> list[str]:
    servers = []
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

def get_tailscale_ip() -> str | None:
    try:
        output = subprocess.check_output(["tailscale", "ip", "-4"], text=True, timeout=2)
        lines = output.strip().split("\n")
        if lines:
            return lines[0].strip()
    except Exception as e:
        logger.warning(f"Failed to get tailscale IP: {e}")
    return None

def run_network_metrics() -> tuple[float | None, float | None, float | None]:
    gateway = get_default_gateway_linux()
    gateway_ping = None
    if gateway:
        logger.info(f"Pinging gateway {gateway}")
        gateway_ping = measure_latency(gateway)
    
    dns_servers = get_dns_servers()
    dns_ping = None
    if dns_servers:
        # Default to the first found DNS server for tracking
        dns_server = dns_servers[0]
        logger.info(f"Pinging DNS server {dns_server}")
        dns_ping = measure_latency(dns_server)
        
    ts_ip = get_tailscale_ip()
    ts_ping = None
    if ts_ip:
        logger.info(f"Pinging Tailscale IP {ts_ip}")
        ts_ping = measure_latency(ts_ip)
    
    return gateway_ping, dns_ping, ts_ping
