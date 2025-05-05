# EcoPlot/routes/recommendation_routes.py
from flask import Blueprint, render_template, jsonify, request, current_app
from flask_login import login_required, current_user
from EcoPlot import db
from EcoPlot.models.device import Device
from EcoPlot.models.device_type import DeviceType
from EcoPlot.models.device_brand import DeviceBrand
from EcoPlot.models.recommendation import RecommendationHistory
from EcoPlot.services.gemini_service import GeminiService
from sqlalchemy.orm import joinedload

recommendations_bp = Blueprint('recommendations', __name__)

@recommendations_bp.route('/recommendations')
@login_required
def recommendations_page():
    """Render the recommendations page"""
    return render_template('recommendations.html')

@recommendations_bp.route('/api/recommendations', methods=['GET'])
@login_required
def get_recommendations():
    """API endpoint to get personalized device usage recommendations"""
    try:
        # Check if the user has any devices
        device_count = Device.query.filter_by(user_id=current_user.id).count()
        if device_count == 0:
            return jsonify({
                'success': False,
                'error': 'No devices found. Please add at least one device to get recommendations.'
            }), 400

        # Get all user devices with related information
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
        ).all()
        
        # Format devices data for the Gemini service
        devices_data = []
        for device, device_type_name, brand_name in devices_query:
            devices_data.append({
                'id': device.id,
                'name': device.name,
                'device_type_name': device_type_name,
                'brand_name': brand_name,
                'power_consumption_watts': device.power_consumption_watts,
                'standby_power_watts': device.standby_power_watts,
                'average_usage_hours_per_day': device.average_usage_hours_per_day,
                'usage_flexibility': device.usage_flexibility,
                'is_schedulable': device.is_schedulable,
                'is_smart_device': device.is_smart_device,
                'is_ev_charger': device.is_ev_charger,
                'priority_level': device.priority_level
            })
        
        # Create user profile data for recommendations
        user_data = {
            'id': current_user.id,
            'username': current_user.username,
            'location': f"{current_user.city}, {current_user.state}, {current_user.country}" 
                if (current_user.city and current_user.state and current_user.country) else None,
            'city': current_user.city,
            'state': current_user.state,
            'country': current_user.country,
            'has_solar': current_user.has_solar,
            'solar_capacity_kw': current_user.solar_capacity_kw,
            'solar_panel_orientation': current_user.solar_panel_orientation,
            'solar_panel_tilt': current_user.solar_panel_tilt,
            'has_battery_storage': current_user.has_battery_storage,
            'battery_capacity_kwh': current_user.battery_capacity_kwh,
            'has_ev': current_user.has_ev,
            'ev_battery_capacity_kwh': current_user.ev_battery_capacity_kwh,
            'energy_savings_goal': current_user.energy_savings_goal,
            'environmental_priority': current_user.environmental_priority,
            'electricity_rate_plan': current_user.electricity_rate_plan,
            'peak_rate_per_kwh': current_user.peak_rate_per_kwh,
            'off_peak_rate_per_kwh': current_user.off_peak_rate_per_kwh,
        }
        
        # Get recommendations from Gemini service
        gemini_service = GeminiService()
        recommendations = gemini_service.generate_device_recommendations(user_data, devices_data)
        
        # Store the recommendations for historical comparison if successful
        if recommendations.get('success', False):
            try:
                # Create a new recommendation history entry
                history = RecommendationHistory.create_from_response(
                    user_id=current_user.id,
                    recommendations_data=recommendations,
                    device_count=len(devices_data),
                    has_solar=current_user.has_solar,
                    has_ev=current_user.has_ev,
                    has_battery=current_user.has_battery_storage
                )
                db.session.add(history)
                db.session.commit()
            except Exception as history_error:
                current_app.logger.error(f"Error saving recommendation history: {str(history_error)}")
                # Continue even if saving history fails
        
        # Return recommendations as JSON
        return jsonify({
            'success': True,
            'user': {
                'id': current_user.id,
                'username': current_user.username,
                'has_solar': current_user.has_solar,
                'has_ev': current_user.has_ev
            },
            'devices_count': len(devices_data),
            'recommendations': recommendations
        })
    
    except Exception as e:
        current_app.logger.error(f"Error generating recommendations: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@recommendations_bp.route('/api/recommendations/device/<int:device_id>', methods=['GET'])
@login_required
def get_device_recommendations(device_id):
    """Get recommendations for a specific device"""
    try:
        # Get the specific device with its type and brand
        device_query = db.session.query(
            Device,
            DeviceType.name.label('device_type_name'),
            DeviceBrand.name.label('brand_name')
        ).join(
            DeviceType, Device.device_type_id == DeviceType.id
        ).join(
            DeviceBrand, Device.brand_id == DeviceBrand.id
        ).filter(
            Device.id == device_id,
            Device.user_id == current_user.id
        ).first()
        
        if not device_query:
            return jsonify({
                'success': False,
                'error': 'Device not found or not owned by user'
            }), 404
        
        device, device_type_name, brand_name = device_query
        
        # Format device data
        device_data = [{
            'id': device.id,
            'name': device.name,
            'device_type_name': device_type_name,
            'brand_name': brand_name,
            'power_consumption_watts': device.power_consumption_watts,
            'standby_power_watts': device.standby_power_watts,
            'average_usage_hours_per_day': device.average_usage_hours_per_day,
            'usage_flexibility': device.usage_flexibility,
            'is_schedulable': device.is_schedulable,
            'is_smart_device': device.is_smart_device,
            'is_ev_charger': device.is_ev_charger,
            'priority_level': device.priority_level
        }]
        
        # Create user profile data
        user_data = {
            'id': current_user.id,
            'username': current_user.username,
            'location': f"{current_user.city}, {current_user.state}, {current_user.country}" 
                if (current_user.city and current_user.state and current_user.country) else None,
            'has_solar': current_user.has_solar,
            'solar_capacity_kw': current_user.solar_capacity_kw,
            'has_battery_storage': current_user.has_battery_storage,
            'battery_capacity_kwh': current_user.battery_capacity_kwh,
            'has_ev': current_user.has_ev,
            'electricity_rate_plan': current_user.electricity_rate_plan,
            'peak_rate_per_kwh': current_user.peak_rate_per_kwh,
            'off_peak_rate_per_kwh': current_user.off_peak_rate_per_kwh,
        }
        
        # Get specific recommendations for this device
        gemini_service = GeminiService()
        recommendations = gemini_service.generate_device_recommendations(user_data, device_data)
        
        return jsonify({
            'success': True,
            'device': device_data[0],
            'recommendations': recommendations
        })
    
    except Exception as e:
        current_app.logger.error(f"Error generating device recommendations: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@recommendations_bp.route('/api/recommendations/history', methods=['GET'])
@login_required
def get_recommendations_history():
    """Get historical recommendations data for comparison"""
    try:
        # Get the user's recommendation history, ordered by most recent first
        history_entries = RecommendationHistory.query\
            .filter_by(user_id=current_user.id)\
            .order_by(RecommendationHistory.created_at.desc())\
            .limit(10)\
            .all()
        
        # Format the history entries for the response
        history_data = [entry.to_dict() for entry in history_entries]
        
        return jsonify({
            'success': True,
            'history': history_data
        })
    except Exception as e:
        current_app.logger.error(f"Error fetching recommendation history: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500