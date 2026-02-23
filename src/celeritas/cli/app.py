import typer
import uvicorn
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from celeritas.core.runner import run_all_tests
from celeritas.config import settings

app = typer.Typer(help="Celeritas Speedtest & Network Utility")


@app.command()
def run() -> None:
    """Run a speedtest and network latency check"""
    console = Console()
    console.print("[bold cyan]Starting tests...[/bold cyan]")
    result = run_all_tests()

    table = Table(show_header=False, box=None)
    table.add_column("Metric", style="bold magenta", justify="right")
    table.add_column("Value", style="cyan")

    if result.speedtest_ping_ms:
        table.add_row("📍 Ping", f"[bold white]{result.speedtest_ping_ms:.2f} ms[/]")
    if result.download_mbps:
        table.add_row("⬇️  Download", f"[bold green]{result.download_mbps:.2f} Mbps[/]")
    if result.upload_mbps:
        table.add_row("⬆️  Upload", f"[bold green]{result.upload_mbps:.2f} Mbps[/]")

    table.add_row("", "")

    if result.gateway_ping_ms:
        table.add_row("🖥️  Gateway Ping", f"[bold white]{result.gateway_ping_ms:.2f} ms[/]")
    if result.dns_ping_ms:
        table.add_row("🌍 DNS Ping", f"[bold white]{result.dns_ping_ms:.2f} ms[/]")

    table.add_row("", "")

    if result.public_ip:
        table.add_row("🌐 Public IP", f"[bold yellow]{result.public_ip}[/]")
    if result.location:
        table.add_row("🗺️  Location", f"[bold yellow]{result.location}[/]")
    if result.container_ip:
        table.add_row("📦 Container IP", f"[bold yellow]{result.container_ip}[/]")
    if result.host_ip:
        table.add_row("🏠 Host IP", f"[bold yellow]{result.host_ip}[/]")

    console.print("\n")
    console.print(Panel(table, title="[bold blue]🏎️  Celeritas Results[/]", border_style="blue", expand=False))


@app.command()
def docs() -> None:
    """Print the documentation URL"""
    typer.echo("Integrated Documentation is available at: http://celeritas.localhost/docs/")


@app.command()
def schedule(
    interval: int = typer.Option(None, help="Interval in minutes (overrides CELERITAS_SCHEDULE_INTERVAL)"),
    once: bool = False,
) -> None:
    """Run tests on a schedule"""
    # Priority: CLI argument > Environment Variable > Default (handled by Settings)
    run_interval = interval if interval is not None else settings.celeritas_schedule_interval

    typer.echo(f"Starting scheduler: Running every {run_interval} minutes.")
    while True:
        try:
            run_all_tests()
        except Exception as e:
            typer.echo(f"Scheduled test failed: {e}", err=True)

        if once:
            break

        time.sleep(run_interval * 60)  # pragma: no cover


@app.command()
def serve(host: str = "0.0.0.0", port: int = settings.celeritas_port) -> None:
    """Start the Celeritas Web Dashboard"""
    typer.echo(f"Starting server on {host}:{port}")
    uvicorn.run("celeritas.server.app:api", host=host, port=port, reload=False)


if __name__ == "__main__":  # pragma: no cover
    app()
