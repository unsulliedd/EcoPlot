// EcoPlot/static/js/device.js

const DeviceManager = {
    showAddModal: function (deviceTypeId, brandId) {
        const modal = new bootstrap.Modal(document.getElementById('addDeviceModal'));

        // Set hidden fields with the selected device type and brand
        document.getElementById('device_type_id').value = deviceTypeId;
        document.getElementById('brand_id').value = brandId;

        // Reset form
        document.getElementById('addDeviceForm').reset();

        // Hide optional sections
        document.getElementById('schedulingFields').style.display = 'none';
        document.getElementById('evFields').style.display = 'none';

        modal.show();
    },

    editDevice: async function (deviceId) {
        try {
            // Fetch device data
            const response = await fetch(`/devices/api/${deviceId}`);
            const result = await response.json();

            if (result.success) {
                const device = result.device;

                // Show modal
                const modal = new bootstrap.Modal(document.getElementById('editDeviceModal'));
                modal.show();

                // Fill form with device data
                document.getElementById('edit_device_id').value = device.id;
                document.getElementById('edit_name').value = device.name || '';
                document.getElementById('edit_model').value = device.model || '';
                document.getElementById('edit_power_consumption_watts').value = device.power_consumption_watts || '';
                document.getElementById('edit_standby_power_watts').value = device.standby_power_watts || '';
                document.getElementById('edit_average_usage_hours_per_day').value = device.average_usage_hours_per_day || '';
                document.getElementById('edit_usage_flexibility').value = device.usage_flexibility || '';
                document.getElementById('edit_priority_level').value = device.priority_level || '';

                // Set checkboxes
                document.getElementById('edit_is_schedulable').checked = device.is_schedulable || false;
                document.getElementById('edit_is_ev_charger').checked = device.is_ev_charger || false;
                document.getElementById('edit_is_smart_device').checked = device.is_smart_device || false;
                document.getElementById('edit_api_controllable').checked = device.api_controllable || false;

                // Show/hide conditional fields
                toggleEditSchedulingFields(document.getElementById('edit_is_schedulable'));
                toggleEditEVFields(document.getElementById('edit_is_ev_charger'));

                // Fill conditional fields if applicable
                if (device.is_schedulable) {
                    document.getElementById('edit_preferred_start_time').value = device.preferred_start_time || '';
                    document.getElementById('edit_preferred_end_time').value = device.preferred_end_time || '';
                    document.getElementById('edit_operation_duration_minutes').value = device.operation_duration_minutes || '';
                }

                if (device.is_ev_charger) {
                    document.getElementById('edit_ev_battery_capacity_kwh').value = device.ev_battery_capacity_kwh || '';
                    document.getElementById('edit_charging_rate_kw').value = device.charging_rate_kw || '';
                }
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error loading device data');
        }
    },

    addDevice: async function () {
        const form = document.getElementById('addDeviceForm');
        const formData = new FormData(form);
        const deviceData = {};

        // Handle checkboxes
        for (let [key, value] of formData.entries()) {
            deviceData[key] = value;
        }

        // Ensure checkboxes are included even if unchecked
        deviceData.is_schedulable = form.elements.is_schedulable.checked;
        deviceData.is_ev_charger = form.elements.is_ev_charger.checked;
        deviceData.is_smart_device = form.elements.is_smart_device.checked;
        deviceData.api_controllable = form.elements.api_controllable.checked;

        try {
            const response = await fetch('/devices/api/add', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(deviceData)
            });

            const result = await response.json();

            if (result.success) {
                alert('Device added successfully!');
                window.location.reload();
            } else {
                alert('Error: ' + result.message);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error adding device');
        }
    },

    updateDevice: async function () {
        const form = document.getElementById('editDeviceForm');
        const deviceId = document.getElementById('edit_device_id').value;
        const formData = new FormData(form);
        const deviceData = {};

        // Handle checkboxes
        for (let [key, value] of formData.entries()) {
            if (key !== 'device_id') {
                deviceData[key] = value;
            }
        }

        // Ensure checkboxes are included even if unchecked
        deviceData.is_schedulable = form.elements.is_schedulable.checked;
        deviceData.is_ev_charger = form.elements.is_ev_charger.checked;
        deviceData.is_smart_device = form.elements.is_smart_device.checked;
        deviceData.api_controllable = form.elements.api_controllable.checked;

        try {
            const response = await fetch(`/devices/api/${deviceId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(deviceData)
            });

            const result = await response.json();

            if (result.success) {
                alert('Device updated successfully!');
                window.location.reload();
            } else {
                alert('Error: ' + result.message);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error updating device');
        }
    },

    deleteDevice: async function (deviceId) {
        if (!confirm('Are you sure you want to delete this device?')) {
            return;
        }

        try {
            const response = await fetch(`/devices/api/${deviceId}`, {
                method: 'DELETE'
            });

            const result = await response.json();

            if (result.success) {
                alert('Device deleted successfully!');
                window.location.reload();
            } else {
                alert('Error: ' + result.message);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error deleting device');
        }
    }
};

// Functions to toggle conditional fields
function toggleSchedulingFields(checkbox) {
    const fields = document.getElementById('schedulingFields');
    fields.style.display = checkbox.checked ? 'block' : 'none';
}

function toggleEVFields(checkbox) {
    const fields = document.getElementById('evFields');
    fields.style.display = checkbox.checked ? 'block' : 'none';
}

function toggleEditSchedulingFields(checkbox) {
    const fields = document.getElementById('editSchedulingFields');
    fields.style.display = checkbox.checked ? 'block' : 'none';
}

function toggleEditEVFields(checkbox) {
    const fields = document.getElementById('editEVFields');
    fields.style.display = checkbox.checked ? 'block' : 'none';
}