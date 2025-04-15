from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models to register with SQLAlchemy
from models.user import User


from . import skill_predictor
