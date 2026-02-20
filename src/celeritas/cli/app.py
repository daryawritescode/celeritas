import typer
import uvicorn
from celeritas.core.runner import run_all_tests
from celeritas.config import settings

app = typer.Typer(help="Celeritas Speedtest & Network Utility")

@app.command()
def run():
    """Run a speedtest and network latency check"""
    typer.echo("Starting tests...")
    result = run_all_tests()
    typer.echo("\n--- Results ---")
    if result.speedtest_ping_ms:
        typer.echo(f"Ping: {result.speedtest_ping_ms} ms")
    if result.download_mbps:
        typer.echo(f"Download: {result.download_mbps:.2f} Mbps")
    if result.upload_mbps:
        typer.echo(f"Upload: {result.upload_mbps:.2f} Mbps")
    if result.gateway_ping_ms:
        typer.echo(f"Gateway Ping: {result.gateway_ping_ms:.2f} ms")
    if result.dns_ping_ms:
        typer.echo(f"DNS (1.1.1.1) Ping: {result.dns_ping_ms:.2f} ms")

@app.command()
def serve(host: str = "0.0.0.0", port: int = settings.celeritas_port):
    """Start the Celeritas Web Dashboard"""
    typer.echo(f"Starting server on {host}:{port}")
    uvicorn.run("celeritas.server.app:api", host=host, port=port, reload=False)

if __name__ == "__main__":
    app()
