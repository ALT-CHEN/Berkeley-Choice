from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from models import User, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        flash('Username already exists.', 'danger')
    else:
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)  # ✅ log them in immediately
        flash('Account created and logged in!', 'success')
    return redirect(url_for('home.home'))

@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        login_user(user)  # ✅ proper login
        flash('Logged in!', 'success')
    else:
        flash('Invalid credentials.', 'danger')
    return redirect(url_for('home.home'))

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()  # ✅ proper logout
    flash('Logged out.', 'info')
    return redirect(url_for('home.home'))
