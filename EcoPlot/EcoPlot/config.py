# EcoPlot/config.py
import os
from datetime import timedelta

# Get the directory of the current file (config.py)
basedir = os.path.abspath(os.path.dirname(__file__))

# Create a data directory if it doesn't exist
data_dir = os.path.join(basedir, 'data')
os.makedirs(data_dir, exist_ok=True)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-for-hackathon'
    # Put the database file in the data directory
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(data_dir, 'ecoplot.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REMEMBER_COOKIE_DURATION = timedelta(days=30)
    # Gemini API config
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY') or 'API_KEY_HERE'