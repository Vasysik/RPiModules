document.addEventListener("DOMContentLoaded", function() {
    fetch('/api/modules')
        .then(response => response.json())
        .then(modules => {
            const moduleGrid = document.querySelector('.module-grid');
            moduleGrid.innerHTML = '';
            modules.forEach(module => {
                const moduleButton = document.createElement('a');
                moduleButton.href = `/${module.route}`;
                moduleButton.className = 'module-button';

                const moduleIcon = document.createElement('img');
                moduleIcon.src = `/${module.icon}`;
                moduleIcon.alt = module.name;
                moduleButton.appendChild(moduleIcon);

                const moduleName = document.createElement('span');
                moduleName.textContent = module.name;
                moduleButton.appendChild(moduleName);

                moduleButton.addEventListener('click', function() {
                    const buttons = document.querySelectorAll('.module-button');
                    buttons.forEach(button => button.classList.remove('active'));

                    this.classList.add('active');
                    localStorage.setItem('selectedModule', module.route);
                });

                if (localStorage.getItem('selectedModule') === module.route) {
                    moduleButton.classList.add('active');
                }

                moduleGrid.appendChild(moduleButton);
            });
        })
        .catch(error => console.error('Error fetching module data:', error));
});