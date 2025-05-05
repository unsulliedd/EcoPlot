# EcoPlot/services/device_service.py
from EcoPlot import db
from EcoPlot.models.device_type import DeviceType
from EcoPlot.models.device_brand import DeviceBrand
from EcoPlot.models.device import Device
from flask_login import current_user

class DeviceService:
    @staticmethod
    def get_all_device_types():
        """Get all device types"""
        return DeviceType.query.all()
    
    @staticmethod
    def get_brands_by_type(device_type_id):
        """Get all brands for a specific device type"""
        return DeviceBrand.query.filter_by(device_type_id=device_type_id).all()
    
    @staticmethod
    def get_user_devices_by_type_and_brand(device_type_id, brand_id):
        """Get user's devices by type and brand"""
        return Device.query.filter_by(
            user_id=current_user.id,
            device_type_id=device_type_id,
            brand_id=brand_id
        ).all()
    
    @staticmethod
    def add_device(data):
        """Add a new device"""
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
            is_smart_device=data.get('is_smart_device', False),
            api_controllable=data.get('api_controllable', False)
        )
        db.session.add(device)
        db.session.commit()
        return device