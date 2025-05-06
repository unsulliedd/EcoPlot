// EcoPlot/static/js/index.js
document.addEventListener('DOMContentLoaded', function () {
    // Animate elements when they come into view
    const animateOnScroll = function () {
        const elements = document.querySelectorAll('.feature-card, .step-card, .benefit-item');

        elements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const elementVisible = 150;

            if (elementTop < window.innerHeight - elementVisible) {
                element.classList.add('animate-fade-in-up');
            }
        });
    };

    // Run animation check on scroll
    window.addEventListener('scroll', animateOnScroll);

    // Run initial animation check
    animateOnScroll();

    // Counter animation for statistics
    const startCounters = function () {
        const statNumbers = document.querySelectorAll('.stat-number');

        statNumbers.forEach(statNumber => {
            const elementTop = statNumber.getBoundingClientRect().top;
            const elementVisible = 150;

            if (elementTop < window.innerHeight - elementVisible && !statNumber.classList.contains('counted')) {
                statNumber.classList.add('counted');

                const targetValue = statNumber.textContent;
                const isPercentage = targetValue.includes('%');
                const isMoney = targetValue.includes('$');
                const isPlus = targetValue.includes('+');

                let cleanValue = targetValue.replace(/[^0-9.]/g, '');
                let countTo = parseFloat(cleanValue);

                let prefix = isMoney ? '$' : '';
                let suffix = isPercentage ? '%' : (isPlus ? '+' : '');

                // Start at 0
                statNumber.textContent = prefix + '0' + suffix;

                let duration = 2000; // 2 seconds
                let startTime = null;

                // Animation function
                const countUp = function (timestamp) {
                    if (!startTime) startTime = timestamp;

                    const progress = Math.min((timestamp - startTime) / duration, 1);
                    const currentCount = Math.floor(progress * countTo);

                    statNumber.textContent = prefix + currentCount + suffix;

                    if (progress < 1) {
                        window.requestAnimationFrame(countUp);
                    } else {
                        statNumber.textContent = targetValue; // Ensure final value is exactly as specified
                    }
                };

                window.requestAnimationFrame(countUp);
            }
        });
    };

    // Run counter animation on scroll
    window.addEventListener('scroll', startCounters);

    // Run initial counter check
    startCounters();
});