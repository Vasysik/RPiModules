let selectedUser = null;
function loadData() {
    fetch('/hamster/api/status')
    .then(response => response.json())
        .then(data => {
            document.getElementById('current-status').textContent = data.status;
            document.getElementById('end-string').textContent = data.endString;
        });

    fetch('/hamster/api/users')
        .then(response => response.json())
        .then(data => {
            const userSelect = document.getElementById('user-select');
            userSelect.innerHTML = '';
            data.users.forEach(user => {
                const option = document.createElement('option');
                option.value = user;
                option.text = user;
                userSelect.appendChild(option);
            });
            if (selectedUser) { userSelect.value = selectedUser; } else { selectedUser = userSelect.value; }
            document.getElementById('user-select').addEventListener('change', function() {
                selectedUser = this.value;
                loadData();
                updateGraph();
            });
        });

    if (selectedUser) {
        fetch(`/hamster/api/current/${selectedUser}`)
            .then(response => response.json())
            .then(data => {
                document.getElementById('earn-passive-hour').textContent = parseInt(data.earnPassivePerHour).toLocaleString();
                document.getElementById('balance-coins').textContent = parseInt(data.balanceCoins).toLocaleString();
                document.getElementById('balance-keys').textContent = parseInt(data.balanceKeys).toLocaleString();
                document.getElementById('earn-per-tap').textContent = parseInt(data.earnPerTap).toLocaleString();
                document.getElementById('user-level').textContent = parseInt(data.level).toLocaleString();
            });
    }

    loadTokens();
}

function loadTokens() {
    fetch('/hamster/api/tokens')
        .then(response => response.json())
        .then(tokens => {
            const tokenList = document.getElementById('token-list');
            tokenList.innerHTML = tokens.map(token => {
                const username = extractUsername(token);
                return `
                    <div class="token-item">
                        <div class="token-username">${username}</div>
                        <div class="token-text" title="${token}">${token}</div>
                        <button class="remove-token" onclick="removeToken('${token}')" title="Remove token">×</button>
                    </div>
                `;
            }).join('');
        });
}

function extractUsername(token) {
    try {
        const userDataStr = decodeURIComponent(token.split('user=')[1].split('&')[0]);
        const userData = JSON.parse(userDataStr);
        return userData.username || 'Unknown';
    } catch (error) {
        console.error('Error extracting username:', error);
        return 'Unknown';
    }
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

function loadConfig() {
    fetch('/hamster/api/config')
        .then(response => response.json())
        .then(config => {
            document.getElementById('auto-buy-upgrade').checked = config.Auto_Buy_Upgrade === 'ON';
            document.getElementById('auto-complete-combo').checked = config.Auto_Complete_Combo === 'ON';
            document.getElementById('auto-complete-cipher').checked = config.Auto_Complete_Cipher === 'ON';
            document.getElementById('auto-complete-mini-game').checked = config.Auto_Complete_Mini_Game === 'ON';
            document.getElementById('auto-complete-tasks').checked = config.Auto_Complete_Tasks === 'ON';
        })
        .catch(error => console.error('Error:', error));
}

function saveConfig() {
    const config = {
        Auto_Buy_Upgrade: document.getElementById('auto-buy-upgrade').checked ? 'ON' : 'OFF',
        Auto_Complete_Combo: document.getElementById('auto-complete-combo').checked ? 'ON' : 'OFF',
        Auto_Complete_Cipher: document.getElementById('auto-complete-cipher').checked ? 'ON' : 'OFF',
        Auto_Complete_Mini_Game: document.getElementById('auto-complete-mini-game').checked ? 'ON' : 'OFF',
        Auto_Complete_Tasks: document.getElementById('auto-complete-tasks').checked ? 'ON' : 'OFF'
    };

    fetch('/hamster/api/config', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(config)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            console.log('Config updated successfully');
        } else {
            alert('Error updating config');
        }
    })
    .catch(error => console.error('Error:', error));
}

function updateGraph() {
    const graphType = document.getElementById('graph-type').value;
    const timeRange = document.getElementById('time-range').value;
    const selectedUser = document.getElementById('user-select').value;

    fetch(`/hamster/api/graph_data?type=${graphType}&range=${timeRange}&user=${selectedUser}`)
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
                margin: {l: 70, r: 30, b: 50, t: 50, pad: 4},
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

document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('save-config').addEventListener('click', saveConfig);
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
});

window.onload = function() {
    loadConfig();
};