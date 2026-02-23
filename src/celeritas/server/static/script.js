let myChart;
let liveChart;
let lastUpdateTimestamp = 0;
let liveData = {
    downloads: [],
    uploads: [],
    labels: []
};

async function fetchResults() {
    try {
        const response = await fetch('/api/results');
        const data = await response.json();

        if (data.length > 0) {
            updateDashboard(data);
        }
    } catch (e) {
        console.error("Failed to fetch results", e);
    }
}

async function pollState() {
    try {
        const response = await fetch('/api/state');
        const state = await response.json();

        const wrapper = document.getElementById('live-chart-wrapper');
        const msg = document.getElementById('progress-msg');
        const bar = document.getElementById('progress-bar');

        if (state.is_running) {
            wrapper.style.display = 'block';
            msg.innerText = state.message;
            bar.style.width = `${state.progress}%`;

            if (state.current_download || state.current_upload) {
                updateLiveChart(state);
            }
        } else {
            wrapper.style.display = 'none';
            if (bar.style.width === '100%') {
                fetchResults();
                resetBtnState();
            }
        }
    } catch (e) {
        console.error("Failed to poll state", e);
    }
}

function updateLiveChart(state) {
    if (!liveChart) {
        initLiveChart();
    }

    const now = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    
    // Only add if data is new or changed
    const lastDl = liveData.downloads[liveData.downloads.length - 1];
    if (state.current_download !== lastDl) {
        liveData.labels.push(now);
        liveData.downloads.push(state.current_download || 0);
        liveData.uploads.push(state.current_upload || 0);

        if (liveData.labels.length > 20) {
            liveData.labels.shift();
            liveData.downloads.shift();
            liveData.uploads.shift();
        }

        liveChart.update();
    }
}

function initLiveChart() {
    const ctx = document.getElementById('liveChart').getContext('2d');
    liveChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: liveData.labels,
            datasets: [
                {
                    label: 'Current Download',
                    data: liveData.downloads,
                    borderColor: '#3b82f6',
                    borderWidth: 2,
                    tension: 0.4,
                    pointRadius: 0
                },
                {
                    label: 'Current Upload',
                    data: liveData.uploads,
                    borderColor: '#8b5cf6',
                    borderWidth: 2,
                    tension: 0.4,
                    pointRadius: 0
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { beginAtZero: true, grid: { color: 'rgba(255, 255, 255, 0.05)' } },
                x: { display: false }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}

function updateDashboard(data) {
    if (data.length === 0) return;

    const latest = data[0];
    const currentTstamp = new Date(latest.timestamp).getTime();

    document.getElementById('val-download').innerHTML = `${latest.download_mbps ? latest.download_mbps.toFixed(1) : '--'} <span>Mbps</span>`;
    document.getElementById('val-upload').innerHTML = `${latest.upload_mbps ? latest.upload_mbps.toFixed(1) : '--'} <span>Mbps</span>`;
    document.getElementById('val-ping').innerHTML = `${latest.speedtest_ping_ms ? latest.speedtest_ping_ms.toFixed(0) : '--'} <span>ms</span>`;

    const gwPing = (typeof latest.gateway_ping_ms === 'number') ? latest.gateway_ping_ms.toFixed(2) : '--';
    const dnsPing = (typeof latest.dns_ping_ms === 'number') ? latest.dns_ping_ms.toFixed(2) : '--';
    document.getElementById('val-network').innerHTML = `${gwPing} <span>/</span> ${dnsPing} <span>ms</span>`;

    document.getElementById('val-public-ip').innerText = latest.public_ip || '--';
    document.getElementById('val-location').innerText = latest.location || '--';
    document.getElementById('val-container-ip').innerText = latest.container_ip || '--';
    document.getElementById('val-host-ip').innerText = latest.host_ip || '--';

    updateHistoryChart([...data].reverse());
    lastUpdateTimestamp = currentTstamp;
}

function updateHistoryChart(data) {
    const ctx = document.getElementById('historyChart').getContext('2d');
    const labels = data.map(d => new Date(d.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }));
    const downloads = data.map(d => d.download_mbps || 0);
    const uploads = data.map(d => d.upload_mbps || 0);

    if (myChart) myChart.destroy();

    Chart.defaults.color = '#94a3b8';
    Chart.defaults.font.family = 'Outfit';

    myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Download (Mbps)',
                    data: downloads,
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    borderWidth: 3,
                    tension: 0.4,
                    fill: true
                },
                {
                    label: 'Upload (Mbps)',
                    data: uploads,
                    borderColor: '#8b5cf6',
                    backgroundColor: 'rgba(139, 92, 246, 0.1)',
                    borderWidth: 3,
                    tension: 0.4,
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { position: 'top' } },
            scales: {
                y: { beginAtZero: true, grid: { color: 'rgba(255, 255, 255, 0.05)' } },
                x: { grid: { display: false } }
            }
        }
    });
}

function resetBtnState() {
    const btn = document.getElementById('runTestBtn');
    const ring = document.getElementById('status-ring');
    btn.disabled = false;
    btn.innerText = 'Run Test';
    ring.classList.remove('testing');
    document.getElementById('results-header').innerText = 'Last Test Results';
    
    // Reset live data for next run
    liveData = { downloads: [], uploads: [], labels: [] };
    if (liveChart) {
        liveChart.destroy();
        liveChart = null;
    }
}

document.getElementById('runTestBtn').addEventListener('click', async () => {
    const btn = document.getElementById('runTestBtn');
    const ring = document.getElementById('status-ring');
    btn.disabled = true;
    btn.innerText = 'Testing...';
    ring.classList.add('testing');
    document.getElementById('results-header').innerText = 'Current Test Results';

    try {
        await fetch('/api/run', { method: 'POST' });
        // Start fast polling
        const poller = setInterval(() => {
            pollState();
            if (btn.disabled === false) clearInterval(poller);
        }, 1000);
    } catch (e) {
        console.error("Test failed", e);
        resetBtnState();
    }
});

fetchResults();
setInterval(pollState, 5000); // Background polling
