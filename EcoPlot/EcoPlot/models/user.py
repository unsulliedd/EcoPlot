# EcoPlot/models/user.py
from EcoPlot import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    
    # Location info for weather data
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    # Energy production details
    has_solar = db.Column(db.Boolean, default=False)
    solar_capacity_kw = db.Column(db.Float)  # in kilowatts
    solar_panel_orientation = db.Column(db.String(20))  # e.g., "south", "southwest"
    solar_panel_tilt = db.Column(db.Float)  # in degrees
    
    # EV details
    has_ev = db.Column(db.Boolean, default=False)
    ev_battery_capacity_kwh = db.Column(db.Float)
    ev_typical_daily_usage_kwh = db.Column(db.Float)
    
    # Battery storage
    has_battery_storage = db.Column(db.Boolean, default=False)
    battery_capacity_kwh = db.Column(db.Float)
    
    # Utility details
    electricity_rate_plan = db.Column(db.String(50))  # e.g., "time-of-use", "flat-rate"
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'