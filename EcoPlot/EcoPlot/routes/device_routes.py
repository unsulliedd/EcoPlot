# EcoPlot/routes/device_routes.py
from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from flask_login import login_required, current_user
from EcoPlot import db
from EcoPlot.models.device import Device
from EcoPlot.models.device_type import DeviceType
from EcoPlot.models.device_brand import DeviceBrand
from datetime import datetime, time

devices_bp = Blueprint('devices', __name__, url_prefix='/devices')

# Page routes
@devices_bp.route('/')
@login_required
def index():
    """Display all device categories"""
    device_types = DeviceType.query.all()
    return render_template('devices/index.html', device_types=device_types)

@devices_bp.route('/type/<int:type_id>/brands')
@login_required
def brands_by_type(type_id):
    """Display brands for a specific device type"""
    device_type = DeviceType.query.get_or_404(type_id)
    brands = DeviceBrand.query.filter_by(device_type_id=type_id).all()
    return render_template('devices/brands.html', device_type=device_type, brands=brands)

@devices_bp.route('/type/<int:type_id>/brand/<int:brand_id>')
@login_required
def devices_by_brand(type_id, brand_id):
    """Display devices for a specific brand and device type"""
    device_type = DeviceType.query.get_or_404(type_id)
    brand = DeviceBrand.query.get_or_404(brand_id)
    user_devices = Device.query.filter_by(
        user_id=current_user.id,
        device_type_id=type_id,
        brand_id=brand_id
    ).all()
    return render_template('devices/device_list.html', 
                         device_type=device_type, 
                         brand=brand, 
                         user_devices=user_devices)

# API endpoints
@devices_bp.route('/api/<int:device_id>', methods=['GET'])
@login_required
def get_device(device_id):
    """API endpoint to get a specific device"""
    device = Device.query.filter_by(id=device_id, user_id=current_user.id).first_or_404()
    
    return jsonify({
        'success': True,
        'device': device.to_dict()
    })

@devices_bp.route('/api/add', methods=['POST'])
@login_required
def add_device():
    """API endpoint to add a device"""
    data = request.get_json()
    
    try:
        # Convert time fields if they exist
        if 'preferred_start_time' in data:
            if not data['preferred_start_time'] or data['preferred_start_time'] == '':
                data['preferred_start_time'] = None
            else:
                try:
                    hours, minutes = map(int, data['preferred_start_time'].split(':'))
                    data['preferred_start_time'] = time(hours, minutes)
                except (ValueError, AttributeError, TypeError):
                    data['preferred_start_time'] = None
        else:
            data['preferred_start_time'] = None
        
        if 'preferred_end_time' in data:
            if not data['preferred_end_time'] or data['preferred_end_time'] == '':
                data['preferred_end_time'] = None
            else:
                try:
                    hours, minutes = map(int, data['preferred_end_time'].split(':'))
                    data['preferred_end_time'] = time(hours, minutes)
                except (ValueError, AttributeError, TypeError):
                    data['preferred_end_time'] = None
        else:
            data['preferred_end_time'] = None
        
        # Convert numeric fields
        numeric_fields = ['power_consumption_watts', 'standby_power_watts', 'average_usage_hours_per_day', 
                         'usage_flexibility', 'priority_level', 'operation_duration_minutes', 
                         'ev_battery_capacity_kwh', 'charging_rate_kw']
        
        for field in numeric_fields:
            if field in data and data[field] is not None and data[field] != '':
                try:
                    if isinstance(data[field], str) and '.' in data[field]:
                        data[field] = float(data[field])
                    else:
                        data[field] = int(float(data[field]))
                except (ValueError, TypeError):
                    # Set default values for required fields
                    if field == 'power_consumption_watts':
                        data[field] = 0  # Set a default value for required field
                    elif field == 'standby_power_watts':
                        data[field] = 0
                    elif field == 'usage_flexibility':
                        data[field] = 0
                    elif field == 'priority_level':
                        data[field] = 5
                    else:
                        data[field] = None
            else:
                # Handle empty or None values with defaults
                if field == 'standby_power_watts':
                    data[field] = 0
                elif field == 'usage_flexibility':
                    data[field] = 0
                elif field == 'priority_level':
                    data[field] = 5
                else:
                    data[field] = None
        
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
            preferred_start_time=data.get('preferred_start_time'),
            preferred_end_time=data.get('preferred_end_time'),
            operation_duration_minutes=data.get('operation_duration_minutes'),
            is_ev_charger=data.get('is_ev_charger', False),
            ev_battery_capacity_kwh=data.get('ev_battery_capacity_kwh'),
            charging_rate_kw=data.get('charging_rate_kw'),
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
        db.session.rollback()  # Add rollback to prevent partial updates
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@devices_bp.route('/api/<int:device_id>', methods=['PUT'])
@login_required
def update_device(device_id):
    """API endpoint to update a device"""
    device = Device.query.filter_by(id=device_id, user_id=current_user.id).first_or_404()
    data = request.get_json()
    
    try:
        # Process each field in the data
        for key, value in data.items():
            if hasattr(device, key):
                # Handle time fields
                if key in ['preferred_start_time', 'preferred_end_time']:
                    if value is None or value == '':
                        value = None
                    elif isinstance(value, str):
                        try:
                            hours, minutes = map(int, value.split(':'))
                            value = time(hours, minutes)
                        except (ValueError, TypeError):
                            value = None
                
                # Handle numeric fields
                elif key in ['power_consumption_watts', 'standby_power_watts', 'average_usage_hours_per_day', 
                           'usage_flexibility', 'priority_level', 'operation_duration_minutes', 
                           'ev_battery_capacity_kwh', 'charging_rate_kw']:
                    if value is None or value == '':
                        value = None
                    else:
                        try:
                            # Convert to float if number has decimal, else int
                            if isinstance(value, str) and '.' in value:
                                value = float(value)
                            else:
                                value = int(float(value)) if value is not None else None
                        except (ValueError, TypeError):
                            # If conversion fails, skip this field
                            continue
                
                # Set the attribute
                setattr(device, key, value)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Device updated successfully',
            'device': device.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@devices_bp.route('/api/<int:device_id>', methods=['DELETE'])
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

@devices_bp.route('/api/user', methods=['GET'])
@login_required
def get_user_devices():
    """Get all devices for the current user"""
    devices = Device.query.filter_by(user_id=current_user.id).all()
    return jsonify({
        'success': True,
        'devices': [device.to_dict() for device in devices]
    })

@devices_bp.route('/api/categories', methods=['GET'])
@login_required
def get_device_categories():
    """Get all device categories"""
    device_types = DeviceType.query.all()
    return jsonify({
        'success': True,
        'device_types': [{'id': dt.id, 'name': dt.name, 'description': dt.description} for dt in device_types]
    })

@devices_bp.route('/api/brands/<int:type_id>', methods=['GET'])
@login_required
def get_brands_by_type(type_id):
    """Get all brands for a specific device type"""
    brands = DeviceBrand.query.filter_by(device_type_id=type_id).all()
    return jsonify({
        'success': True,
        'brands': [{'id': brand.id, 'name': brand.name} for brand in brands]
    })
