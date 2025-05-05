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
    
    # Account and subscription info
    is_pro = db.Column(db.Boolean, default=False)  # Pro vs Free account
    subscription_expires = db.Column(db.DateTime)  # When pro subscription expires
    
    # Location info for weather data
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    timezone = db.Column(db.String(50))  # Important for scheduling
    address = db.Column(db.String(255))  # Full address for weather lookup
    city = db.Column(db.String(100))
    state = db.Column(db.String(50))
    country = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    
    # Home characteristics
    home_size_sqft = db.Column(db.Float)  # For energy modeling
    home_type = db.Column(db.String(50))  # apartment, house, etc.
    occupants_count = db.Column(db.Integer)  # Number of people in household
    
    # Energy production details (solar)
    has_solar = db.Column(db.Boolean, default=False)
    solar_capacity_kw = db.Column(db.Float)  # in kilowatts
    solar_panel_orientation = db.Column(db.String(20))  # e.g., "south", "southwest"
    solar_panel_tilt = db.Column(db.Float)  # in degrees
    solar_installation_date = db.Column(db.Date)  # For degradation calculations
    
    # Wind energy
    has_wind_turbine = db.Column(db.Boolean, default=False)
    wind_turbine_capacity_kw = db.Column(db.Float)
    wind_turbine_height_meters = db.Column(db.Float)
    
    # EV details
    has_ev = db.Column(db.Boolean, default=False)
    ev_battery_capacity_kwh = db.Column(db.Float)
    ev_typical_daily_usage_kwh = db.Column(db.Float)
    ev_manufacturer = db.Column(db.String(50))  # Tesla, Nissan, etc.
    ev_model = db.Column(db.String(50))
    ev_charging_preference = db.Column(db.String(50))  # "cheapest", "greenest", "fastest"
    
    # Battery storage
    has_battery_storage = db.Column(db.Boolean, default=False)
    battery_capacity_kwh = db.Column(db.Float)
    battery_brand = db.Column(db.String(50))  # Tesla Powerwall, Enphase, etc.
    
    # Utility details
    utility_provider = db.Column(db.String(100))
    electricity_rate_plan = db.Column(db.String(50))  # e.g., "time-of-use", "flat-rate"
    peak_rate_per_kwh = db.Column(db.Float)
    off_peak_rate_per_kwh = db.Column(db.Float)
    solar_feed_in_tariff = db.Column(db.Float)  # Rate for selling back to grid
    
    # User preferences
    energy_savings_goal = db.Column(db.Float)  # Target savings percentage
    environmental_priority = db.Column(db.Integer, default=5)  # 1-10 scale
    budget_constraints = db.Column(db.Float)  # Monthly energy budget
    notification_preferences = db.Column(db.String(100))  # email, push, sms
    language_preference = db.Column(db.String(10), default='en')
    
    # Integration settings
    ev_api_key = db.Column(db.String(255))  # For EV manufacturer API
    smart_home_platform = db.Column(db.String(50))  # Google Home, Alexa, etc.
    weather_api_preference = db.Column(db.String(50))  # OpenWeatherMap, etc.
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Methods
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_subscription_active(self):
        if not self.is_pro:
            return False
        if self.subscription_expires and self.subscription_expires < datetime.utcnow():
            return False
        return True
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def to_dict(self, include_private=False):
        """Convert user object to dictionary for API responses"""
        user_dict = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_pro': self.is_pro,
            'timezone': self.timezone,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
        
        if include_private:
            # Add additional fields for authenticated requests
            user_dict.update({
                'has_solar': self.has_solar,
                'has_ev': self.has_ev,
                'has_battery_storage': self.has_battery_storage,
                'home_size_sqft': self.home_size_sqft,
                'energy_savings_goal': self.energy_savings_goal
            })
        
        return user_dict