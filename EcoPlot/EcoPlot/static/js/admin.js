// Admin Panel JavaScript

class AdminPanel {
    constructor() {
        this.devices = [];
        this.deviceTypes = new Map();
        this.deviceBrands = new Map();
        this.currentFilter = {
            type: '',
            user: '',
            brand: ''
        };
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadInitialData();
    }

    bindEvents() {
        // Make sure DOM is ready before binding events
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setupEventBindings());
        } else {
            this.setupEventBindings();
        }
    }

    setupEventBindings() {
        console.log('Setting up event bindings...');

        // Filter events
        const typeFilter = document.getElementById('deviceTypeFilter');
        const userFilter = document.getElementById('userFilter');
        const brandFilter = document.getElementById('brandFilter');

        console.log('Filter elements found:', {
            typeFilter: !!typeFilter,
            userFilter: !!userFilter,
            brandFilter: !!brandFilter
        });

        if (typeFilter) {
            typeFilter.addEventListener('change', (e) => {
                console.log('Type filter changed to:', e.target.value);
                this.currentFilter.type = e.target.value;
                this.filterDevices();
            });
        }

        if (userFilter) {
            userFilter.addEventListener('change', (e) => {
                console.log('User filter changed to:', e.target.value);
                this.currentFilter.user = e.target.value;
                this.filterDevices();
            });
        }

        if (brandFilter) {
            brandFilter.addEventListener('change', (e) => {
                console.log('Brand filter changed to:', e.target.value);
                this.currentFilter.brand = e.target.value;
                this.filterDevices();
            });
        }

        // Add event delegation for dynamic content
        document.body.addEventListener('click', (e) => {
            if (e.target.matches('.collapsible-header') || e.target.closest('.collapsible-header')) {
                this.toggleCollapsible(e.target.closest('.collapsible-header'));
            }
        });
    }

    async loadInitialData() {
        this.showLoading();
        try {
            await Promise.all([
                this.loadDeviceTypes(),
                this.loadAllBrands(), // Load all brands from all device types
                this.loadDevices(),
                this.loadUsers()
            ]);
            console.log('All data loaded:');
            console.log('Device types:', this.deviceTypes);
            console.log('Device brands:', this.deviceBrands);
            console.log('Devices:', this.devices);

            this.updateStats();
            this.renderDevices();
            this.populateFilters();
        } catch (error) {
            console.error('Error loading initial data:', error);
            this.showError('Failed to load admin data');
        } finally {
            this.hideLoading();
        }
    }

    async loadDeviceTypes() {
        try {
            const response = await fetch('/devices/api/categories');
            const data = await response.json();
            if (data.success) {
                data.device_types.forEach(type => {
                    this.deviceTypes.set(type.id, type);
                });
            }
        } catch (error) {
            console.error('Error loading device types:', error);
        }
    }

    extractDeviceTypes() {
        this.devices.forEach(device => {
            if (device.device_type) {
                this.deviceTypes.set(device.device_type.id, device.device_type);
            }
        });
    }

    async loadAllBrands() {
        try {
            // Get all device types first
            if (this.deviceTypes.size === 0) {
                await this.loadDeviceTypes();
            }

            // Load brands for each device type
            for (const [typeId, deviceType] of this.deviceTypes) {
                const response = await fetch(`/devices/api/brands/${typeId}`);
                const data = await response.json();

                if (data.success) {
                    data.brands.forEach(brand => {
                        this.deviceBrands.set(brand.id, brand);
                    });
                }
            }
            console.log('Loaded all brands:', this.deviceBrands.size);
        } catch (error) {
            console.error('Error loading all brands:', error);
        }
    }

    extractDeviceBrands() {
        // Add any brands that are in use but not already in our Map
        this.devices.forEach(device => {
            if (device.brand) {
                this.deviceBrands.set(device.brand.id, device.brand);
            }
        });
    }

    async loadDevices() {
        try {
            const response = await fetch('/admin/api/devices');
            if (!response.ok) throw new Error('Failed to fetch devices');

            const data = await response.json();
            if (data.success) {
                this.devices = data.devices;

                // Extract device types and brands from the loaded devices
                this.extractDeviceTypes();
                this.extractDeviceBrands();
            }
        } catch (error) {
            console.error('Error loading devices:', error);
            this.showError('Failed to load devices');
        }
    }

    // Remove the async loadBrandsForDevices() function since we're not using it anymore
    // The data is loaded directly from the API with the devices

    async loadUsers() {
        try {
            const response = await fetch('/admin/api/users');
            if (!response.ok) throw new Error('Failed to fetch users');

            const data = await response.json();
            if (data.success) {
                this.renderUsers(data.users);
            }
        } catch (error) {
            console.error('Error loading users:', error);
            this.showError('Failed to load users');
        }
    }

    renderUsers(users) {
        const userList = document.getElementById('userList');
        if (!userList) return;

        let html = '';
        users.forEach(user => {
            html += `
                <tr data-user-id="${user.id}">
                    <td>${user.username}</td>
                    <td>${user.email}</td>
                    <td>${user.device_count}</td>
                    <td>
                        <button class="admin-btn admin-btn-primary btn-sm" onclick="adminPanel.viewUser(${user.id})">
                            <i class="bi bi-eye"></i> View Devices
                        </button>
                    </td>
                </tr>
            `;
        });

        userList.innerHTML = html;
    }

    viewUser(userId) {
        // TODO: Implement user detail view
        window.location.href = `/admin/user/${userId}`;
    }

    updateStats() {
        const deviceCount = document.getElementById('deviceCount');
        const energyConsumption = document.getElementById('totalEnergyConsumption');
        const activeDevices = document.getElementById('activeDevices');

        if (deviceCount) {
            deviceCount.textContent = this.devices.length;
        }

        if (energyConsumption) {
            const totalPower = this.devices.reduce((sum, device) => {
                return sum + (device.power_consumption_watts || 0);
            }, 0);
            energyConsumption.textContent = `${(totalPower / 1000).toFixed(2)} kW`;
        }

        if (activeDevices) {
            const smartDevices = this.devices.filter(d => d.is_smart_device).length;
            activeDevices.textContent = smartDevices;
        }
    }

    renderDevices() {
        const deviceList = document.getElementById('deviceList');
        if (!deviceList) return;

        let html = '';

        this.devices.forEach(device => {
            // Use the preloaded data from the API response
            const deviceType = device.device_type || this.deviceTypes.get(device.device_type_id);
            const deviceBrand = device.brand || this.deviceBrands.get(device.brand_id);

            html += this.getDeviceRowHTML(device, deviceType, deviceBrand);
        });

        deviceList.innerHTML = html;
    }

    getDeviceRowHTML(device, deviceType, deviceBrand) {
        const badges = this.getDeviceBadges(device);
        const powerBar = this.getPowerBar(device);

        return `
            <tr class="expandable-row" onclick="adminPanel.toggleDeviceDetails(${device.id})">
                <td>${device.name}</td>
                <td>
                    ${deviceType?.icon_path ? `<img src="${deviceType.icon_path}" class="device-type-icon" alt="${deviceType.name}">` : ''}
                    ${deviceType?.name || 'N/A'}
                </td>
                <td>
                    ${deviceBrand?.logo_path ? `<img src="${deviceBrand.logo_path}" class="brand-logo" alt="${deviceBrand.name}">` : ''}
                    ${deviceBrand?.name || 'N/A'}
                </td>
                <td>${device.model || 'N/A'}</td>
                <td>
                    ${device.power_consumption_watts}W
                    ${powerBar}
                </td>
                <td>${badges}</td>
                <td>
                    ${device.created_at ? new Date(device.created_at).toLocaleDateString() : 'N/A'}
                    <br>
                    <small class="text-muted">User: ${device.user?.username || 'N/A'}</small>
                </td>
            </tr>
            <tr class="expandable-details" id="details-${device.id}">
                <td colspan="7">
                    ${this.getDeviceDetailsHTML(device)}
                </td>
            </tr>
        `;
    }

    getDeviceBadges(device) {
        let badges = '';

        if (device.is_schedulable) {
            badges += `<span class="device-badge schedulable">Schedulable</span>`;
        }
        if (device.is_ev_charger) {
            badges += `<span class="device-badge ev-charger">EV Charger</span>`;
        }
        if (device.is_smart_device) {
            badges += `<span class="device-badge smart">Smart Device</span>`;
        }

        return badges || '<span class="text-muted">—</span>';
    }

    getPowerBar(device) {
        const maxPower = 2000; // Watts
        const percentage = Math.min((device.power_consumption_watts / maxPower) * 100, 100);

        return `
            <div class="power-bar">
                <div class="power-fill" style="width: ${percentage}%"></div>
            </div>
        `;
    }

    getDeviceDetailsHTML(device) {
        const details = {
            'Device Type': device.device_type?.name || this.deviceTypes.get(device.device_type_id)?.name || 'N/A',
            'Brand': device.brand?.name || this.deviceBrands.get(device.brand_id)?.name || 'N/A',
            'Model': device.model || 'N/A',
            'Owner': device.user?.username || 'Unknown',
            'Power Consumption': `${device.power_consumption_watts} watts`,
            'Standby Power': `${device.standby_power_watts || 0} watts`,
            'Usage Hours/Day': device.average_usage_hours_per_day ? `${device.average_usage_hours_per_day} hours` : 'N/A',
            'Usage Flexibility': device.usage_flexibility ? `${device.usage_flexibility}/10` : 'N/A',
            'Priority Level': device.priority_level ? `${device.priority_level}/10` : 'N/A'
        };

        if (device.is_schedulable) {
            details['Preferred Start Time'] = device.preferred_start_time || 'N/A';
            details['Preferred End Time'] = device.preferred_end_time || 'N/A';
            details['Operation Duration'] = device.operation_duration_minutes ? `${device.operation_duration_minutes} minutes` : 'N/A';
        }

        if (device.is_ev_charger) {
            details['EV Battery Capacity'] = device.ev_battery_capacity_kwh ? `${device.ev_battery_capacity_kwh} kWh` : 'N/A';
            details['Charging Rate'] = device.charging_rate_kw ? `${device.charging_rate_kw} kW` : 'N/A';
        }

        let detailsHTML = '<div class="device-details">';
        Object.entries(details).forEach(([key, value]) => {
            detailsHTML += `
                <div class="detail-row">
                    <span class="detail-label">${key}:</span>
                    <span class="detail-value">${value}</span>
                </div>
            `;
        });
        detailsHTML += '</div>';

        return detailsHTML;
    }

    toggleDeviceDetails(deviceId) {
        const details = document.getElementById(`details-${deviceId}`);
        if (details) {
            details.classList.toggle('show');
        }
    }

    populateFilters() {
        this.populateTypeFilter();
        this.populateBrandFilter();
        this.populateUserFilter();
    }

    populateUserFilter() {
        const userFilter = document.getElementById('userFilter');
        if (!userFilter) return;

        // Get unique users from devices
        const uniqueUsers = new Map();
        this.devices.forEach(device => {
            if (device.user) {
                uniqueUsers.set(device.user.id, device.user);
            }
        });

        let html = '<option value="">All Users</option>';
        uniqueUsers.forEach(user => {
            html += `<option value="${user.id}">${user.username}</option>`;
        });
        userFilter.innerHTML = html;
    }

    populateTypeFilter() {
        const typeFilter = document.getElementById('deviceTypeFilter');
        if (!typeFilter) return;

        let html = '<option value="">All Types</option>';
        this.deviceTypes.forEach(type => {
            html += `<option value="${type.id}">${type.name}</option>`;
        });
        typeFilter.innerHTML = html;
    }

    populateBrandFilter() {
        const brandFilter = document.getElementById('brandFilter');
        if (!brandFilter) return;

        let html = '<option value="">All Brands</option>';
        const uniqueBrands = new Map();

        this.deviceBrands.forEach(brand => {
            uniqueBrands.set(brand.id, brand);
        });

        uniqueBrands.forEach(brand => {
            html += `<option value="${brand.id}">${brand.name}</option>`;
        });
        brandFilter.innerHTML = html;
    }

    filterDevices() {
        console.group('=== FILTERING DEVICES ===');
        console.log('Current filters:', JSON.stringify(this.currentFilter, null, 2));
        console.log('Total devices:', this.devices.length);

        const filteredDevices = this.devices.filter(device => {
            // Get the proper type ID either from nested object or direct field
            const deviceTypeId = device.device_type?.id || device.device_type_id;
            const deviceBrandId = device.brand?.id || device.brand_id;
            const deviceUserId = device.user?.id || device.user_id;

            console.log(`Device "${device.name}":`, {
                deviceTypeId,
                deviceBrandId,
                deviceUserId,
                filterType: this.currentFilter.type,
                filterBrand: this.currentFilter.brand,
                filterUser: this.currentFilter.user
            });

            const typeMatch = !this.currentFilter.type || String(deviceTypeId) === String(this.currentFilter.type);
            const brandMatch = !this.currentFilter.brand || String(deviceBrandId) === String(this.currentFilter.brand);
            const userMatch = !this.currentFilter.user || String(deviceUserId) === String(this.currentFilter.user);

            console.log(`Matches: type=${typeMatch}, brand=${brandMatch}, user=${userMatch}`);

            return typeMatch && brandMatch && userMatch;
        });

        console.log('Filtered devices:', filteredDevices.length);
        console.groupEnd();

        const deviceList = document.getElementById('deviceList');
        const emptyState = document.getElementById('emptyState');

        if (!deviceList) {
            console.error('deviceList element not found');
            return;
        }

        if (filteredDevices.length === 0) {
            if (emptyState) {
                emptyState.style.display = 'block';
            }
            deviceList.innerHTML = '';
            return;
        } else {
            if (emptyState) {
                emptyState.style.display = 'none';
            }
        }

        let html = '';
        filteredDevices.forEach(device => {
            const deviceType = device.device_type || this.deviceTypes.get(device.device_type_id);
            const deviceBrand = device.brand || this.deviceBrands.get(device.brand_id);
            html += this.getDeviceRowHTML(device, deviceType, deviceBrand);
        });

        deviceList.innerHTML = html;
    }

    toggleCollapsible(header) {
        header.classList.toggle('active');
        const content = header.nextElementSibling;
        if (content && content.classList.contains('collapsible-content')) {
            content.classList.toggle('show');
        }
    }

    showLoading() {
        const overlay = document.createElement('div');
        overlay.className = 'loading-overlay';
        overlay.innerHTML = '<div class="loading-spinner"></div>';
        document.body.appendChild(overlay);
    }

    hideLoading() {
        const overlay = document.querySelector('.loading-overlay');
        if (overlay) {
            overlay.remove();
        }
    }

    showError(message) {
        const alert = document.createElement('div');
        alert.className = 'admin-alert admin-alert-danger';
        alert.innerHTML = `
            <i class="bi bi-exclamation-triangle-fill"></i>
            ${message}
        `;
        document.querySelector('.admin-container').prepend(alert);

        setTimeout(() => {
            alert.remove();
        }, 5000);
    }

    showSuccess(message) {
        const alert = document.createElement('div');
        alert.className = 'admin-alert admin-alert-success';
        alert.innerHTML = `
            <i class="bi bi-check-circle-fill"></i>
            ${message}
        `;
        document.querySelector('.admin-container').prepend(alert);

        setTimeout(() => {
            alert.remove();
        }, 3000);
    }
}

// Initialize admin panel
let adminPanel;

// Initialize immediately when the script loads
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        console.log('DOM loaded, initializing admin panel...');
        adminPanel = new AdminPanel();
        window.adminPanel = adminPanel; // Make it globally accessible
    });
} else {
    console.log('DOM already loaded, initializing admin panel...');
    adminPanel = new AdminPanel();
    window.adminPanel = adminPanel; // Make it globally accessible
}

// Export for global use
window.AdminPanel = AdminPanel;