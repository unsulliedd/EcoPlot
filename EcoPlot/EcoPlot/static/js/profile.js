// EcoPlot/static/js/profile.js
document.addEventListener('DOMContentLoaded', function () {
    // Advanced location fields toggle
    initLocationFieldsToggle();

    // Initialize all toggle sections
    initToggleSections();

    // Set up form validation
    initFormValidation();
});

/**
 * Initialize the toggle for advanced location fields
 */
function initLocationFieldsToggle() {
    const toggleLocationBtn = document.getElementById('toggleLocationFields');
    const advancedLocationFields = document.getElementById('advancedLocationFields');

    // Set initial state - hidden by default
    advancedLocationFields.style.display = 'none';

    toggleLocationBtn.addEventListener('click', function () {
        if (advancedLocationFields.style.display === 'none') {
            advancedLocationFields.style.display = 'block';
            toggleLocationBtn.textContent = 'Hide Advanced Location Fields';
        } else {
            advancedLocationFields.style.display = 'none';
            toggleLocationBtn.textContent = 'Show Advanced Location Fields';
        }
    });
}

/**
 * Initialize all toggle sections (solar, wind, battery, EV)
 */
function initToggleSections() {
    const toggleSections = document.querySelectorAll('.toggle-section');

    toggleSections.forEach(function (toggle) {
        // Find the target section ID from the hidden input
        const targetInput = toggle.nextElementSibling.nextElementSibling;
        const targetId = targetInput.value;
        const targetSection = document.getElementById(targetId);

        // Set initial state based on checkbox
        targetSection.style.display = toggle.checked ? 'block' : 'none';

        // Add event listener for future changes
        toggle.addEventListener('change', function () {
            targetSection.style.display = this.checked ? 'block' : 'none';
        });
    });
}

/**
 * Basic form validation 
 */
function initFormValidation() {
    const form = document.querySelector('form');

    form.addEventListener('submit', function (event) {
        let isValid = true;

        // Validate solar fields if solar is checked
        const hasSolar = document.getElementById('has_solar');
        if (hasSolar.checked) {
            const solarCapacity = document.getElementById('solar_capacity_kw');
            if (solarCapacity.value === '' || parseFloat(solarCapacity.value) <= 0) {
                markInvalid(solarCapacity, 'Please enter a valid solar capacity');
                isValid = false;
            } else {
                markValid(solarCapacity);
            }
        }

        // Validate EV fields if EV is checked
        const hasEV = document.getElementById('has_ev');
        if (hasEV.checked) {
            const evManufacturer = document.getElementById('ev_manufacturer');
            if (evManufacturer.value === '') {
                markInvalid(evManufacturer, 'Please enter your EV manufacturer');
                isValid = false;
            } else {
                markValid(evManufacturer);
            }

            const evModel = document.getElementById('ev_model');
            if (evModel.value === '') {
                markInvalid(evModel, 'Please enter your EV model');
                isValid = false;
            } else {
                markValid(evModel);
            }
        }

        // Validate battery fields if battery is checked
        const hasBattery = document.getElementById('has_battery_storage');
        if (hasBattery.checked) {
            const batteryCapacity = document.getElementById('battery_capacity_kwh');
            if (batteryCapacity.value === '' || parseFloat(batteryCapacity.value) <= 0) {
                markInvalid(batteryCapacity, 'Please enter a valid battery capacity');
                isValid = false;
            } else {
                markValid(batteryCapacity);
            }
        }

        // Validate wind fields if wind is checked
        const hasWind = document.getElementById('has_wind_turbine');
        if (hasWind.checked) {
            const windCapacity = document.getElementById('wind_turbine_capacity_kw');
            if (windCapacity.value === '' || parseFloat(windCapacity.value) <= 0) {
                markInvalid(windCapacity, 'Please enter a valid wind turbine capacity');
                isValid = false;
            } else {
                markValid(windCapacity);
            }
        }

        // If form is not valid, prevent submission
        if (!isValid) {
            event.preventDefault();

            // Scroll to the first invalid element
            const firstInvalid = document.querySelector('.is-invalid');
            if (firstInvalid) {
                firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }
    });
}

/**
 * Mark a form field as invalid
 */
function markInvalid(element, message) {
    element.classList.add('is-invalid');

    // Create error message if it doesn't exist
    let feedback = element.nextElementSibling;
    if (!feedback || !feedback.classList.contains('invalid-feedback')) {
        feedback = document.createElement('div');
        feedback.className = 'invalid-feedback';
        element.parentNode.insertBefore(feedback, element.nextSibling);
    }

    feedback.textContent = message;
}

/**
 * Mark a form field as valid
 */
function markValid(element) {
    element.classList.remove('is-invalid');
    element.classList.add('is-valid');

    // Remove error message if it exists
    const feedback = element.nextElementSibling;
    if (feedback && feedback.classList.contains('invalid-feedback')) {
        feedback.remove();
    }
}

/**
 * Check for field completion status and update UI accordingly
 */
function checkProfileCompletionStatus() {
    // Check if user has at least one renewable energy or EV
    const hasSolar = document.getElementById('has_solar').checked;
    const hasEV = document.getElementById('has_ev').checked;
    const hasBattery = document.getElementById('has_battery_storage').checked;
    const hasWind = document.getElementById('has_wind_turbine').checked;

    // Check if one of them is enabled
    const hasAnyRenewable = hasSolar || hasEV || hasBattery || hasWind;

    // Display completion banner if profile is incomplete
    const completionBanner = document.getElementById('completionBanner');
    if (completionBanner) {
        completionBanner.style.display = hasAnyRenewable ? 'none' : 'block';
    }
}

// Call this function when the page loads and when form values change
document.addEventListener('DOMContentLoaded', function () {
    checkProfileCompletionStatus();

    // Add event listeners to monitor changes
    const checkboxes = document.querySelectorAll('.toggle-section');
    checkboxes.forEach(function (checkbox) {
        checkbox.addEventListener('change', checkProfileCompletionStatus);
    });
});