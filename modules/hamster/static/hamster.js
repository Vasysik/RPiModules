document.addEventListener('DOMContentLoaded', function() {
    function loadData() {
        fetch('/hamster/api/current')
            .then(response => response.json())
            .then(data => {
                document.getElementById('current-status').textContent = data.status;
                document.getElementById('end-time').textContent = data.endString;
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
                    `<div>${token} <button onclick="removeToken('${token}')">Remove</button></div>`
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

    loadData();

    setInterval(loadData, 30000);
});