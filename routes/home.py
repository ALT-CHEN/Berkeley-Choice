from flask import Blueprint, render_template

home_bp = Blueprint("home", __name__)  # Create a Blueprint

@home_bp.route("/")
def home():
    return "home page"
