# EcoPlot/routes/main.py (updated)
from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from EcoPlot import db
from EcoPlot.forms.profile import ProfileForm
from EcoPlot.models.device import Device
from EcoPlot.models.device_type import DeviceType
from EcoPlot.models.device_brand import DeviceBrand
from EcoPlot.models.recommendation import RecommendationHistory
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@main_bp.route('/api/dashboard/summary')
@login_required
def dashboard_summary():
    """API endpoint to get dashboard summary data"""
    try:
        # Get time period from query parameter (default: day)
        period = request.args.get('period', 'day')
        
        # In a real implementation, this would query the database
        # For now, let's return some mock data
        
        # Calculate different values based on the period
        energy_used = 0
        energy_produced = 0
        carbon_saved = 0
        cost_savings = 0
        
        if period == 'day':
            energy_used = 12.5
            energy_produced = 8.7
            carbon_saved = 3.8
            cost_savings = 2.35
        elif period == 'week':
            energy_used = 78.3
            energy_produced = 54.2
            carbon_saved = 24.5
            cost_savings = 14.75
        else:  # month
            energy_used = 320.6
            energy_produced = 210.8
            carbon_saved = 95.7
            cost_savings = 58.20
        
        return jsonify({
            'success': True,
            'period': period,
            'summary': {
                'energy_used': energy_used,
                'energy_used_change': -5.2,  # percentage change
                'energy_produced': energy_produced,
                'energy_produced_change': 12.3,
                'carbon_saved': carbon_saved,
                'carbon_saved_change': 8.7,
                'cost_savings': cost_savings,
                'cost_savings_change': 10.5
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@main_bp.route('/api/dashboard/devices')
@login_required
def dashboard_devices():
    """API endpoint to get device energy consumption data"""
    try:
        # Get devices with their type and brand
        devices_query = db.session.query(
            Device,
            DeviceType.name.label('device_type_name'),
            DeviceBrand.name.label('brand_name')
        ).join(
            DeviceType, Device.device_type_id == DeviceType.id
        ).join(
            DeviceBrand, Device.brand_id == DeviceBrand.id
        ).filter(
            Device.user_id == current_user.id
        ).order_by(
            Device.power_consumption_watts.desc()
        ).all()
        
        # Format device data
        devices_data = []
        for device, device_type_name, brand_name in devices_query:
            # Calculate daily usage based on average usage hours
            daily_usage = 0
            if device.average_usage_hours_per_day and device.power_consumption_watts:
                daily_usage = (device.average_usage_hours_per_day * device.power_consumption_watts) / 1000  # kWh
            
            devices_data.append({
                'id': device.id,
                'name': device.name,
                'type': device_type_name,
                'brand': brand_name,
                'power_watts': device.power_consumption_watts,
                'daily_usage_kwh': daily_usage,
                'is_ev_charger': device.is_ev_charger,
                'is_smart_device': device.is_smart_device,
                'is_schedulable': device.is_schedulable
            })
        
        return jsonify({
            'success': True,
            'devices': devices_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@main_bp.route('/api/dashboard/energy-usage')
@login_required
def dashboard_energy_usage():
    """API endpoint to get energy usage and production data"""
    try:
        # Get time period from query parameter (default: day)
        period = request.args.get('period', 'day')
        
        # In a real implementation, this would query usage logs from the database
        # For now, return mock data with appropriate time labels
        
        # Generate time labels based on period
        time_labels = []
        consumption_data = []
        production_data = []
        
        if period == 'day':
            # Hourly data for a day
            for i in range(24):
                time_labels.append(f"{i}:00")
                
                # Create realistic usage pattern
                if i < 6:  # Night (low)
                    consumption = 0.2 + (i * 0.05)
                elif i < 10:  # Morning peak
                    consumption = 0.5 + ((i - 5) * 0.2)
                elif i < 16:  # Midday (medium)
                    consumption = 0.5 + (i % 3) * 0.1
                elif i < 22:  # Evening peak
                    consumption = 0.8 + ((i - 15) * 0.15)
                else:  # Late night (low)
                    consumption = 0.5 - ((i - 21) * 0.15)
                
                # Solar production follows sun pattern
                if i >= 6 and i <= 20:  # Daylight hours
                    # Bell curve centered at 1pm (hour 13)
                    hour_offset = abs(i - 13)
                    production = max(0, 0.8 - (hour_offset * 0.12))
                else:
                    production = 0
                
                consumption_data.append(round(consumption, 2))
                production_data.append(round(production, 2))
                
        elif period == 'week':
            # Daily data for a week
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            for i, day in enumerate(days):
                time_labels.append(day)
                
                # Higher usage on weekends
                is_weekend = i >= 5
                base_consumption = 10 if is_weekend else 8
                consumption = base_consumption + (i * 0.5) % 2
                
                # Solar production varies by day (simulated weather effects)
                weather_factor = 0.8 + (i * 0.1) % 0.4
                production = 7 * weather_factor
                
                consumption_data.append(round(consumption, 2))
                production_data.append(round(production, 2))
                
        else:  # month
            # Generate 30 days of data
            for i in range(1, 31):
                time_labels.append(f"Day {i}")
                
                # Weekend effect (every 6th and 7th day)
                is_weekend = (i % 7 == 6) or (i % 7 == 0)
                base_consumption = 12 if is_weekend else 9.5
                
                # Random daily fluctuation
                daily_factor = 0.8 + (i * 0.13) % 0.5
                consumption = base_consumption * daily_factor
                
                # Solar production with weather patterns
                weather_factor = 0.7 + (i * 0.19) % 0.6
                production = 8 * weather_factor
                
                consumption_data.append(round(consumption, 2))
                production_data.append(round(production, 2))
        
        return jsonify({
            'success': True,
            'period': period,
            'labels': time_labels,
            'consumption': consumption_data,
            'production': production_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@main_bp.route('/api/dashboard/recommendations')
@login_required
def dashboard_recommendations():
    """API endpoint to get the latest recommendations for dashboard"""
    try:
        # Get latest recommendation history record
        latest_recs = RecommendationHistory.query.filter_by(
            user_id=current_user.id
        ).order_by(
            RecommendationHistory.created_at.desc()
        ).first()
        
        # Format recommendations for dashboard display
        recommendations = []
        
        if latest_recs and latest_recs.recommendations_json:
            import json
            rec_data = json.loads(latest_recs.recommendations_json)
            
            # Get overall recommendations (just the first 4)
            overall_recs = rec_data.get('overall_recommendations', [])
            for i, rec in enumerate(overall_recs[:4]):
                recommendations.append({
                    'content': rec,
                    'saving': f"${(4 - i) * 1.5:.2f} per month"  # Dummy savings estimates
                })
            
            # Add device-specific recommendations if we don't have 4 yet
            if len(recommendations) < 4:
                device_recs = rec_data.get('device_recommendations', {})
                for device_id, device_data in device_recs.items():
                    if len(recommendations) >= 4:
                        break
                    recommendations.append({
                        'content': device_data.get('recommendation', ''),
                        'saving': f"${device_data.get('estimated_savings', 0):.2f} per month"
                    })
        
        # If we still don't have recommendations, provide defaults
        if not recommendations:
            recommendations = [
                {
                    'content': 'Add more devices to get personalized recommendations',
                    'saving': 'Potential savings'
                },
                {
                    'content': 'Complete your profile with energy preferences',
                    'saving': 'Improve accuracy'
                }
            ]
        
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'last_updated': latest_recs.created_at.isoformat() if latest_recs else None
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

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
        # Update user profile data
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