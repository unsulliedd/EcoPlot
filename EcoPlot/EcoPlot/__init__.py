# EcoPlot/__init__.py - Add configuration classes
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import Config
from .seeds.seed_devices import seed_device_types_and_brands

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Import models
    from EcoPlot.models.user import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    from EcoPlot.routes.main import main_bp
    from EcoPlot.routes.auth import auth_bp
    from EcoPlot.routes.admin_routes import admin_bp
    from EcoPlot.routes.device_routes import devices_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp)
    app.register_blueprint(devices_bp)
       
    # Create database tables
    with app.app_context():
        db.create_all()
        # seed_device_types_and_brands # Uncomment this line to seed device types and brands
    
    return app
# Create an app instance
app = create_app()