import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import config

# Initialize extensions but do not configure them yet
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'  # The route for the login page
login.login_message = 'Please log in to access this page.'
login.login_message_category = 'info'

def create_app(config_name='default'):
    """
    Application factory function.
    Configures and returns the Flask application instance.
    """
    app = Flask(__name__, instance_relative_config=True)

    # Load configuration from the specified config object
    app.config.from_object(config[config_name])

    # Ensure the instance folder exists for sqlite db etc.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize extensions with the app instance
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    # --- Register Blueprints ---
    from app.routes.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Admin blueprint (will be created later)
    # from app.routes.admin import bp as admin_bp
    # app.register_blueprint(admin_bp, url_prefix='/admin')

    # Cashier blueprint (will be created later)
    # from app.routes.cashier import bp as cashier_bp
    # app.register_blueprint(cashier_bp, url_prefix='/cashier')

    # Customer blueprint (will be created later)
    # from app.routes.customer import bp as customer_bp
    # app.register_blueprint(customer_bp, url_prefix='/customer')

    # API blueprint (will be created later)
    # from app.routes.api import bp as api_bp
    # app.register_blueprint(api_bp, url_prefix='/api')

    # --- Import models after db is initialized and before it's used ---
    # This is crucial for Flask-Migrate to detect the models.
    from app import models
    from datetime import datetime

    @app.context_processor
    def inject_year():
        """Inject the current year into all templates."""
        return {'year': datetime.utcnow().year}

    return app
