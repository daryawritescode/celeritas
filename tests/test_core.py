from unittest.mock import patch, mock_open, MagicMock
from celeritas.core.speed import run_speedtest
from celeritas.core.network import (
    get_default_gateway_linux,
    measure_latency,
    run_network_metrics,
    get_dns_servers,
    get_ip_info,
)
from celeritas.core.runner import run_all_tests

@patch("celeritas.core.speed.speedtest.Speedtest")
def test_run_speedtest(mock_speedtest_class):
    mock_st = MagicMock()
    mock_speedtest_class.return_value = mock_st
    mock_st.download.return_value = 100_000_000
    mock_st.upload.return_value = 50_000_000
    mock_st.results.ping = 15.0

    dl, ul, p = run_speedtest()
    assert dl == 100.0
    assert ul == 50.0
    assert p == 15.0

def test_get_default_gateway_linux():
    m_open = mock_open(read_data="Iface\tDestination\tGateway \tFlags\tRefCnt\tUse\tMetric\neth0\t00000000\t0101A8C0\t0003\n")
    with patch("builtins.open", m_open):
        gw = get_default_gateway_linux()
        assert gw == "192.168.1.1"

def test_get_default_gateway_linux_no_default():
    m_open = mock_open(read_data="Iface\tDestination\tGateway \tFlags\tRefCnt\tUse\tMetric\neth0\t0101A8C0\t00000000\t0001\n")
    with patch("builtins.open", m_open):
        gw = get_default_gateway_linux()
        assert gw is None

def test_get_default_gateway_linux_exception():
    with patch("builtins.open", side_effect=Exception("Read error")):
        gw = get_default_gateway_linux()
        assert gw is None

def test_get_dns_servers():
    m_open = mock_open(read_data="nameserver 1.1.1.1\nnameserver 8.8.8.8\n")
    with patch("builtins.open", m_open):
        servers = get_dns_servers()
        assert servers == ["1.1.1.1", "8.8.8.8"]

def test_get_dns_servers_empty():
    m_open = mock_open(read_data="options edns0\n")
    with patch("builtins.open", m_open):
        servers = get_dns_servers()
        assert servers == []

def test_get_dns_servers_exception():
    with patch("builtins.open", side_effect=Exception("Read error")):
        servers = get_dns_servers()
        assert servers == []

@patch("urllib.request.urlopen")
def test_get_ip_info(mock_urlopen):
    mock_response = MagicMock()
    mock_response.read.return_value = b'{"ip": "8.8.8.8", "city": "Seattle", "region": "Washington", "country": "US"}'
    mock_response.__enter__.return_value = mock_response
    mock_urlopen.return_value = mock_response
    
    with patch("celeritas.core.network.socket.gethostbyname", return_value="172.17.0.2"):
        with patch("celeritas.core.network.get_default_gateway_linux", return_value="172.17.0.1"):
            info = get_ip_info()
            assert info["public_ip"] == "8.8.8.8"
            assert info["location"] == "Seattle, Washington, US"
            assert info["container_ip"] == "172.17.0.2"
            assert info["host_ip"] == "172.17.0.1"

@patch("celeritas.core.network.ping")
def test_measure_latency(mock_ping):
    mock_ping.return_value = 0.015
    assert measure_latency("1.1.1.1") == 15.0

@patch("celeritas.core.network.ping")
def test_measure_latency_fails(mock_ping):
    mock_ping.return_value = None
    assert measure_latency("1.1.1.1") is None
    
    mock_ping.side_effect = Exception("error")
    assert measure_latency("1.1.1.1") is None

@patch("celeritas.core.network.get_default_gateway_linux")
@patch("celeritas.core.network.get_dns_servers")
@patch("celeritas.core.network.get_ip_info")
@patch("celeritas.core.network.measure_latency")
def test_run_network_metrics(mock_lat, mock_ip, mock_dns, mock_gw):
    mock_gw.return_value = "192.168.1.1"
    mock_dns.return_value = ["8.8.8.8"]
    mock_ip.return_value = {"public_ip": "1.1.1.1"}
    
    mock_lat.side_effect = [1.5, 12.0]
    
    gw, dns, ip_info = run_network_metrics()
    assert gw == 1.5
    assert dns == 12.0
    assert ip_info["public_ip"] == "1.1.1.1"
    
    # Check calls
    assert mock_lat.call_args_list[0][0][0] == "192.168.1.1"
    assert mock_lat.call_args_list[1][0][0] == "8.8.8.8"

@patch("celeritas.core.runner.run_speedtest")
@patch("celeritas.core.runner.run_network_metrics")
@patch("celeritas.core.runner.save_result")
def test_run_all_tests(mock_save, mock_net, mock_speed):
    mock_speed.return_value = (100.0, 50.0, 15.0)
    mock_net.return_value = (1.5, 12.0, {"public_ip": "8.8.8.8"})
    
    res = run_all_tests()
    assert res.download_mbps == 100.0
    assert mock_save.called

@patch("celeritas.core.runner.run_speedtest")
@patch("celeritas.core.runner.run_network_metrics")
@patch("celeritas.core.runner.save_result")
def test_run_all_tests_with_speedtest_error(mock_save, mock_net, mock_speed):
    mock_speed.side_effect = Exception("Fail")
    mock_net.return_value = (1.5, 12.0, {"public_ip": "8.8.8.8"})
    mock_save.side_effect = Exception("DB Fail")
    
    res = run_all_tests()
    assert res.download_mbps is None
    assert res.gateway_ping_ms == 1.5
