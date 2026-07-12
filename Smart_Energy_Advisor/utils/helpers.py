import re

def is_valid_email(email):
    """Validate email address format using regular expressions."""
    if not email:
        return False
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(email_regex, email.strip()))

def is_strong_password(password):
    """Verify if a password meets complexity rules.
    - At least 8 characters
    - Contains an uppercase letter
    - Contains a lowercase letter
    - Contains a numeric digit
    - Contains a special symbol (!@#$%^&* etc.)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number."
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character (!@#$%^&* etc.)."
    return True, ""

def calculate_detailed_bill(units, rate_per_unit):
    """Calculate utility bill parameters including fixed charges, GST, and totals."""
    # Standard rates
    fixed_charge = 150.0  # ₹ Fixed grid line charge
    
    # Cost calculation
    energy_cost = units * rate_per_unit
    
    # Taxes
    gst = round(energy_cost * 0.18, 2)  # 18% GST on energy
    
    total_amount = round(fixed_charge + energy_cost + gst, 2)
    
    return {
        "units": round(units, 1),
        "rate": round(rate_per_unit, 2),
        "fixed_charges": fixed_charge,
        "gst": gst,
        "total_amount": total_amount
    }
