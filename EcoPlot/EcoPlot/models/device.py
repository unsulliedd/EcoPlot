# EcoPlot/models/device.py
from EcoPlot import db
from datetime import datetime

class Device(db.Model):
    __tablename__ = 'devices'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    device_type_id = db.Column(db.Integer, db.ForeignKey('device_types.id'), nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey('device_brands.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100))
    
    # Power consumption details
    power_consumption_watts = db.Column(db.Float, nullable=False)  # in watts
    standby_power_watts = db.Column(db.Float, default=0.0)  # standby power in watts
    
    # Usage patterns
    average_usage_hours_per_day = db.Column(db.Float)
    usage_flexibility = db.Column(db.Integer, default=0)  # 0-10 scale (0=inflexible, 10=very flexible)
    priority_level = db.Column(db.Integer, default=5)  # 1-10 scale for optimization priority
    
    # For schedulable devices
    is_schedulable = db.Column(db.Boolean, default=False)
    preferred_start_time = db.Column(db.Time)
    preferred_end_time = db.Column(db.Time)
    operation_duration_minutes = db.Column(db.Integer)
    
    # For EV charging
    is_ev_charger = db.Column(db.Boolean, default=False)
    ev_battery_capacity_kwh = db.Column(db.Float)  # if it's an EV charger
    charging_rate_kw = db.Column(db.Float)  # charging rate in kW
    
    # Smart device integration
    is_smart_device = db.Column(db.Boolean, default=False)
    api_controllable = db.Column(db.Boolean, default=False)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('devices', lazy=True))
    usage_logs = db.relationship('DeviceUsageLog', backref='device', lazy=True)
    
    def __repr__(self):
        return f'<Device {self.name} ({self.device_type_id})>'
    
    def to_dict(self):
        """Convert device object to dictionary for API responses"""
        return {
            'id': self.id,
            'name': self.name,
            'device_type_id': self.device_type_id,
            'brand_id': self.brand_id,
            'model': self.model,
            'power_consumption_watts': self.power_consumption_watts,
            'standby_power_watts': self.standby_power_watts,
            'average_usage_hours_per_day': self.average_usage_hours_per_day,
            'usage_flexibility': self.usage_flexibility,
            'priority_level': self.priority_level,
            'is_schedulable': self.is_schedulable,
            'preferred_start_time': self.preferred_start_time.strftime('%H:%M') if self.preferred_start_time else None,
            'preferred_end_time': self.preferred_end_time.strftime('%H:%M') if self.preferred_end_time else None,
            'operation_duration_minutes': self.operation_duration_minutes,
            'is_ev_charger': self.is_ev_charger,
            'ev_battery_capacity_kwh': self.ev_battery_capacity_kwh,
            'charging_rate_kw': self.charging_rate_kw,
            'is_smart_device': self.is_smart_device,
            'api_controllable': self.api_controllable,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }