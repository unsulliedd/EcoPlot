# app/models/device_usage.py
from EcoPlot import db
from datetime import datetime

class DeviceUsageLog(db.Model):
    __tablename__ = 'device_usage_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    energy_consumed_kwh = db.Column(db.Float)  # in kilowatt-hours
    cost = db.Column(db.Float)  # cost based on energy pricing at that time
    is_optimal_usage = db.Column(db.Boolean, default=False)  # Was this usage during optimal time?
    energy_source = db.Column(db.String(50))  # solar, grid, battery, etc.
    carbon_footprint_kg = db.Column(db.Float)  # kg of CO2 equivalent
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<DeviceUsageLog {self.device_id} {self.start_time}>'
    
    def to_dict(self):
        """Convert usage log to dictionary for API responses"""
        return {
            'id': self.id,
            'device_id': self.device_id,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'energy_consumed_kwh': self.energy_consumed_kwh,
            'cost': self.cost,
            'is_optimal_usage': self.is_optimal_usage,
            'energy_source': self.energy_source,
            'carbon_footprint_kg': self.carbon_footprint_kg
        }