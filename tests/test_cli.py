from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from celeritas.cli.app import app

runner = CliRunner()


@patch("celeritas.cli.app.run_all_tests")
def test_run_command(mock_run: MagicMock) -> None:
    mock_run.return_value.speedtest_ping_ms = 10.0
    mock_run.return_value.download_mbps = 100.0
    mock_run.return_value.upload_mbps = 50.0
    mock_run.return_value.gateway_ping_ms = 1.0
    mock_run.return_value.dns_ping_ms = 12.0

    result = runner.invoke(app, ["run"])
    assert result.exit_code == 0
    assert "100.00 Mbps" in result.stdout
    assert "Download" in result.stdout


@patch("celeritas.cli.app.run_all_tests")
def test_run_command_partial_metrics(mock_run: MagicMock) -> None:
    mock_run.return_value.speedtest_ping_ms = None
    mock_run.return_value.download_mbps = None
    mock_run.return_value.upload_mbps = None
    mock_run.return_value.gateway_ping_ms = None
    mock_run.return_value.dns_ping_ms = None
    result = runner.invoke(app, ["run"])
    assert result.exit_code == 0


@patch("celeritas.cli.app.uvicorn.run")
def test_serve_command(mock_uvicorn: MagicMock) -> None:
    result = runner.invoke(app, ["serve", "--host", "127.0.0.1", "--port", "8080"])
    assert result.exit_code == 0
    mock_uvicorn.assert_called_once()
