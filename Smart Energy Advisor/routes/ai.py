from flask import Blueprint, render_template, redirect, url_for, request, flash, session, jsonify
import re
from routes.main import login_required
from services.db import get_latest_energy_usage
from models.predictor import predict_energy_usage
from utils.helpers import calculate_detailed_bill
from services.gemini import get_chatbot_response, get_energy_recommendations

ai_bp = Blueprint('ai', __name__)

def parse_recommendations_to_list(text):
    """RegEx parser to translate raw advisor markdown output into structured cards."""
    # Pattern matching: Title, Description, Monthly Savings, Yearly Savings, CO2, Priority
    pattern = (
        r'###\s+\d+\.\s+([^\n]+)\n'
        r'\*\*Description:\*\*\s*([^\n]+)\n'
        r'\*\*Expected Monthly Savings:\*\*\s*([^\n]+)\n'
        r'\*\*Estimated Yearly Savings:\*\*\s*([^\n]+)\n'
        r'\*\*Carbon Footprint Reduction:\*\*\s*([^\n]+)\n'
        r'\*\*Priority Level:\*\*\s*([^\n]+)'
    )
    
    matches = re.findall(pattern, text)
    
    recs = []
    for match in matches:
        recs.append({
            "title": match[0].strip(),
            "description": match[1].strip(),
            "monthly_savings": match[2].strip(),
            "yearly_savings": match[3].strip(),
            "co2_reduction": match[4].strip(),
            "priority": match[5].strip()
        })
        
    # If the parser yields nothing due to formatting differences, provide a structured fallback list
    if not recs:
        # Fallback to scanning lines for keywords to extract sections
        sections = text.split("###")
        for sec in sections[1:]:
            lines = sec.strip().split("\n")
            if not lines:
                continue
            title = lines[0].strip()
            desc = ""
            m_savings = "N/A"
            y_savings = "N/A"
            co2 = "N/A"
            priority = "Medium"
            
            for line in lines[1:]:
                if "Description:" in line:
                    desc = line.replace("**Description:**", "").strip()
                elif "Monthly Savings:" in line:
                    m_savings = line.replace("**Expected Monthly Savings:**", "").strip()
                elif "Yearly Savings:" in line:
                    y_savings = line.replace("**Estimated Yearly Savings:**", "").strip()
                elif "Carbon Footprint" in line or "CO2" in line:
                    co2 = line.replace("**Carbon Footprint Reduction:**", "").strip()
                elif "Priority" in line:
                    priority = line.replace("**Priority Level:**", "").strip()
            
            if title and desc:
                recs.append({
                    "title": title,
                    "description": desc,
                    "monthly_savings": m_savings,
                    "yearly_savings": y_savings,
                    "co2_reduction": co2,
                    "priority": priority
                })
                
    return recs

@ai_bp.route('/ai-assistant', methods=['GET', 'POST'])
@login_required
def assistant():
    """Manages the AI Assistant chat page and handles async AJAX queries."""
    if request.method == 'POST':
        data = request.get_json() or {}
        user_message = data.get('message', '').strip()
        history = data.get('history', [])
        
        if not user_message:
            return jsonify({"response": "I didn't receive any message. How can I assist you today?"}), 400
            
        chatbot_reply = get_chatbot_response(user_message, history)
        return jsonify({"response": chatbot_reply})
        
    return render_template('ai_assistant.html')

@ai_bp.route('/recommendations')
@login_required
def recommendations():
    """Generates and displays structured AI recommendations based on user parameters."""
    user_id = session['user_id']
    latest_usage = get_latest_energy_usage(user_id)
    
    if not latest_usage:
        flash("Please log your appliance variables on the Electricity Usage page first.", "info")
        return redirect(url_for('main.usage'))
        
    # Get predictions
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
    bill_details = calculate_detailed_bill(predicted_units, latest_usage['rate'])
    predicted_bill_val = bill_details['total_amount']
    
    # Generate report
    report_markdown = get_energy_recommendations(latest_usage, predicted_units, predicted_bill_val)
    recommendations_list = parse_recommendations_to_list(report_markdown)
    
    return render_template('recommendations.html', recommendations=recommendations_list)
