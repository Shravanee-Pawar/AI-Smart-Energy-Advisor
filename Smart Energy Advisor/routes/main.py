from flask import Blueprint, render_template, redirect, url_for, request, flash, session, jsonify
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

from services.db import (
    get_user_by_id, update_user_profile, update_user_password,
    add_energy_usage, get_latest_energy_usage, get_energy_usage_history, delete_all_energy_usage
)
from models.predictor import predict_energy_usage
from utils.helpers import calculate_detailed_bill

main_bp = Blueprint('main', __name__)

def login_required(f):
    """Decorator to protect routes from unauthenticated session requests."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Authentication required. Please log in first.", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@main_bp.route('/')
def index():
    """Renders the landing page."""
    return render_template('landing.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Renders the user dashboard showing energy cards, stats, and footprint calculations."""
    user_id = session['user_id']
    user = get_user_by_id(user_id)
    latest_usage = get_latest_energy_usage(user_id)
    
    # Defaults if no logs are recorded yet
    current_units = 0.0
    rate = 8.0
    predicted_units = 0.0
    predicted_bill_val = 0.0
    carbon_footprint = 0.0
    status = "No Data Recorded"
    badge_color = "gray"
    
    if latest_usage:
        current_units = latest_usage['units_consumed']
        rate = latest_usage['rate']
        carbon_footprint = round(current_units * 0.85, 1)
        
        # Predict usage using ML model
        pred = predict_energy_usage(
            latest_usage['family_members'],
            latest_usage['house_type'],
            latest_usage['ac_hours'],
            latest_usage['fan_hours'],
            latest_usage['tv_hours'],
            latest_usage['refrigerator'],
            latest_usage['washing_machine'],
            latest_usage['cooler'],
            latest_usage['other_appliances']
        )
        predicted_units = pred['predicted_units']
        
        # Bill calculation
        bill_details = calculate_detailed_bill(predicted_units, rate)
        predicted_bill_val = bill_details['total_amount']
        
        # Assign energy efficiency badge based on usage levels
        if current_units < 200:
            status = "Excellent Eco-Saver"
            badge_color = "emerald"
        elif current_units < 500:
            status = "Moderate Consumer"
            badge_color = "blue"
        elif current_units < 800:
            status = "High Consumer"
            badge_color = "amber"
        else:
            status = "Warning: Excess Load"
            badge_color = "rose"
            
    # Calculate mock historical comparison savings
    # Baseline comparison: typical non-efficient house consumes ~850 kWh
    baseline = 850.0
    monthly_saving = max(0.0, round((baseline - current_units) * rate, 2)) if latest_usage else 0.0
    
    metrics = {
        "current_units": current_units,
        "predicted_units": predicted_units,
        "predicted_bill": predicted_bill_val,
        "status": status,
        "badge_color": badge_color,
        "monthly_saving": monthly_saving,
        "carbon_footprint": carbon_footprint,
        "rate": rate
    }
    
    return render_template('dashboard.html', user=user, metrics=metrics)

@main_bp.route('/usage', methods=['GET', 'POST'])
@login_required
def usage():
    """Allows user to enter current month units consumed, appliance draw metrics, and family specs."""
    user_id = session['user_id']
    
    if request.method == 'POST':
        units_consumed = float(request.form.get('units_consumed', 0))
        rate = float(request.form.get('rate', 8))
        family_members = int(request.form.get('family_members', 1))
        house_type = request.form.get('house_type', 'Apartment')
        
        ac_hours = float(request.form.get('ac_hours', 0))
        fan_hours = float(request.form.get('fan_hours', 0))
        tv_hours = float(request.form.get('tv_hours', 0))
        
        refrigerator = 1 if request.form.get('refrigerator') == 'on' else 0
        washing_machine = 1 if request.form.get('washing_machine') == 'on' else 0
        cooler = 1 if request.form.get('cooler') == 'on' else 0
        other_appliances = 1 if request.form.get('other_appliances') == 'on' else 0
        
        recorded_date = request.form.get('recorded_date')
        if not recorded_date:
            recorded_date = datetime.date.today().strftime("%Y-%m-%d")
            
        success = add_energy_usage(
            user_id, units_consumed, rate, family_members, house_type,
            ac_hours, fan_hours, tv_hours, refrigerator, washing_machine,
            cooler, other_appliances, recorded_date
        )
        
        if success:
            flash("Energy parameters successfully saved into database!", "success")
        else:
            flash("Failed to save energy details.", "error")
            
        return redirect(url_for('main.dashboard'))
        
    latest_usage = get_latest_energy_usage(user_id)
    return render_template('usage.html', usage=latest_usage)

@main_bp.route('/usage/reset', methods=['POST'])
@login_required
def reset_usage():
    """Deletes all energy log history for the user."""
    user_id = session['user_id']
    if delete_all_energy_usage(user_id):
        flash("All usage logs have been successfully reset.", "success")
    else:
        flash("Could not reset logs.", "error")
    return redirect(url_for('main.dashboard'))

@main_bp.route('/prediction')
@login_required
def prediction():
    """Retrieves prediction statistics generated from the Scikit-learn RandomForest model."""
    user_id = session['user_id']
    latest_usage = get_latest_energy_usage(user_id)
    
    if not latest_usage:
        flash("Please log your appliance variables on the Electricity Usage page first.", "info")
        return redirect(url_for('main.usage'))
        
    pred = predict_energy_usage(
        latest_usage['family_members'],
        latest_usage['house_type'],
        latest_usage['ac_hours'],
        latest_usage['fan_hours'],
        latest_usage['tv_hours'],
        latest_usage['refrigerator'],
        latest_usage['washing_machine'],
        latest_usage['cooler'],
        latest_usage['other_appliances']
    )
    
    return render_template('prediction.html', pred=pred, usage=latest_usage)

@main_bp.route('/bill')
@login_required
def bill():
    """Generates an estimated utility invoice based on predicted consumption."""
    user_id = session['user_id']
    latest_usage = get_latest_energy_usage(user_id)
    
    if not latest_usage:
        flash("Please log your appliance variables on the Electricity Usage page first.", "info")
        return redirect(url_for('main.usage'))
        
    pred = predict_energy_usage(
        latest_usage['family_members'],
        latest_usage['house_type'],
        latest_usage['ac_hours'],
        latest_usage['fan_hours'],
        latest_usage['tv_hours'],
        latest_usage['refrigerator'],
        latest_usage['washing_machine'],
        latest_usage['cooler'],
        latest_usage['other_appliances']
    )
    
    bill_details = calculate_detailed_bill(pred['predicted_units'], latest_usage['rate'])
    
    return render_template('bill.html', bill=bill_details, usage=latest_usage, pred=pred)

@main_bp.route('/analytics')
@login_required
def analytics():
    """Loads visual graphs using Chart.js configurations."""
    user_id = session['user_id']
    history = get_energy_usage_history(user_id)
    
    # Pre-populate sample dashboard data if user history is sparse (< 3 logs)
    # This prevents blank layouts and offers professional previews
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    sample_consumption = [450, 480, 520, 610, 780, 920, 1050, 980, 750, 580, 490, 460]
    sample_bills = [3800, 4000, 4400, 5200, 6800, 8100, 9300, 8600, 6500, 4900, 4100, 3900]
    
    if len(history) >= 3:
        # Generate custom lists from SQLite history
        custom_months = []
        custom_consumption = []
        custom_bills = []
        
        for record in history:
            # Parse recorded date to obtain Month Name
            date_obj = datetime.datetime.strptime(record['recorded_date'], "%Y-%m-%d")
            custom_months.append(date_obj.strftime("%b"))
            custom_consumption.append(record['units_consumed'])
            custom_bills.append(record['units_consumed'] * record['rate'])
            
        months = custom_months
        sample_consumption = custom_consumption
        sample_bills = custom_bills
        is_sample = False
    else:
        is_sample = True
        
    latest_usage = get_latest_energy_usage(user_id)
    appliance_shares = {"Heating & Cooling": 45, "Water Heater": 18, "Refrigeration": 15, "Lighting & Fans": 12, "Other": 10}
    
    if latest_usage:
        # Dynamically scale appliance shares based on current user inputs
        total_score = 0
        hvac_score = latest_usage['ac_hours'] * 3.0
        fans_score = latest_usage['fan_hours'] * 0.5
        ref_score = 4.0 if latest_usage['refrigerator'] else 0
        wm_score = 2.0 if latest_usage['washing_machine'] else 0
        cooler_score = 5.0 if latest_usage['cooler'] else 0
        other_score = 3.0 if latest_usage['other_appliances'] else 0
        
        total_score = hvac_score + fans_score + ref_score + wm_score + cooler_score + other_score
        
        if total_score > 0:
            appliance_shares = {
                "Heating & Cooling": round((hvac_score + cooler_score) / total_score * 100),
                "Lighting & Fans": round(fans_score / total_score * 100),
                "Refrigeration": round(ref_score / total_score * 100),
                "Laundry & Appliances": round(wm_score / total_score * 100),
                "Other Electronics": round(other_score / total_score * 100)
            }
            
    graph_data = {
        "months": months,
        "consumption": sample_consumption,
        "bills": sample_bills,
        "appliances": list(appliance_shares.keys()),
        "appliance_values": list(appliance_shares.values()),
        "is_sample": is_sample
    }
    
    return render_template('analytics.html', graph_data=graph_data)

@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Allows user to update profile details and modify account password."""
    user_id = session['user_id']
    user = get_user_by_id(user_id)
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'update_profile':
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            
            if not name or not email:
                flash("Name and Email fields are required.", "error")
                return render_template('profile.html', user=user)
                
            success = update_user_profile(user_id, name, email)
            if success:
                session['user_name'] = name
                session['user_email'] = email
                flash("Profile successfully updated!", "success")
                return redirect(url_for('main.profile'))
            else:
                flash("Email already in use by another user account.", "error")
                
        elif action == 'change_password':
            current_pwd = request.form.get('current_password', '')
            new_pwd = request.form.get('new_password', '')
            confirm_pwd = request.form.get('confirm_password', '')
            
            if not check_password_hash(user['password_hash'], current_pwd):
                flash("Incorrect current password.", "error")
                return render_template('profile.html', user=user)
                
            if new_pwd != confirm_pwd:
                flash("Confirm password does not match new password.", "error")
                return render_template('profile.html', user=user)
                
            from utils.helpers import is_strong_password
            is_strong, pwd_err = is_strong_password(new_pwd)
            if not is_strong:
                flash(pwd_err, "error")
                return render_template('profile.html', user=user)
                
            new_hash = generate_password_hash(new_pwd)
            update_user_password(user_id, new_hash)
            flash("Password updated successfully!", "success")
            return redirect(url_for('main.profile'))
            
    return render_template('profile.html', user=user)
