from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from services.db import get_user_by_email, create_user
from utils.helpers import is_valid_email, is_strong_password

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))
        
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Basic validation
        if not name or not email or not password or not confirm_password:
            flash("All fields are required.", "error")
            return render_template('register.html')
            
        if not is_valid_email(email):
            flash("Invalid email format.", "error")
            return render_template('register.html')
            
        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return render_template('register.html')
            
        is_strong, pwd_err = is_strong_password(password)
        if not is_strong:
            flash(pwd_err, "error")
            return render_template('register.html')
            
        # Hashing and duplicate checks
        pwd_hash = generate_password_hash(password)
        user_id = create_user(name, email, pwd_hash)
        
        if user_id is None:
            flash("An account with this email already exists.", "error")
            return render_template('register.html')
            
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('auth.login'))
        
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember') == 'on'
        
        if not email or not password:
            flash("Email and Password are required.", "error")
            return render_template('login.html')
            
        user = get_user_by_email(email)
        
        if user is None or not check_password_hash(user['password_hash'], password):
            flash("Invalid email or password.", "error")
            return render_template('login.html')
            
        # Configure session
        session.clear()
        session['user_id'] = user['id']
        session['user_name'] = user['name']
        session['user_email'] = user['email']
        
        if remember:
            session.permanent = True
            
        flash(f"Welcome back, {user['name']}!", "success")
        return redirect(url_for('main.dashboard'))
        
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("You have logged out successfully.", "success")
    return redirect(url_for('auth.login'))
