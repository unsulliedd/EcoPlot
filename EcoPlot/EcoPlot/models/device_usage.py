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
    is_optimal_usage = db.Column(db.Boolean, default=False)  # Was this usage during optimal time?
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<DeviceUsage {self.device_id} {self.start_time}>'