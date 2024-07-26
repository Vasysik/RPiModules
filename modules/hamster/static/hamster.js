document.addEventListener('DOMContentLoaded', function() {
    fetchData('/hamster/api/status', 'status-container', renderStatus);
    fetchData('/hamster/api/config', 'config-container', renderConfig);
    fetchData('/hamster/api/current', 'current-container', renderCurrent);
    fetchTokens();
});

function fetchData(url, containerId, renderFunction) {
    fetch(url)
        .then(response => response.json())
        .then(data => renderFunction(data, containerId))
        .catch(error => console.error('Error:', error));
}

function renderStatus(data, containerId) {
    const container = document.getElementById(containerId);
    container.innerHTML = `
        <p><strong>Status:</strong> ${data.status}</p>
        <p><strong>End Time:</strong> ${data.endString}</p>
    `;
}

function renderConfig(data, containerId) {
    const container = document.getElementById(containerId);
    container.innerHTML = Object.entries(data)
        .map(([key, value]) => `<p><strong>${key}:</strong> ${value}</p>`)
        .join('');
}

function renderCurrent(data, containerId) {
    const container = document.getElementById(containerId);
    container.innerHTML = Object.entries(data)
        .map(([user, userData]) => `
            <h3>${user}</h3>
            <p><strong>Balance Coins:</strong> ${userData.balanceCoins}</p>
            <p><strong>Balance Keys:</strong> ${userData.balanceKeys}</p>
            <p><strong>Available Taps:</strong> ${userData.availableTaps}</p>
            <p><strong>Earn Per Tap:</strong> ${userData.earnPerTap}</p>
            <p><strong>Level:</strong> ${userData.level}</p>
        `)
        .join('');
}

function fetchTokens() {
    fetch('/hamster/api/tokens')
        .then(response => response.json())
        .then(tokens => {
            const tokenList = document.getElementById('tokenList');
            tokenList.innerHTML = tokens.map(token => 
                `<li>${token} <button class="btn btn-sm btn-danger" onclick="removeToken('${token}')">Remove</button></li>`
            ).join('');
        })
        .catch(error => console.error('Error:', error));
}

function removeToken(token) {
    fetch('/hamster/api/tokens', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token: token }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            fetchTokens();
        } else {
            alert('Error removing token');
        }
    });
}

document.getElementById('addTokenForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const token = document.getElementById('newToken').value;
    fetch('/hamster/api/tokens', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token: token }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            fetchTokens();
            document.getElementById('newToken').value = '';
        } else {
            alert('Error adding token');
        }
    });
});