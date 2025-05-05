# app/models/device_type.py
from EcoPlot import db

class DeviceType(db.Model):
    __tablename__ = 'device_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    icon_path = db.Column(db.String(255))
    
    # Relationships
    devices = db.relationship('Device', backref='device_type_obj', lazy=True)
    brands = db.relationship('DeviceBrand', backref='device_type_obj', lazy=True)
    
    def __repr__(self):
        return f'<DeviceType {self.name}>'