# EcoPlot/forms/profile.py
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, IntegerField, SelectField, SubmitField, DateField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange

class ProfileForm(FlaskForm):
    # Location Information
    address = StringField('Address', validators=[Length(max=255)])
    city = StringField('City', validators=[Length(max=100)])
    state = StringField('State/Province', validators=[Length(max=50)])
    country = StringField('Country', validators=[Length(max=100)])
    postal_code = StringField('Postal Code', validators=[Length(max=20)])
    latitude = FloatField('Latitude', validators=[Optional(), NumberRange(min=-90, max=90)])
    longitude = FloatField('Longitude', validators=[Optional(), NumberRange(min=-180, max=180)])
    timezone = StringField('Timezone', validators=[Length(max=50)])
    
    # Home characteristics
    home_size_sqft = FloatField('Home Size (sq ft)', validators=[Optional()])
    home_type = SelectField('Home Type', choices=[
        ('', 'Select home type'),
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('townhouse', 'Townhouse'),
        ('condo', 'Condominium'),
        ('mobile', 'Mobile Home'),
        ('other', 'Other')
    ], validators=[Optional()])
    occupants_count = IntegerField('Number of Occupants', validators=[Optional(), NumberRange(min=1)])
    
    # Energy production (solar)
    has_solar = BooleanField('I have solar panels')
    solar_capacity_kw = FloatField('Solar Capacity (kW)', validators=[Optional()])
    solar_panel_orientation = SelectField('Panel Orientation', choices=[
        ('', 'Select orientation'),
        ('north', 'North'),
        ('northeast', 'Northeast'),
        ('east', 'East'),
        ('southeast', 'Southeast'),
        ('south', 'South'),
        ('southwest', 'Southwest'),
        ('west', 'West'),
        ('northwest', 'Northwest')
    ], validators=[Optional()])
    solar_panel_tilt = FloatField('Panel Tilt (degrees)', validators=[Optional(), NumberRange(min=0, max=90)])
    solar_installation_date = DateField('Installation Date', format='%Y-%m-%d', validators=[Optional()])
    
    # Wind energy
    has_wind_turbine = BooleanField('I have a wind turbine')
    wind_turbine_capacity_kw = FloatField('Wind Turbine Capacity (kW)', validators=[Optional()])
    wind_turbine_height_meters = FloatField('Wind Turbine Height (meters)', validators=[Optional()])
    
    # EV details
    has_ev = BooleanField('I have an electric vehicle')
    ev_manufacturer = StringField('EV Manufacturer', validators=[Length(max=50)])
    ev_model = StringField('EV Model', validators=[Length(max=50)])
    ev_battery_capacity_kwh = FloatField('Battery Capacity (kWh)', validators=[Optional()])
    ev_typical_daily_usage_kwh = FloatField('Typical Daily Usage (kWh)', validators=[Optional()])
    ev_charging_preference = SelectField('Charging Preference', choices=[
        ('', 'Select preference'),
        ('cheapest', 'Lowest Cost'),
        ('greenest', 'Most Environmentally Friendly'),
        ('fastest', 'Fastest Charging')
    ], validators=[Optional()])
    
    # Battery storage
    has_battery_storage = BooleanField('I have home battery storage')
    battery_capacity_kwh = FloatField('Battery Capacity (kWh)', validators=[Optional()])
    battery_brand = StringField('Battery Brand', validators=[Length(max=50)])
    
    # Utility details
    utility_provider = StringField('Utility Provider', validators=[Length(max=100)])
    electricity_rate_plan = SelectField('Rate Plan', choices=[
        ('', 'Select rate plan'),
        ('flat', 'Flat Rate'),
        ('tou', 'Time-of-Use'),
        ('tiered', 'Tiered Rate'),
        ('demand', 'Demand Charges'),
        ('other', 'Other')
    ], validators=[Optional()])
    peak_rate_per_kwh = FloatField('Peak Rate ($/kWh)', validators=[Optional()])
    off_peak_rate_per_kwh = FloatField('Off-Peak Rate ($/kWh)', validators=[Optional()])
    solar_feed_in_tariff = FloatField('Solar Feed-in Tariff ($/kWh)', validators=[Optional()])
    
    # User preferences
    energy_savings_goal = IntegerField('Energy Savings Goal (%)', validators=[Optional(), NumberRange(min=0, max=100)])
    environmental_priority = IntegerField('Environmental Priority (1-10)', validators=[Optional(), NumberRange(min=1, max=10)])
    budget_constraints = FloatField('Monthly Energy Budget ($)', validators=[Optional()])
    notification_preferences = SelectField('Notification Preferences', choices=[
        ('email', 'Email Only'),
        ('push', 'Push Notifications Only'),
        ('sms', 'SMS Only'),
        ('email,push', 'Email and Push'),
        ('email,sms', 'Email and SMS'),
        ('push,sms', 'Push and SMS'),
        ('email,push,sms', 'All (Email, Push, SMS)')
    ], validators=[Optional()])
    language_preference = SelectField('Language', choices=[
        ('en', 'English'),
        ('es', 'Espanol'),
        ('fr', 'Francais'),
        ('de', 'Deutsch'),
    ], default='en')
    
    # Smart home integration
    smart_home_platform = SelectField('Smart Home Platform', choices=[
        ('', 'None'),
        ('google', 'Google Home'),
        ('alexa', 'Amazon Alexa'),
        ('homekit', 'Apple HomeKit'),
        ('smartthings', 'Samsung SmartThings'),
        ('other', 'Other')
    ], validators=[Optional()])
    
    # Weather API preference
    weather_api_preference = SelectField('Weather Data Source', choices=[
        ('', 'Default'),
        ('openweathermap', 'OpenWeatherMap'),
        ('weatherapi', 'WeatherAPI'),
        ('accuweather', 'AccuWeather'),
        ('noaa', 'NOAA'),
        ('other', 'Other')
    ], validators=[Optional()])
    
    submit = SubmitField('Save Profile')