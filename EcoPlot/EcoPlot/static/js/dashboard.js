// EcoPlot/static/js/dashboard.js

document.addEventListener('DOMContentLoaded', function () {
    // Initialize all charts and load data
    initializeDashboard();

    // Add event listeners for time period toggles
    document.getElementById('day-view').addEventListener('click', function () {
        updateTimePeriod('day');
    });

    document.getElementById('week-view').addEventListener('click', function () {
        updateTimePeriod('week');
    });

    document.getElementById('month-view').addEventListener('click', function () {
        updateTimePeriod('month');
    });
});

// Global variables for charts
let energyUsageChart;
let deviceConsumptionChart;
let energyTimelineChart;
let currentPeriod = 'day'; // Default time period

function initializeDashboard() {
    // Load summary data
    loadSummaryData();

    // Initialize charts
    initializeEnergyUsageChart();
    initializeDeviceConsumptionChart();
    initializeEnergyTimelineChart();

    // Load devices and recommendations
    loadTopDevices();
    loadLatestRecommendations();
}

// Update all data based on selected time period
function updateTimePeriod(period) {
    // Update active button state
    document.querySelectorAll('.btn-group .btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.getElementById(period + '-view').classList.add('active');

    currentPeriod = period;

    // Reload all data with new time period
    loadSummaryData();
    updateCharts();
}

// Initialize Energy Usage Chart (Consumption vs Production)
function initializeEnergyUsageChart() {
    const ctx = document.getElementById('energyUsageChart').getContext('2d');

    energyUsageChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: generateTimeLabels(currentPeriod),
            datasets: [
                {
                    label: 'Energy Consumed (kWh)',
                    data: [],
                    backgroundColor: 'rgba(220, 53, 69, 0.7)',
                    borderColor: 'rgba(220, 53, 69, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Energy Produced (kWh)',
                    data: [],
                    backgroundColor: 'rgba(40, 167, 69, 0.7)',
                    borderColor: 'rgba(40, 167, 69, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Energy (kWh)'
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Energy Consumption vs. Production'
                }
            }
        }
    });

    // Load initial data
    loadEnergyUsageData();
}

// Initialize Device Consumption Chart (Pie chart of device energy usage)
function initializeDeviceConsumptionChart() {
    const ctx = document.getElementById('deviceConsumptionChart').getContext('2d');

    deviceConsumptionChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: [],
            datasets: [{
                data: [],
                backgroundColor: [
                    'rgba(40, 167, 69, 0.7)',
                    'rgba(0, 123, 255, 0.7)',
                    'rgba(255, 193, 7, 0.7)',
                    'rgba(23, 162, 184, 0.7)',
                    'rgba(111, 66, 193, 0.7)',
                    'rgba(220, 53, 69, 0.7)',
                    'rgba(253, 126, 20, 0.7)',
                    'rgba(102, 16, 242, 0.7)'
                ],
                borderColor: [
                    'rgba(40, 167, 69, 1)',
                    'rgba(0, 123, 255, 1)',
                    'rgba(255, 193, 7, 1)',
                    'rgba(23, 162, 184, 1)',
                    'rgba(111, 66, 193, 1)',
                    'rgba(220, 53, 69, 1)',
                    'rgba(253, 126, 20, 1)',
                    'rgba(102, 16, 242, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right'
                },
                title: {
                    display: true,
                    text: 'Device Energy Consumption'
                }
            }
        }
    });

    // Load initial data
    loadDeviceConsumptionData();
}

// Initialize Energy Timeline Chart (Line chart showing energy usage over time)
function initializeEnergyTimelineChart() {
    const ctx = document.getElementById('energyTimelineChart').getContext('2d');

    energyTimelineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: generateTimeLabels(currentPeriod),
            datasets: [{
                label: 'Grid Energy (kWh)',
                data: [],
                borderColor: 'rgba(220, 53, 69, 1)',
                backgroundColor: 'rgba(220, 53, 69, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.2
            }, {
                label: 'Solar Energy (kWh)',
                data: [],
                borderColor: 'rgba(40, 167, 69, 1)',
                backgroundColor: 'rgba(40, 167, 69, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.2
            }, {
                label: 'Battery Usage (kWh)',
                data: [],
                borderColor: 'rgba(0, 123, 255, 1)',
                backgroundColor: 'rgba(0, 123, 255, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Energy (kWh)'
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Energy Sources Timeline'
                }
            }
        }
    });

    // Load initial data
    loadEnergyTimelineData();
}

// Update all charts with new data
function updateCharts() {
    loadEnergyUsageData();
    loadDeviceConsumptionData();
    loadEnergyTimelineData();
}

// Generate time labels based on selected period
function generateTimeLabels(period) {
    let labels = [];

    switch (period) {
        case 'day':
            // Hours of the day
            for (let i = 0; i < 24; i++) {
                labels.push(i + ':00');
            }
            break;
        case 'week':
            // Days of the week
            labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
            break;
        case 'month':
            // Days of the month (simplified to 30 days)
            for (let i = 1; i <= 30; i++) {
                labels.push('Day ' + i);
            }
            break;
    }

    return labels;
}

// Load summary metrics data
function loadSummaryData() {
    // Fetch summary data from API
    fetch(`/api/dashboard/summary?period=${currentPeriod}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const summary = data.summary;

                // Update summary cards
                document.getElementById('energy-used').textContent = `${summary.energy_used.toFixed(1)} kWh`;
                document.getElementById('energy-used-change').innerHTML =
                    `<i class="fas fa-arrow-${summary.energy_used_change < 0 ? 'down' : 'up'}"></i> ${Math.abs(summary.energy_used_change).toFixed(1)}%`;

                document.getElementById('solar-generated').textContent = `${summary.energy_produced.toFixed(1)} kWh`;
                document.getElementById('solar-generated-change').innerHTML =
                    `<i class="fas fa-arrow-${summary.energy_produced_change < 0 ? 'down' : 'up'}"></i> ${Math.abs(summary.energy_produced_change).toFixed(1)}%`;

                document.getElementById('carbon-saved').textContent = `${summary.carbon_saved.toFixed(1)} kg`;
                document.getElementById('carbon-saved-change').innerHTML =
                    `<i class="fas fa-arrow-${summary.carbon_saved_change < 0 ? 'down' : 'up'}"></i> ${Math.abs(summary.carbon_saved_change).toFixed(1)}%`;

                document.getElementById('cost-savings').textContent = `$${summary.cost_savings.toFixed(2)}`;
                document.getElementById('cost-savings-change').innerHTML =
                    `<i class="fas fa-arrow-${summary.cost_savings_change < 0 ? 'down' : 'up'}"></i> ${Math.abs(summary.cost_savings_change).toFixed(1)}%`;
            }
        })
        .catch(error => {
            console.error('Error loading summary data:', error);
            // Fallback to generated data if API fails
            // ... (keep your existing fallback code)
        });
}

// Load Energy Usage Chart data
function loadEnergyUsageData() {
    // Fetch energy usage data from API
    fetch(`/api/dashboard/energy-usage?period=${currentPeriod}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update chart with API data
                energyUsageChart.data.labels = data.labels;
                energyUsageChart.data.datasets[0].data = data.consumption;
                energyUsageChart.data.datasets[1].data = data.production;
                energyUsageChart.update();
            }
        })
        .catch(error => {
            console.error('Error loading energy usage data:', error);
            // Fallback to generated data if API fails
            // ... (keep your existing fallback code)
        });
}

// Load Device Consumption Chart data
function loadDeviceConsumptionData() {
    // Fetch device consumption data
    fetch('/api/dashboard/devices')
        .then(response => response.json())
        .then(data => {
            if (data.success && data.devices.length > 0) {
                // Process devices to get data for chart
                const labels = [];
                const chartData = [];

                // Group devices by type and calculate total consumption
                const devicesByType = {};

                data.devices.forEach(device => {
                    const typeName = device.type;
                    if (!devicesByType[typeName]) {
                        devicesByType[typeName] = 0;
                    }
                    devicesByType[typeName] += device.daily_usage_kwh || 0;
                });

                // Convert to arrays for chart
                for (const [type, usage] of Object.entries(devicesByType)) {
                    labels.push(type);
                    chartData.push(parseFloat(usage.toFixed(2)));
                }

                // Update chart
                deviceConsumptionChart.data.labels = labels;
                deviceConsumptionChart.data.datasets[0].data = chartData;
                deviceConsumptionChart.update();
            }
        })
        .catch(error => {
            console.error('Error loading device consumption data:', error);
            // Fallback to generated data if API fails
            // ... (keep your existing fallback code)
        });
}

// Load Energy Timeline Chart data
function loadEnergyTimelineData() {
    // Fetch energy timeline data from API
    fetch(`/api/dashboard/energy-usage?period=${currentPeriod}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update chart with API data
                energyTimelineChart.data.labels = data.labels;
                energyTimelineChart.data.datasets[0].data = data.consumption;
                energyTimelineChart.data.datasets[1].data = data.production;
                // You might need to calculate battery usage or adjust based on your API
                energyTimelineChart.data.datasets[2].data = data.production.map((val, idx) =>
                    Math.max(0, (data.consumption[idx] - val) * 0.5));
                energyTimelineChart.update();
            }
        })
        .catch(error => {
            console.error('Error loading energy timeline:', error);
            // Generate fallback data
            let gridData = [];
            let solarData = [];
            let batteryData = [];
            const timeLabels = generateTimeLabels(currentPeriod);

            // Generate data based on period
            for (let i = 0; i < timeLabels.length; i++) {
                // Generate realistic patterns based on time of day/week
                let timeIdx = i;

                if (currentPeriod === 'day') {
                    // During the day, solar is higher during midday, grid lower
                    let daytime = i >= 6 && i <= 18;
                    let peakSolar = i >= 10 && i <= 15;

                    let solar = daytime ? (peakSolar ? 0.8 + Math.random() * 0.4 : 0.3 + Math.random() * 0.3) : 0;
                    let grid = daytime ? (0.3 + Math.random() * 0.4) : (0.5 + Math.random() * 0.5);
                    let battery = daytime ? (0.1 + Math.random() * 0.2) : (0.3 + Math.random() * 0.2);

                    // Evening peak
                    if (i >= 18 && i <= 22) {
                        grid = 0.9 + Math.random() * 0.4;
                        battery = 0.4 + Math.random() * 0.3;
                    }

                    gridData.push(grid);
                    solarData.push(solar);
                    batteryData.push(battery);
                } else if (currentPeriod === 'week') {
                    // Weekly patterns - weekends different from weekdays
                    let weekday = i < 5;

                    let solar = 4 + Math.random() * 3;
                    let grid = weekday ? (6 + Math.random() * 2) : (8 + Math.random() * 3);
                    let battery = weekday ? (2 + Math.random() * 1) : (1 + Math.random() * 2);

                    gridData.push(grid);
                    solarData.push(solar);
                    batteryData.push(battery);
                } else {
                    // Monthly patterns
                    let solar = 4 + Math.random() * 3;
                    // Weekend effect
                    let weekend = i % 7 === 5 || i % 7 === 6;
                    let grid = weekend ? (8 + Math.random() * 3) : (6 + Math.random() * 2);
                    let battery = weekend ? (1 + Math.random() * 2) : (2 + Math.random() * 1);

                    // Weather pattern simulation (cloudy days affect solar)
                    if (i % 5 === 0) { // Simulated cloudy day
                        solar = solar * 0.6;
                        grid = grid * 1.2;
                    }

                    gridData.push(grid);
                    solarData.push(solar);
                    batteryData.push(battery);
                }
            }

            // Update chart with generated data
            energyTimelineChart.data.labels = timeLabels;
            energyTimelineChart.data.datasets[0].data = gridData;
            energyTimelineChart.data.datasets[1].data = solarData;
            energyTimelineChart.data.datasets[2].data = batteryData;
            energyTimelineChart.update();
        });
}

// Load top energy consuming devices
function loadTopDevices() {
    // Fetch user's devices from API
    fetch('/api/dashboard/devices')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const devicesList = document.getElementById('topDevicesList');
                devicesList.innerHTML = '';

                // Display top 5 devices by power consumption
                const topDevices = data.devices.slice(0, 5);

                if (topDevices.length === 0) {
                    devicesList.innerHTML = `
                        <div class="text-center py-3">
                            <p>No devices found. Add devices to see their energy consumption.</p>
                        </div>
                    `;
                    return;
                }

                topDevices.forEach(device => {
                    const deviceItem = document.createElement('div');
                    deviceItem.className = 'device-item';
                    deviceItem.innerHTML = `
                        <div class="device-info">
                            <h6>${device.name}</h6>
                            <p class="text-muted">${device.brand} ${device.type}</p>
                        </div>
                        <div class="device-usage">
                            <div class="device-power">${device.power_watts}W</div>
                            <div class="device-daily">${device.daily_usage_kwh.toFixed(2)} kWh/day</div>
                        </div>
                    `;
                    devicesList.appendChild(deviceItem);
                });
            }
        })
        .catch(error => {
            console.error('Error loading devices:', error);
            document.getElementById('topDevicesList').innerHTML = `
                <div class="alert alert-danger">
                    Failed to load device data
                </div>
            `;
        });
}

// Load latest recommendations
function loadLatestRecommendations() {
    // Fetch recommendations from API
    fetch('/api/dashboard/recommendations')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const recommendationsList = document.getElementById('recommendationsList');
                recommendationsList.innerHTML = '';

                const recommendations = data.recommendations;

                if (recommendations.length === 0) {
                    recommendationsList.innerHTML = `
                        <div class="text-center py-3">
                            <p>No recommendations available yet.</p>
                        </div>
                    `;
                    return;
                }

                recommendations.forEach(rec => {
                    const recItem = document.createElement('div');
                    recItem.className = 'recommendation-item';
                    recItem.innerHTML = `
                        <div class="recommendation-content">
                            <p>${rec.content}</p>
                        </div>
                        <div class="recommendation-saving">
                            <span class="badge bg-success">${rec.saving}</span>
                        </div>
                    `;
                    recommendationsList.appendChild(recItem);
                });
            }
        })
        .catch(error => {
            console.error('Error loading recommendations:', error);
            document.getElementById('recommendationsList').innerHTML = `
                <div class="alert alert-danger">
                    Failed to load recommendations
                </div>
            `;
        });
}