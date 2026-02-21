let myChart;
let lastUpdateTimestamp = 0;

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

function updateDashboard(data) {
    if (data.length === 0) return;

    // Determine if new data arrived based on timestamp
    const latest = data[0];
    const currentTstamp = new Date(latest.timestamp).getTime();

    document.getElementById('val-download').innerHTML = `${latest.download_mbps ? latest.download_mbps.toFixed(1) : '--'} <span>Mbps</span>`;
    document.getElementById('val-upload').innerHTML = `${latest.upload_mbps ? latest.upload_mbps.toFixed(1) : '--'} <span>Mbps</span>`;
    document.getElementById('val-ping').innerHTML = `${latest.speedtest_ping_ms ? latest.speedtest_ping_ms.toFixed(0) : '--'} <span>ms</span>`;

    const gwPing = latest.gateway_ping_ms ? latest.gateway_ping_ms.toFixed(2) : '--';
    const dnsPing = latest.dns_ping_ms ? latest.dns_ping_ms.toFixed(2) : '--';
    document.getElementById('val-network').innerHTML = `${gwPing} <span>/</span> ${dnsPing} <span>ms</span>`;

    document.getElementById('val-public-ip').innerText = latest.public_ip || '--';
    document.getElementById('val-location').innerText = latest.location || '--';
    document.getElementById('val-container-ip').innerText = latest.container_ip || '--';
    document.getElementById('val-host-ip').innerText = latest.host_ip || '--';

    updateChart([...data].reverse());

    if (currentTstamp > lastUpdateTimestamp && lastUpdateTimestamp !== 0) {
        // New record appeared! 
        resetBtnState();
    }
    lastUpdateTimestamp = currentTstamp;
}

function updateChart(data) {
    const ctx = document.getElementById('historyChart').getContext('2d');

    const labels = data.map(d => {
        const date = new Date(d.timestamp);
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    });

    const downloads = data.map(d => d.download_mbps || 0);
    const uploads = data.map(d => d.upload_mbps || 0);

    if (myChart) {
        myChart.destroy();
    }

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
                    fill: true,
                    pointBackgroundColor: '#3b82f6',
                },
                {
                    label: 'Upload (Mbps)',
                    data: uploads,
                    borderColor: '#8b5cf6',
                    backgroundColor: 'rgba(139, 92, 246, 0.1)',
                    borderWidth: 3,
                    tension: 0.4,
                    fill: true,
                    pointBackgroundColor: '#8b5cf6',
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { mode: 'index', intersect: false },
            plugins: {
                legend: { position: 'top', labels: { usePointStyle: true, boxWidth: 8 } }
            },
            scales: {
                y: { beginAtZero: true, grid: { color: 'rgba(255, 255, 255, 0.05)' } },
                x: { grid: { display: false } }
            }
        }
    });
}

let pollingInterval;

function resetBtnState() {
    const btn = document.getElementById('runTestBtn');
    const ring = document.getElementById('status-ring');
    btn.disabled = false;
    btn.innerText = 'Run Test';
    ring.classList.remove('testing');
    if (pollingInterval) clearInterval(pollingInterval);
}

document.getElementById('runTestBtn').addEventListener('click', async () => {
    const btn = document.getElementById('runTestBtn');
    const ring = document.getElementById('status-ring');
    btn.disabled = true;
    btn.innerText = 'Testing...';
    ring.classList.add('testing');

    try {
        await fetch('/api/run', { method: 'POST' });

        // Wait till result drops
        let attempts = 0;
        pollingInterval = setInterval(async () => {
            attempts++;
            await fetchResults();

            if (attempts > 30) { // 30 * 4s = 120s max
                resetBtnState();
            }
        }, 4000);
    } catch (e) {
        console.error("Test failed", e);
        resetBtnState();
    }
});

// Initial load
fetchResults();
