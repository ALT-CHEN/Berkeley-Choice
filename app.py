from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from routes.home import home_bp
from routes.about import about_bp
from routes.recommendation import recommendation_bp

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Initialize database
    db.init_app(app)
    Migrate(app, db)

    # Register Blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(about_bp)
    app.register_blueprint(recommendation_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
