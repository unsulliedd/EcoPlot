# EcoPlot/routes/main.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from EcoPlot.models.device import Device
from EcoPlot import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    user_devices = current_user.devices if hasattr(current_user, 'devices') else []
    return render_template('dashboard.html', devices=user_devices)

@main_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@main_bp.route('/settings')
def settings():
    return render_template('settings.html')

@main_bp.route('/devices_page')
@login_required
def devices_page():
    user_devices = current_user.devices if hasattr(current_user, 'devices') else []
    return render_template('devices.html', devices=user_devices)

@main_bp.route('/add_device', methods=['POST'])
@login_required
def add_device():
    name = request.form.get('name')
    device_type = request.form.get('device_type')
    brand = request.form.get('brand')
    model = request.form.get('model')
    power_consumption_watts = request.form.get('power_consumption_watts')
    is_smart_device = request.form.get('is_smart_device') == 'True'

    new_device = Device(
        user_id=current_user.id,
        name=name,
        device_type=device_type,
        brand=brand,
        model=model,
        power_consumption_watts=power_consumption_watts,
        is_smart_device=is_smart_device
    )
    db.session.add(new_device)
    db.session.commit()
    flash('Cihaz başarıyla eklendi!', 'success')
    return redirect(url_for('main.devices_page'))