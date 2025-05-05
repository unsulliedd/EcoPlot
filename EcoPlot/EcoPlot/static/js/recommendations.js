// EcoPlot/static/js/recommendations.js

// Initialize when the document is ready
document.addEventListener('DOMContentLoaded', function () {
    fetchRecommendations();

    // Set up refresh button event listener
    document.getElementById('refreshRecommendations').addEventListener('click', function () {
        fetchRecommendations();
    });
});

/**
 * Fetches recommendations from the API
 */
async function fetchRecommendations() {
    try {
        // Show loading indicator, hide content and error
        document.getElementById('loadingRecommendations').style.display = 'block';
        document.getElementById('recommendationsContent').style.display = 'none';
        document.getElementById('recommendationError').style.display = 'none';

        // Fetch recommendations from the API
        const response = await fetch('/api/recommendations');
        const data = await response.json();

        if (data.success && data.recommendations && data.recommendations.success) {
            // Hide loading indicator and show content
            document.getElementById('loadingRecommendations').style.display = 'none';
            document.getElementById('recommendationsContent').style.display = 'block';

            // Display the recommendations
            displayRecommendations(data.recommendations.recommendations);
        } else {
            throw new Error(data.error || data.recommendations.error || 'Failed to get recommendations');
        }
    } catch (error) {
        console.error('Error fetching recommendations:', error);

        // Hide loading, show error
        document.getElementById('loadingRecommendations').style.display = 'none';
        document.getElementById('recommendationError').style.display = 'block';
        document.getElementById('errorMessage').textContent = error.message || 'Unable to generate recommendations. Please try again later.';
    }
}

/**
 * Displays recommendations in the UI
 * @param {Object} recommendations - The recommendations data
 */
function displayRecommendations(recommendations) {
    // Display summary metrics
    document.getElementById('monthlySavings').textContent = `$${formatNumber(recommendations.estimated_monthly_savings)}`;
    document.getElementById('carbonReduction').textContent = formatNumber(recommendations.carbon_reduction_potential);

    // Estimate total energy savings (this would be calculated based on device recommendations)
    let totalEnergySavings = 0;
    for (const deviceId in recommendations.device_recommendations) {
        const device = recommendations.device_recommendations[deviceId];
        if (device.estimated_savings) {
            totalEnergySavings += parseFloat(device.estimated_savings);
        }
    }
    document.getElementById('totalEnergySavings').textContent = `${formatNumber(totalEnergySavings)} kWh`;

    // Display overall recommendations
    const overallRecommendationsList = document.getElementById('overallRecommendations');
    overallRecommendationsList.innerHTML = '';

    if (recommendations.overall_recommendations && recommendations.overall_recommendations.length > 0) {
        recommendations.overall_recommendations.forEach(recommendation => {
            const li = document.createElement('li');
            li.innerHTML = `<i class="bi bi-check-circle-fill text-success"></i><span>${recommendation}</span>`;
            overallRecommendationsList.appendChild(li);
        });
    } else {
        overallRecommendationsList.innerHTML = '<li>No overall recommendations available at this time.</li>';
    }

    // Display device-specific recommendations
    const deviceRecommendationsDiv = document.getElementById('deviceRecommendations');
    deviceRecommendationsDiv.innerHTML = '';

    const deviceIds = Object.keys(recommendations.device_recommendations || {});
    if (deviceIds.length === 0) {
        deviceRecommendationsDiv.innerHTML = '<p class="text-center py-3">No device-specific recommendations available. Try adding more devices to get personalized advice.</p>';
    } else {
        deviceIds.forEach(deviceId => {
            const deviceRec = recommendations.device_recommendations[deviceId];

            // Create device card
            const deviceCard = document.createElement('div');
            deviceCard.className = 'card device-card';

            // Determine if we have a recommendation text or an array
            let recommendationText = '';
            if (typeof deviceRec.recommendation === 'string') {
                recommendationText = deviceRec.recommendation;
            } else if (Array.isArray(deviceRec.recommendation)) {
                recommendationText = deviceRec.recommendation.join('<br>');
            }

            // Format estimated savings
            let savingsHtml = '';
            if (deviceRec.estimated_savings) {
                savingsHtml = `<div class="savings-pill">
                    <i class="bi bi-graph-up-arrow me-1"></i>
                    Save ${formatNumber(deviceRec.estimated_savings)} kWh/month
                </div>`;
            }

            // Set card content
            deviceCard.innerHTML = `
                <div class="card-header">
                    ${deviceRec.name || `Device ${deviceId}`}
                </div>
                <div class="card-body">
                    <p>${recommendationText}</p>
                    ${savingsHtml}
                </div>
            `;

            deviceRecommendationsDiv.appendChild(deviceCard);
        });
    }

    // Display schedule optimization
    const scheduleOptimizationList = document.getElementById('scheduleOptimization');
    scheduleOptimizationList.innerHTML = '';

    if (recommendations.schedule_optimization && recommendations.schedule_optimization.length > 0) {
        recommendations.schedule_optimization.forEach(suggestion => {
            const li = document.createElement('li');
            li.innerHTML = `<i class="bi bi-clock text-primary"></i><span>${suggestion}</span>`;
            scheduleOptimizationList.appendChild(li);
        });
    } else {
        scheduleOptimizationList.innerHTML = '<li>No schedule optimization recommendations available.</li>';
    }

    // Display energy saving tips
    const energySavingTipsList = document.getElementById('energySavingTips');
    energySavingTipsList.innerHTML = '';

    if (recommendations.energy_saving_tips && recommendations.energy_saving_tips.length > 0) {
        recommendations.energy_saving_tips.forEach(tip => {
            const li = document.createElement('li');
            li.innerHTML = `<i class="bi bi-lightbulb text-warning"></i><span>${tip}</span>`;
            energySavingTipsList.appendChild(li);
        });
    } else {
        energySavingTipsList.innerHTML = '<li>No energy saving tips available.</li>';
    }
}

/**
 * Formats a number with commas and 2 decimal places
 * @param {number} number - The number to format
 * @returns {string} The formatted number
 */
function formatNumber(number) {
    // Handle null or undefined
    if (number === null || number === undefined) {
        return '0';
    }

    // Parse as float and ensure 2 decimal places
    const value = parseFloat(number);
    return value.toLocaleString('en-US', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 2
    });
}