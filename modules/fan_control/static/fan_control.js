function updateCurrentStatus() {
    fetch('/fan_control/api/current')
        .then(response => response.json())
        .then(data => {
            document.getElementById('current-temperature').textContent = data.Temperature + '°C';
            document.getElementById('fan-state').textContent = data['Fan State'];
        })
        .catch(error => console.error('Error:', error));
}

function loadSettings() {
    fetch('/fan_control/api/settings')
        .then(response => response.json())
        .then(settings => {
            document.getElementById('tempOn').value = settings.tempOn;
            document.getElementById('tempOff').value = settings.tempOff;
            document.getElementById('mode').value = settings.mode;
        })
        .catch(error => console.error('Error:', error));
}

function saveSettings() {
    const settings = {
        tempOn: document.getElementById('tempOn').value,
        tempOff: document.getElementById('tempOff').value,
        mode: document.getElementById('mode').value
    };

    fetch('/fan_control/api/settings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(settings)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            alert('Settings updated successfully');
        } else {
            alert('Error updating settings');
        }
    })
    .catch(error => console.error('Error:', error));
}

setInterval(updateCurrentStatus, 1000);

window.onload = function() {
    updateCurrentStatus();
    loadSettings();
};