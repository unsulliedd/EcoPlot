# app/models/device_brand.py
from EcoPlot import db

class DeviceBrand(db.Model):
    __tablename__ = 'device_brands'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    device_type_id = db.Column(db.Integer, db.ForeignKey('device_types.id'), nullable=False)
    logo_path = db.Column(db.String(255))
    website = db.Column(db.String(255))
    is_custom = db.Column(db.Boolean, default=False)  # True for "Other" option
    
    # Relationships
    devices = db.relationship('Device', backref='brand_obj', lazy=True)
    
    __table_args__ = (
        db.UniqueConstraint('name', 'device_type_id', name='_brand_device_type_uc'),
    )
    
    def __repr__(self):
        return f'<DeviceBrand {self.name} (Type: {self.device_type_id})>'