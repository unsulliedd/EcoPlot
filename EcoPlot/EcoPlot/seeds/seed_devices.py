# EcoPlot/seeds/seed_devices.py
def seed_device_types_and_brands():
    """Seed the database with common device types and brands"""
    from EcoPlot import db  # Import inside function to avoid circular imports
    from EcoPlot.models import DeviceType, DeviceBrand
    
    # Clear existing data
    db.session.query(DeviceBrand).delete()
    db.session.query(DeviceType).delete()
    
    # Create device types
    device_types = [
        {"name": "Refrigerator", "description": "Kitchen refrigeration appliance", "icon_path": "/static/icons/refrigerator.png"},
        {"name": "Dishwasher", "description": "Automatic dish washing machine", "icon_path": "/static/icons/dishwasher.png"},
        {"name": "Washing Machine", "description": "Clothes washing appliance", "icon_path": "/static/icons/washing_machine.png"},
        {"name": "Dryer", "description": "Clothes drying appliance", "icon_path": "/static/icons/dryer.png"},
        {"name": "HVAC", "description": "Heating, ventilation, and air conditioning", "icon_path": "/static/icons/hvac.png"},
        {"name": "Water Heater", "description": "Water heating appliance", "icon_path": "/static/icons/water_heater.png"},
        {"name": "EV Charger", "description": "Electric vehicle charging station", "icon_path": "/static/icons/ev_charger.png"},
        {"name": "Lighting", "description": "Home lighting systems", "icon_path": "/static/icons/lighting.png"},
        {"name": "Television", "description": "Home entertainment display", "icon_path": "/static/icons/tv.png"},
        {"name": "Computer", "description": "Personal computing device", "icon_path": "/static/icons/computer.png"},
        {"name": "Small Kitchen Appliance", "description": "Small kitchen appliances like toasters, blenders", "icon_path": "/static/icons/small_appliance.png"},
        {"name": "Smart Speaker", "description": "Voice-controlled speaker with virtual assistant", "icon_path": "/static/icons/smart_speaker.png"},
        {"name": "Pool Pump", "description": "Swimming pool water circulation", "icon_path": "/static/icons/pool_pump.png"},
        {"name": "Other", "description": "Other device types", "icon_path": "/static/icons/other.png"},
    ]
    
    type_objects = {}
    for type_data in device_types:
        device_type = DeviceType(**type_data)
        db.session.add(device_type)
        db.session.flush()  # To get the ID
        type_objects[device_type.name] = device_type
    
    # Define brands for each device type
    brands_by_type = {
        "Refrigerator": ["Samsung", "LG", "Whirlpool", "GE", "Bosch", "Electrolux", "Haier", "Frigidaire", "Other"],
        "Dishwasher": ["Bosch", "Whirlpool", "Miele", "GE", "LG", "Samsung", "Maytag", "KitchenAid", "Other"],
        "Washing Machine": ["LG", "Samsung", "Whirlpool", "Bosch", "Electrolux", "Maytag", "GE", "Speed Queen", "Other"],
        "Dryer": ["LG", "Samsung", "Whirlpool", "Bosch", "Electrolux", "Maytag", "GE", "Speed Queen", "Other"],
        "HVAC": ["Carrier", "Trane", "Lennox", "Rheem", "Goodman", "Bryant", "York", "Amana", "Daikin", "Other"],
        "Water Heater": ["Rheem", "A.O. Smith", "Bradford White", "Rinnai", "Navien", "Noritz", "EcoSmart", "Other"],
        "EV Charger": ["Tesla", "ChargePoint", "Electrify America", "EVBox", "Blink", "Wallbox", "JuiceBox", "Other"],
        "Lighting": ["Philips Hue", "LIFX", "Nanoleaf", "Sengled", "GE", "Sylvania", "Wyze", "Cree", "Other"],
        "Television": ["Samsung", "LG", "Sony", "TCL", "Vizio", "Hisense", "Panasonic", "Other"],
        "Computer": ["Apple", "Dell", "HP", "Lenovo", "Asus", "Acer", "Microsoft", "Other"],
        "Small Kitchen Appliance": ["KitchenAid", "Cuisinart", "Breville", "Ninja", "Hamilton Beach", "Oster", "Other"],
        "Smart Speaker": ["Amazon", "Google", "Apple", "Sonos", "Bose", "JBL", "Other"],
        "Pool Pump": ["Hayward", "Pentair", "Jandy", "Sta-Rite", "Intex", "Other"],
        "Other": ["Other"]
    }
    
    # Create brands
    for device_type_name, brands in brands_by_type.items():
        device_type = type_objects[device_type_name]
        for brand_name in brands:
            is_custom = (brand_name == "Other")
            logo_path = f"/static/logos/{brand_name.lower().replace(' ', '_')}.png" if not is_custom else "/static/logos/other.png"
            
            brand = DeviceBrand(
                name=brand_name,
                device_type_id=device_type.id,
                logo_path=logo_path,
                is_custom=is_custom
            )
            db.session.add(brand)
    
    # Commit all changes
    db.session.commit()
    print("Successfully seeded device types and brands!")