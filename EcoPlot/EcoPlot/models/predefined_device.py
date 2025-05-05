# app/models/predefined_device.py
from EcoPlot import db

class PredefinedDevice(db.Model):
    __tablename__ = 'predefined_devices'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    device_type_id = db.Column(db.Integer, db.ForeignKey('device_types.id'), nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey('device_brands.id'), nullable=False)
    model = db.Column(db.String(100))
    image_path = db.Column(db.String(255), nullable=False)
    
    # Default power specifications
    power_consumption_watts = db.Column(db.Float, nullable=False)
    standby_power_watts = db.Column(db.Float, default=0.0)
    
    # Default settings
    average_usage_hours_per_day = db.Column(db.Float)
    usage_flexibility = db.Column(db.Integer, default=0)
    priority_level = db.Column(db.Integer, default=5)
    is_schedulable = db.Column(db.Boolean, default=False)
    is_ev_charger = db.Column(db.Boolean, default=False)
    is_smart_device = db.Column(db.Boolean, default=False)
    api_controllable = db.Column(db.Boolean, default=False)
    
    # Additional information
    description = db.Column(db.Text)
    energy_saving_tips = db.Column(db.Text)
    
    # Relationships
    devices = db.relationship('Device', backref='predefined_template', lazy=True)
    
    def __repr__(self):
        return f'<PredefinedDevice {self.name} ({self.model})>'