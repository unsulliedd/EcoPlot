# EcoPlot/routes/admin_routes.py
from flask import Blueprint, render_template, jsonify, flash, redirect, url_for
from flask_login import login_required
from EcoPlot import db
from EcoPlot.models.device import Device
from EcoPlot.models.device_type import DeviceType
from EcoPlot.models.device_brand import DeviceBrand
from EcoPlot.models.user import User
from sqlalchemy.orm import joinedload
from EcoPlot.seeds.seed_devices import seed_device_types_and_brands

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/panel')
@login_required
def admin_panel():
    return render_template('admin/panel.html')

@admin_bp.route('/api/devices', methods=['GET'])
@login_required
def get_all_devices():
    """API endpoint to get all devices with related data"""
    try:
        # Eager load related objects to avoid N+1 queries
        devices = Device.query.options(
            joinedload(Device.user),
            joinedload(Device.device_type_obj),
            joinedload(Device.brand_obj)
        ).order_by(Device.created_at.desc()).all()
        
        device_data = []
        for device in devices:
            device_dict = device.to_dict()
            # Add related data
            device_dict['user'] = {
                'id': device.user.id,
                'username': device.user.username,
                'email': device.user.email
            }
            if device.device_type_obj:
                device_dict['device_type'] = {
                    'id': device.device_type_obj.id,
                    'name': device.device_type_obj.name,
                    'icon_path': device.device_type_obj.icon_path
                }
            if device.brand_obj:
                device_dict['brand'] = {
                    'id': device.brand_obj.id,
                    'name': device.brand_obj.name,
                    'logo_path': device.brand_obj.logo_path
                }
            device_data.append(device_dict)
        
        return jsonify({
            'success': True,
            'devices': device_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@admin_bp.route('/api/users', methods=['GET'])
@login_required
def get_all_users():
    """API endpoint to get all users with device counts"""
    try:
        users = User.query.all()
        user_data = []
        for user in users:
            user_dict = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'device_count': len(user.devices) if hasattr(user, 'devices') else 0,
                'created_at': user.created_at.isoformat() if user.created_at else None
            }
            user_data.append(user_dict)
        
        return jsonify({
            'success': True,
            'users': user_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@admin_bp.route('/run-seeds')
@login_required
def run_seeds():
    try:
        seed_device_types_and_brands()
        flash('Database seeded successfully!', 'success')
    except Exception as e:
        flash(f'Error seeding database: {str(e)}', 'danger')
    return redirect(url_for('admin.admin_panel'))

@admin_bp.route('/run-upgrades')
@login_required
def run_upgrades():
    try:
        # Add any database upgrade logic here
        flash('Upgrades completed successfully!', 'success')
    except Exception as e:
        flash(f'Error running upgrades: {str(e)}', 'danger')
    return redirect(url_for('admin.admin_panel'))