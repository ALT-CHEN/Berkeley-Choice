from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Route blueprints
from routes.home import home_bp
from routes.about import about_bp
from routes.recommendation import recommendation_bp
from routes.contact import contact_bp
from routes.auth import auth_bp  # ✅ NEW

from flask_login import LoginManager
from models.user import User  # Adjust path if User is in models/user.py

# Database
from models import db  # ✅ From models/__init__.py

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Initialize database
    db.init_app(app)
    Migrate(app, db)

    # ✅ Initialize login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth_bp.login'  # name of your login route
    login_manager.init_app(app)

    # ✅ Provide user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(about_bp)
    app.register_blueprint(recommendation_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(auth_bp)  # ✅ Register auth routes

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
