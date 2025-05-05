# app/models/device.py
from EcoPlot import db
from datetime import datetime, timezone

class Device(db.Model):
    __tablename__ = 'devices'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    
    # Foreign keys for relationships
    device_type_id = db.Column(db.Integer, db.ForeignKey('device_types.id'), nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey('device_brands.id'), nullable=False)
    model = db.Column(db.String(100))
    
    # Device image
    image_path = db.Column(db.String(255))
    
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
    ev_battery_capacity_kwh = db.Column(db.Float)
    charging_rate_kw = db.Column(db.Float)
    
    # Smart device integration
    is_smart_device = db.Column(db.Boolean, default=False)
    api_controllable = db.Column(db.Boolean, default=False)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships (no backrefs because they're already in DeviceBrand and DeviceType)
    user = db.relationship('User', backref=db.backref('devices', lazy=True))
    usage_logs = db.relationship('DeviceUsageLog', backref='device', lazy=True)
    
    def __repr__(self):
        return f'<Device {self.name} ({self.device_type_obj.name})>'
    
    def to_dict(self):
        """Convert device object to dictionary for API responses"""
        return {
            'id': self.id,
            'name': self.name,
            'device_type': {
                'id': self.device_type_obj.id,
                'name': self.device_type_obj.name,
                'icon_path': self.device_type_obj.icon_path
            },
            'brand': {
                'id': self.brand_obj.id,
                'name': self.brand_obj.name,
                'logo_path': self.brand_obj.logo_path
            },
            'model': self.model,
            'image_path': self.image_path,
            'power_consumption_watts': self.power_consumption_watts,
            'standby_power_watts': self.standby_power_watts,
            'average_usage_hours_per_day': self.average_usage_hours_per_day,
            'usage_flexibility': self.usage_flexibility,
            'priority_level': self.priority_level,
            'is_schedulable': self.is_schedulable,
            'is_ev_charger': self.is_ev_charger,
            'is_smart_device': self.is_smart_device,
            'api_controllable': self.api_controllable,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }