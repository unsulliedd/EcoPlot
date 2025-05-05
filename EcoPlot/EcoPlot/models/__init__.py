# EcoPlot/models/__init__.py

# Import all models to make them accessible from EcoPlot.models
from .device import Device
from .device_usage import DeviceUsageLog
from .device_type import DeviceType
from .device_brand import DeviceBrand
from .user import User

# Make all models available when importing EcoPlot.models
__all__ = [
    'Device',
    'DeviceUsageLog',
    'DeviceType',
    'DeviceBrand',
    'User'
]