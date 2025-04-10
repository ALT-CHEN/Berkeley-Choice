
from flask import Blueprint, render_template

contact_bp = Blueprint("contact", __name__)  # Create a Blueprint for contact

@contact_bp.route("/contact")
def contact():
    return render_template("contact.html")
