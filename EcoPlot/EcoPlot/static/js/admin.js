// EcoPlot Admin Panel JavaScript

// Global variables
let deviceTypes = [];
let brands = [];
let predefinedDevices = [];
let userDevices = [];
let users = [];

// Navigation
function showSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });

    // Remove active class from all nav links
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.classList.remove('active');
    });

    // Show selected section
    const selectedSection = document.getElementById(sectionId);
    if (selectedSection) {
        selectedSection.classList.add('active');
        // Add active class to corresponding nav link
        document.querySelector(`a[href="#${sectionId}"]`).classList.add('active');
    }

    // Load data for the section
    loadSectionData(sectionId);
}

// Data loading functions
async function loadSectionData(sectionId) {
    showLoading(true);
    try {
        switch (sectionId) {
            case 'dashboard':
                await getStats();
                break;
            case 'device-types':
                await loadDeviceTypes();
                break;
            case 'brands':
                await loadBrands();
                break;
            case 'devices':
                await loadPredefinedDevices();
                await loadUserDevices();
                break;
            case 'users':
                await loadUsers();
                break;
        }
    } catch (error) {
        console.error('Error loading section data:', error);
        showStatus(`Error loading section ${sectionId}: ${error.message}`, true);
    } finally {
        showLoading(false);
    }
}

// Loading indicator
function showLoading(show = true) {
    document.getElementById('loading').style.display = show ? 'block' : 'none';
}

// Status message
function showStatus(message, isError = false) {
    const statusMessage = document.getElementById('statusMessage');
    statusMessage.textContent = message;
    statusMessage.className = `status-message ${isError ? 'error' : ''}`;
    statusMessage.style.display = 'block';

    setTimeout(() => {
        statusMessage.style.display = 'none';
    }, 3000);
}

// Database Management
async function initializeDatabase() {
    if (!confirm('This will initialize the database. Continue?')) return;

    try {
        showLoading(true);
        const response = await fetch('/admin/init-db', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const result = await response.json();
        if (result.success) {
            showStatus('Database initialized successfully');
            await getStats();
        } else {
            showStatus(result.message || 'Error initializing database', true);
        }
    } catch (error) {
        showStatus('Error initializing database', true);
    } finally {
        showLoading(false);
    }
}

async function seedDevices() {
    if (!confirm('This will seed device data. Continue?')) return;

    try {
        showLoading(true);
        const response = await fetch('/admin/seed-devices', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const result = await response.json();
        if (result.success) {
            showStatus('Device data seeded successfully');
            await getStats();
        } else {
            showStatus(result.message || 'Error seeding devices', true);
        }
    } catch (error) {
        showStatus('Error seeding devices', true);
    } finally {
        showLoading(false);
    }
}

async function clearDevices() {
    if (!confirm('This will clear all device data. Continue?')) return;

    try {
        showLoading(true);
        const response = await fetch('/admin/clear-devices', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const result = await response.json();
        if (result.success) {
            showStatus('Device data cleared successfully');
            await getStats();
        } else {
            showStatus(result.message || 'Error clearing devices', true);
        }
    } catch (error) {
        showStatus('Error clearing devices', true);
    } finally {
        showLoading(false);
    }
}

async function resetDatabase() {
    if (!confirm('This will reset the entire database. This action cannot be undone. Continue?')) return;

    try {
        showLoading(true);
        const response = await fetch('/admin/reset-db', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const result = await response.json();
        if (result.success) {
            showStatus('Database reset successfully');
            await getStats();
        } else {
            showStatus(result.message || 'Error resetting database', true);
        }
    } catch (error) {
        showStatus('Error resetting database', true);
    } finally {
        showLoading(false);
    }
}

// Statistics
async function getStats() {
    try {
        const response = await fetch('/admin/stats');
        const data = await response.json();

        if (data.success && data.stats) {
            const statsContainer = document.getElementById('statsContainer');
            statsContainer.innerHTML = `
                <div class="stat-card">
                    <h3>Users</h3>
                    <p>${data.stats.users || 0}</p>
                </div>
                <div class="stat-card">
                    <h3>Device Types</h3>
                    <p>${data.stats.device_types || 0}</p>
                </div>
                <div class="stat-card">
                    <h3>Brands</h3>
                    <p>${data.stats.brands || 0}</p>
                </div>
                <div class="stat-card">
                    <h3>Predefined Devices</h3>
                    <p>${data.stats.predefined_devices || 0}</p>
                </div>
                <div class="stat-card">
                    <h3>User Devices</h3>
                    <p>${data.stats.user_devices || 0}</p>
                </div>
            `;
        } else {
            throw new Error('Invalid response format');
        }
    } catch (error) {
        console.error('Error loading statistics:', error);
        showStatus('Error loading statistics', true);
    }
}

// Test Data Creation
async function createTestUsers() {
    try {
        showLoading(true);
        const response = await fetch('/admin/create-test-users', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const result = await response.json();
        if (result.success) {
            showStatus('Test users created successfully');
            await getStats();
        } else {
            showStatus(result.message || 'Error creating test users', true);
        }
    } catch (error) {
        showStatus('Error creating test users', true);
    } finally {
        showLoading(false);
    }
}

async function createTestDevices() {
    try {
        showLoading(true);
        const response = await fetch('/admin/create-test-devices', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const result = await response.json();
        if (result.success) {
            showStatus('Test devices created successfully');
            await getStats();
        } else {
            showStatus(result.message || 'Error creating test devices', true);
        }
    } catch (error) {
        showStatus('Error creating test devices', true);
    } finally {
        showLoading(false);
    }
}

// Export data
async function exportData() {
    try {
        showLoading(true);
        const response = await fetch('/admin/export-data');

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `ecoplot-export-${new Date().toISOString().split('T')[0]}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
            showStatus('Data exported successfully');
        } else {
            const result = await response.json();
            showStatus(result.message || 'Error exporting data', true);
        }
    } catch (error) {
        showStatus('Error exporting data', true);
    } finally {
        showLoading(false);
    }
}