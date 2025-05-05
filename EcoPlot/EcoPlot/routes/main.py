# EcoPlot/routes/main.py
from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from EcoPlot import db
from EcoPlot.forms.profile import ProfileForm

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    
    # Pre-populate form with existing user data
    if request.method == 'GET':
        # Location info
        form.address.data = current_user.address
        form.city.data = current_user.city
        form.state.data = current_user.state
        form.country.data = current_user.country
        form.postal_code.data = current_user.postal_code
        form.latitude.data = current_user.latitude
        form.longitude.data = current_user.longitude
        form.timezone.data = current_user.timezone
        
        # Home characteristics
        form.home_size_sqft.data = current_user.home_size_sqft
        form.home_type.data = current_user.home_type
        form.occupants_count.data = current_user.occupants_count
        
        # Solar energy
        form.has_solar.data = current_user.has_solar
        form.solar_capacity_kw.data = current_user.solar_capacity_kw
        form.solar_panel_orientation.data = current_user.solar_panel_orientation
        form.solar_panel_tilt.data = current_user.solar_panel_tilt
        form.solar_installation_date.data = current_user.solar_installation_date
        
        # Wind energy
        form.has_wind_turbine.data = current_user.has_wind_turbine
        form.wind_turbine_capacity_kw.data = current_user.wind_turbine_capacity_kw
        form.wind_turbine_height_meters.data = current_user.wind_turbine_height_meters
        
        # EV details
        form.has_ev.data = current_user.has_ev
        form.ev_manufacturer.data = current_user.ev_manufacturer
        form.ev_model.data = current_user.ev_model
        form.ev_battery_capacity_kwh.data = current_user.ev_battery_capacity_kwh
        form.ev_typical_daily_usage_kwh.data = current_user.ev_typical_daily_usage_kwh
        form.ev_charging_preference.data = current_user.ev_charging_preference
        
        # Battery storage
        form.has_battery_storage.data = current_user.has_battery_storage
        form.battery_capacity_kwh.data = current_user.battery_capacity_kwh
        form.battery_brand.data = current_user.battery_brand
        
        # Utility details
        form.utility_provider.data = current_user.utility_provider
        form.electricity_rate_plan.data = current_user.electricity_rate_plan
        form.peak_rate_per_kwh.data = current_user.peak_rate_per_kwh
        form.off_peak_rate_per_kwh.data = current_user.off_peak_rate_per_kwh
        form.solar_feed_in_tariff.data = current_user.solar_feed_in_tariff
        
        # User preferences
        form.energy_savings_goal.data = current_user.energy_savings_goal
        form.environmental_priority.data = current_user.environmental_priority
        form.budget_constraints.data = current_user.budget_constraints
        form.notification_preferences.data = current_user.notification_preferences
        form.language_preference.data = current_user.language_preference
        
        # Integration settings
        form.smart_home_platform.data = current_user.smart_home_platform
        form.weather_api_preference.data = current_user.weather_api_preference
    
    if form.validate_on_submit():

        is_profile_complete = False

        # Location info
        current_user.address = form.address.data
        current_user.city = form.city.data
        current_user.state = form.state.data
        current_user.country = form.country.data
        current_user.postal_code = form.postal_code.data
        current_user.latitude = form.latitude.data
        current_user.longitude = form.longitude.data
        current_user.timezone = form.timezone.data
        
        # Home characteristics
        current_user.home_size_sqft = form.home_size_sqft.data
        current_user.home_type = form.home_type.data
        current_user.occupants_count = form.occupants_count.data
        
        # Solar energy
        current_user.has_solar = form.has_solar.data
        current_user.solar_capacity_kw = form.solar_capacity_kw.data
        current_user.solar_panel_orientation = form.solar_panel_orientation.data
        current_user.solar_panel_tilt = form.solar_panel_tilt.data
        current_user.solar_installation_date = form.solar_installation_date.data
        
        # Wind energy
        current_user.has_wind_turbine = form.has_wind_turbine.data
        current_user.wind_turbine_capacity_kw = form.wind_turbine_capacity_kw.data
        current_user.wind_turbine_height_meters = form.wind_turbine_height_meters.data
        
        # EV details
        current_user.has_ev = form.has_ev.data
        current_user.ev_manufacturer = form.ev_manufacturer.data
        current_user.ev_model = form.ev_model.data
        current_user.ev_battery_capacity_kwh = form.ev_battery_capacity_kwh.data
        current_user.ev_typical_daily_usage_kwh = form.ev_typical_daily_usage_kwh.data
        current_user.ev_charging_preference = form.ev_charging_preference.data
        
        # Battery storage
        current_user.has_battery_storage = form.has_battery_storage.data
        current_user.battery_capacity_kwh = form.battery_capacity_kwh.data
        current_user.battery_brand = form.battery_brand.data
        
        # Utility details
        current_user.utility_provider = form.utility_provider.data
        current_user.electricity_rate_plan = form.electricity_rate_plan.data
        current_user.peak_rate_per_kwh = form.peak_rate_per_kwh.data
        current_user.off_peak_rate_per_kwh = form.off_peak_rate_per_kwh.data
        current_user.solar_feed_in_tariff = form.solar_feed_in_tariff.data
        
        # User preferences
        current_user.energy_savings_goal = form.energy_savings_goal.data
        current_user.environmental_priority = form.environmental_priority.data
        current_user.budget_constraints = form.budget_constraints.data
        current_user.notification_preferences = form.notification_preferences.data
        current_user.language_preference = form.language_preference.data
        
        # Integration settings
        current_user.smart_home_platform = form.smart_home_platform.data
        current_user.weather_api_preference = form.weather_api_preference.data
        
        # Save to database
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        
        # Redirect based on profile completion status
        if is_profile_complete and request.form.get('origin') == 'registration':
            # If this was their first login after registration and profile is complete
            return redirect(url_for('main.dashboard'))
        else:
            # Otherwise stay on profile page
            return redirect(url_for('main.profile'))
    
    # Determine if this is their first visit to profile after registration
    is_first_visit = request.args.get('first_visit', 'false') == 'true'
    
    # Return the profile template with the form
    return render_template('profile.html', form=form, 
                          is_first_visit=is_first_visit,
                          profile_data=current_user)

@main_bp.route('/recommendations')
@login_required
def recommendations():
    return render_template('recommendations.html')

