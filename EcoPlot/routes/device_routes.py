# EcoPlot/routes/device_routes.py
from flask import request, jsonify, current_app
from EcoPlot import db
from EcoPlot.models.device import Device  # Updated import path
from EcoPlot.models.user import User
from EcoPlot.routes import main_bp

@main_bp.route('/devices', methods=['GET'])
def get_devices():
    # For hackathon, we'll use a simple approach without authentication
    # In a real app, you'd get the user_id from the authenticated session
    user_id = request.args.get('user_id', 1, type=int)
    
    devices = Device.query.filter_by(user_id=user_id).all()
    return jsonify({
        'success': True,
        'devices': [device.to_dict() for device in devices]
    })

@main_bp.route('/devices', methods=['POST'])
def add_device():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['user_id', 'name', 'device_type', 'power_consumption_watts']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'success': False,
                'message': f'Missing required field: {field}'
            }), 400
    
    # Create new device
    new_device = Device(
        user_id=data['user_id'],
        name=data['name'],
        device_type=data['device_type'],
        brand=data.get('brand'),
        model=data.get('model'),
        power_consumption_watts=data['power_consumption_watts'],
        standby_power_watts=data.get('standby_power_watts', 0.0),
        average_usage_hours_per_day=data.get('average_usage_hours_per_day'),
        usage_flexibility=data.get('usage_flexibility', 0),
        is_schedulable=data.get('is_schedulable', False),
        is_ev_charger=data.get('is_ev_charger', False),
        is_smart_device=data.get('is_smart_device', False),
        api_controllable=data.get('api_controllable', False)
    )
    
    # Handle additional fields for specific device types
    if new_device.is_schedulable:
        new_device.preferred_start_time = data.get('preferred_start_time')
        new_device.preferred_end_time = data.get('preferred_end_time')
        new_device.operation_duration_minutes = data.get('operation_duration_minutes')
    
    if new_device.is_ev_charger:
        new_device.ev_battery_capacity_kwh = data.get('ev_battery_capacity_kwh')
        new_device.charging_rate_kw = data.get('charging_rate_kw')
    
    db.session.add(new_device)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Device added successfully',
        'device': new_device.to_dict()
    }), 201

@main_bp.route('/devices/<int:device_id>', methods=['PUT'])
def update_device(device_id):
    device = Device.query.get_or_404(device_id)
    data = request.get_json()
    
    # Update fields
    for key, value in data.items():
        if hasattr(device, key):
            setattr(device, key, value)
    
    db.session.commit()
    return jsonify({
        'success': True,
        'message': 'Device updated successfully',
        'device': device.to_dict()
    })

@main_bp.route('/devices/<int:device_id>', methods=['DELETE'])
def delete_device(device_id):
    device = Device.query.get_or_404(device_id)
    db.session.delete(device)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Device deleted successfully'
    })