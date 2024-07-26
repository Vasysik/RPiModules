function loadData() {
    fetch('/hamster/api/status')
    .then(response => response.json())
        .then(data => {
            document.getElementById('current-status').textContent = data.status;
            document.getElementById('end-string').textContent = data.endString;
        });

    fetch('/hamster/api/current')
        .then(response => response.json())
        .then(data => {
            document.getElementById('earn-passive-hour').textContent = data.wasys.earnPassivePerHour;
            document.getElementById('balance-coins').textContent = data.wasys.balanceCoins;
            document.getElementById('balance-keys').textContent = data.wasys.balanceKeys;
            document.getElementById('available-taps').textContent = data.wasys.availableTaps;
            document.getElementById('earn-per-tap').textContent = data.wasys.earnPerTap;
            document.getElementById('user-level').textContent = data.wasys.level;
        });

    fetch('/hamster/api/config')
        .then(response => response.json())
        .then(data => {
            document.getElementById('auto-buy-upgrade').textContent = data['Auto Buy Upgrade'];
            document.getElementById('auto-complete-cipher').textContent = data['Auto Complete Cipher'];
            document.getElementById('auto-complete-combo').textContent = data['Auto Complete Combo'];
            document.getElementById('auto-complete-mini-game').textContent = data['Auto Complete Mini Game'];
            document.getElementById('auto-complete-tasks').textContent = data['Auto Complete Tasks'];
        });

    loadTokens();
}

function loadTokens() {
    fetch('/hamster/api/tokens')
        .then(response => response.json())
        .then(tokens => {
            const tokenList = document.getElementById('token-list');
            tokenList.innerHTML = tokens.map(token => 
                `<div>${token}</div><button onclick="removeToken('${token}')">Remove</button>`
            ).join('');
        });
}

function removeToken(token) {
    fetch('/hamster/api/tokens', {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token: token })
    })
    .then(response => response.json())
    .then(() => loadTokens());
}

document.getElementById('add-token').addEventListener('click', function() {
    const token = document.getElementById('new-token').value;
    fetch('/hamster/api/tokens', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token: token })
    })
    .then(response => response.json())
    .then(() => {
        loadTokens();
        document.getElementById('new-token').value = '';
    });
});

function updateGraph() {
    const graphType = document.getElementById('graph-type').value;
    const timeRange = document.getElementById('time-range').value;

    fetch(`/fan_control/api/graph_data?type=${graphType}&range=${timeRange}`)
        .then(response => response.json())
        .then(data => {
            const trace = {
                x: data.timestamps,
                y: data[graphType],
                type: 'scatter',
                mode: 'lines',
                line: {color: 'orange', width: 2},
                connectgaps: false
            };

            const layout = {
                title: graphType === 'earnPassivePerHour' ? 'Earn Passive Per Hour Graph' : 'Balance Coins Graph',
                xaxis: {
                    title: 'Time',
                    color: getComputedStyle(document.documentElement).getPropertyValue('--text-primary').trim()
                },
                yaxis: {
                    title: graphType === 'earnPassivePerHour' ? 'Earn Passive Per Hour' : 'Balance Coins',
                    color: getComputedStyle(document.documentElement).getPropertyValue('--text-primary').trim()
                },
                paper_bgcolor: getComputedStyle(document.documentElement).getPropertyValue('--bg-primary').trim(),
                plot_bgcolor: getComputedStyle(document.documentElement).getPropertyValue('--bg-primary').trim(),
                font: {
                    color: getComputedStyle(document.documentElement).getPropertyValue('--text-primary').trim()
                },
                margin: {l: 50, r: 50, b: 50, t: 50, pad: 4},
                showlegend: false,
                dragmode: false,
                displayModeBar: false
            };

            Plotly.newPlot('graph', [trace], layout, {responsive: true, displayModeBar: false});
        })
        .catch(error => console.error('Error:', error));
}

function updateGraphTheme() {
    const graphDiv = document.getElementById('graph');
    if (graphDiv && graphDiv.data && graphDiv.layout) {
        const update = {
            'paper_bgcolor': getComputedStyle(document.documentElement).getPropertyValue('--bg-primary').trim(),
            'plot_bgcolor': getComputedStyle(document.documentElement).getPropertyValue('--bg-primary').trim(),
            'font.color': getComputedStyle(document.documentElement).getPropertyValue('--text-primary').trim(),
            'xaxis.color': getComputedStyle(document.documentElement).getPropertyValue('--text-primary').trim(),
            'yaxis.color': getComputedStyle(document.documentElement).getPropertyValue('--text-primary').trim()
        };
        Plotly.relayout(graphDiv, update);
    }
}

// Добавим слушатель изменения темы
if (window.matchMedia) {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    mediaQuery.addListener(updateGraphTheme);
}

setInterval(loadData, 1000);
setInterval(updateGraph, 1000);

window.onload = function() {
    loadData();
    updateGraph();
};