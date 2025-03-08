from flask import Blueprint, render_template, request

recommendation_bp = Blueprint("recommendation", __name__)

@recommendation_bp.route("/recommend", methods=["GET", "POST"])
def recommend():
    return "recommendation page"
