from flask import Blueprint

# Create a Blueprint named 'main'
main_bp = Blueprint('main', __name__)

# Import routes that use this Blueprint
from . import device_routes