// Main JS for AI Resume Screener

document.addEventListener('DOMContentLoaded', function() {
    // Dark Mode Toggle
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) {
        darkModeToggle.addEventListener('change', () => {
            document.body.classList.toggle('dark-mode');
            localStorage.setItem('dark-mode', document.body.classList.contains('dark-mode'));
        });

        // Check local storage
        if (localStorage.getItem('dark-mode') === 'true') {
            darkModeToggle.checked = true;
            document.body.classList.add('dark-mode');
        }
    }

    // Match Distribution Chart (on Dashboard)
    const ctx = document.getElementById('matchDistributionChart');
    if (ctx) {
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['High (>80%)', 'Medium (50-80%)', 'Low (<50%)'],
                datasets: [{
                    data: [12, 19, 3],
                    backgroundColor: ['#10b981', '#f59e0b', '#ef4444'],
                    borderWidth: 0
                }]
            },
            options: {
                cutout: '70%',
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
});
