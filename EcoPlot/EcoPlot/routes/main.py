# EcoPlot/routes/main.py
from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from flask_login import login_required, current_user
from EcoPlot import db
from EcoPlot.models.device import Device
from EcoPlot.models.device_type import DeviceType
from EcoPlot.models.device_brand import DeviceBrand

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@main_bp.route('/api/devices/add', methods=['POST'])
@login_required
def add_device():
    """API endpoint to add a device"""
    data = request.get_json()
    
    # Create device directly (no predefined devices)
    try:
        device = Device(
            user_id=current_user.id,
            name=data['name'],
            device_type_id=data['device_type_id'],
            brand_id=data['brand_id'],
            model=data.get('model'),
            power_consumption_watts=data['power_consumption_watts'],
            standby_power_watts=data.get('standby_power_watts', 0),
            average_usage_hours_per_day=data.get('average_usage_hours_per_day'),
            usage_flexibility=data.get('usage_flexibility', 0),
            priority_level=data.get('priority_level', 5),
            is_schedulable=data.get('is_schedulable', False),
            is_ev_charger=data.get('is_ev_charger', False),
            is_smart_device=data.get('is_smart_device', False),
            api_controllable=data.get('api_controllable', False)
        )
        
        db.session.add(device)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Device added successfully',
            'device': device.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@main_bp.route('/api/devices/<int:device_id>', methods=['PUT'])
@login_required
def update_device(device_id):
    """API endpoint to update a device"""
    device = Device.query.filter_by(id=device_id, user_id=current_user.id).first_or_404()
    data = request.get_json()
    
    try:
        # Update device fields
        for key, value in data.items():
            if hasattr(device, key):
                setattr(device, key, value)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Device updated successfully',
            'device': device.to_dict()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@main_bp.route('/api/devices/<int:device_id>', methods=['DELETE'])
@login_required
def delete_device(device_id):
    """API endpoint to delete a device"""
    device = Device.query.filter_by(id=device_id, user_id=current_user.id).first_or_404()
    
    try:
        db.session.delete(device)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Device deleted successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@main_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

# API endpoint to get user's devices (useful for dashboard)
@main_bp.route('/api/devices/user', methods=['GET'])
@login_required
def get_user_devices():
    """Get all devices for the current user"""
    devices = Device.query.filter_by(user_id=current_user.id).all()
    return jsonify({
        'success': True,
        'devices': [device.to_dict() for device in devices]
    })