// EcoPlot/static/js/theme.js
document.addEventListener('DOMContentLoaded', function () {
    // Initialize theme based on local storage or system preference
    const savedTheme = localStorage.getItem('ecoplot-theme');
    const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');

    // Set initial theme
    if (savedTheme === 'dark' || (!savedTheme && prefersDarkScheme.matches)) {
        document.body.classList.add('dark-mode');
        document.getElementById('theme-toggle').checked = true;
    }

    // Add event listener to theme toggle
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('change', function () {
            if (this.checked) {
                document.body.classList.add('dark-mode');
                localStorage.setItem('ecoplot-theme', 'dark');
            } else {
                document.body.classList.remove('dark-mode');
                localStorage.setItem('ecoplot-theme', 'light');
            }
        });
    }

    // Add event listener for system preference changes
    prefersDarkScheme.addEventListener('change', e => {
        // Only change based on system if user hasn't set preference
        if (!localStorage.getItem('ecoplot-theme')) {
            if (e.matches) {
                document.body.classList.add('dark-mode');
                if (themeToggle) themeToggle.checked = true;
            } else {
                document.body.classList.remove('dark-mode');
                if (themeToggle) themeToggle.checked = false;
            }
        }
    });
});