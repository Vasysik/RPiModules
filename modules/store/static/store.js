document.addEventListener("DOMContentLoaded", function() {
    const moduleContainer = document.getElementById('available-modules');

    fetch('/store/api/available_modules')
        .then(response => response.json())
        .then(modules => {
            console.log('Received modules:', modules); // Добавим лог для отладки
            if (modules.length === 0) {
                moduleContainer.innerHTML = '<p>All available modules are already installed.</p>';
                return;
            }
            moduleContainer.innerHTML = ''; // Очистим контейнер перед добавлением новых модулей
            modules.forEach(module => {
                const moduleElement = document.createElement('div');
                moduleElement.className = 'module-card';
                moduleElement.innerHTML = `
                    <h3>${module.name}</h3>
                    <p>${module.description || 'No description available.'}</p>
                    <button class="install-btn" onclick="installModule('${module.repo}', '${module.name}')">Install</button>
                `;
                moduleContainer.appendChild(moduleElement);
            });
        })
        .catch(error => {
            console.error('Error fetching available modules:', error);
            moduleContainer.innerHTML = '<p>Error loading modules. Please try again later.</p>';
        });
});

function installModule(repo, name) {
    fetch('/store/api/install_module', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ repo, name }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            location.reload();
        } else {
            alert('Error: ' + (data.error || 'Unknown error occurred'));
        }
    })
    .catch(error => {
        console.error('Error installing module:', error);
        alert('Error installing module. Please try again.');
    });
}