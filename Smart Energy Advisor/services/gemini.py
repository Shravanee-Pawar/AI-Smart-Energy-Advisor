import os
import google.generativeai as genai

# Load Gemini API Key
api_key = os.getenv("GEMINI_API_KEY")

# Flag to trace if API is configured
_api_configured = False
if api_key and api_key.strip() and not api_key.startswith("YOUR_"):
    try:
        genai.configure(api_key=api_key.strip())
        _api_configured = True
        print("[Smart Energy Advisor] Gemini API successfully configured.")
    except Exception as e:
        print(f"[Smart Energy Advisor] Error configuring Gemini API: {e}. Falling back to Rule-Based Mock Consultant.")
else:
    print("[Smart Energy Advisor] Gemini API key not provided or placeholder used. Running in Mock Mode.")

def get_chatbot_response(user_message, history=None):
    """Retrieve conversational AI response, using Google Gemini or a rich local mockup helper."""
    global _api_configured
    
    system_instruction = (
        "You are 'Smarty', an intelligent home energy assistant. Answer user queries about saving electricity, "
        "improving appliance efficiency, understanding bills, and general conservation habits. Be helpful, concise, and professional."
    )
    
    if _api_configured:
        try:
            # Build conversation history context
            formatted_prompt = f"{system_instruction}\n\n"
            if history:
                for msg in history:
                    role = "User" if msg["role"] == "user" else "Assistant"
                    formatted_prompt += f"{role}: {msg['content']}\n"
            formatted_prompt += f"User: {user_message}\nAssistant:"
            
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(formatted_prompt)
            return response.text.strip()
        except Exception as e:
            print(f"[Smart Energy Advisor] Gemini API execution error: {e}. Triggering local fallback.")
            # Fall through to mock logic if API fails
            
    # Rich rule-based mock chat consultant
    msg_lower = user_message.lower()
    if "reduce" in msg_lower and "bill" in msg_lower:
        return (
            "To reduce your electricity bill immediately, focus on these top areas:\n\n"
            "1. **Thermostat management**: Every degree you raise your thermostat in summer (or lower in winter) saves about 3% on cooling/heating costs.\n"
            "2. **Phantom load**: Unplug computers, game consoles, and chargers when not in use. They draw 'standby' power.\n"
            "3. **Lighting**: Swap traditional incandescent bulbs with LEDs. They use 75% less energy.\n"
            "4. **Washing schedules**: Wash clothes in cold water and run your dishwasher only with full loads."
        )
    elif "ac" in msg_lower or "air condition" in msg_lower:
        return (
            "Air Conditioning represents the single largest electricity load in most homes. Here is how to optimize it:\n\n"
            "• **The 78°F Rule**: Keep your AC set at 78°F (25°C) or higher when home. Use ceiling fans to create a wind-chill effect.\n"
            "• **Filter Check**: Clean or replace AC filters every 30 days. Dirty filters make the compressor work 15% harder.\n"
            "• **Seal Drafts**: Check doors and windows for air leaks. Draft seals keep the cool air in and heat out.\n"
            "• **Smart Thermostats**: Install a programmable thermostat to automatically raise the temperature when you are away."
        )
    elif "appliance" in msg_lower:
        return (
            "When evaluating home appliances for energy efficiency:\n\n"
            "1. Look for the **ENERGY STAR®** label. Certified models use 10% to 50% less energy than standard ones.\n"
            "2. **Refrigerators**: Clean condenser coils twice a year. Keep it stocked (thermal mass helps maintain temperature), but do not overcrowd it.\n"
            "3. **Water Heaters**: Electric water heaters are heavy draws. Set the thermostat to 120°F (49°C) instead of 140°F.\n"
            "4. **Dryers**: Clean the lint trap after every load and ensure external exhaust vents are unblocked."
        )
    elif "increase" in msg_lower or "increasing" in msg_lower or "high" in msg_lower:
        return (
            "If your electricity bill is unexpectedly rising, investigate these common culprits:\n\n"
            "• **Seasonal changes**: Extreme hot or cold weather forces HVAC systems to cycle frequently.\n"
            "• **Appliance degradation**: Older refrigerators or AC compressors draw more current as they wear down.\n"
            "• **Phantom draw**: Additional game consoles, chargers, or home server units left running 24/7.\n"
            "• **Tiered billing tariffs**: Consuming past a certain kWh threshold triggers higher utility rates per unit."
        )
    else:
        return (
            "Hello! I am your AI Energy Assistant. You can ask me how to save power on AC, which energy-saving "
            "appliances to buy, or why your monthly bill might be rising. How can I help you conserve energy today?"
        )

def get_energy_recommendations(usage_data, predicted_units, predicted_bill):
    """Generate structured energy recommendations using Gemini or local rules."""
    global _api_configured
    
    prompt = f"""You are an expert Energy Consultant.
Based on the user's electricity consumption, predicted bill, appliance usage, and household information, provide personalized energy-saving recommendations.

Household details:
- Current Monthly Units: {usage_data.get('units_consumed', 0)} kWh
- Predicted Next Month Units: {predicted_units} kWh
- Cost Per Unit: {usage_data.get('rate', 0)} units
- Estimated Next Month Bill: ₹{predicted_bill:.2f}
- Family Size: {usage_data.get('family_members', 1)}
- House Type: {usage_data.get('house_type', 'Apartment')}
- AC Hours/Day: {usage_data.get('ac_hours', 0)} hrs
- Fan Hours/Day: {usage_data.get('fan_hours', 0)} hrs
- Refrigerator: {'Yes' if usage_data.get('refrigerator') else 'No'}
- Washing Machine: {'Yes' if usage_data.get('washing_machine') else 'No'}
- Cooler: {'Yes' if usage_data.get('cooler') else 'No'}
- Other Appliances: {'Yes' if usage_data.get('other_appliances') else 'No'}

Suggest:
Top 10 recommendations
Expected monthly savings (in ₹)
Estimated yearly savings (in ₹)
Carbon footprint reduction (in lbs of CO2, using 0.85 lbs CO2 per kWh saved)
Priority level (High, Medium, Low)

Keep responses simple, actionable, and formatted clearly.
"""

    if _api_configured:
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"[Smart Energy Advisor] Gemini API recommendation error: {e}. Generating local fallback recommendations.")
            # Fall through to local fallback

    # Highly structured mock recommendations markdown response
    ac_hours = usage_data.get('ac_hours', 0)
    has_cooler = usage_data.get('cooler')
    
    # Customize recommendations based on usage
    ac_tip = ""
    if ac_hours > 5:
        ac_tip = (
            "### 1. Optimize AC Thermostat Settings 🌡️\n"
            "**Description:** Raise the AC temperature to 78°F (25°C). Use ceiling fans to distribute cool air.\n"
            "**Expected Monthly Savings:** ₹1,200\n"
            "**Estimated Yearly Savings:** ₹14,400\n"
            "**Carbon Footprint Reduction:** 120 lbs CO2\n"
            "**Priority Level:** High\n\n"
        )
    else:
        ac_tip = (
            "### 1. Clean AC Filter regularly 🧹\n"
            "**Description:** Clean the air conditioning filter every 2-4 weeks to improve airflow and efficiency.\n"
            "**Expected Monthly Savings:** ₹300\n"
            "**Estimated Yearly Savings:** ₹3,600\n"
            "**Carbon Footprint Reduction:** 30 lbs CO2\n"
            "**Priority Level:** Medium\n\n"
        )

    recommendations_md = f"""# Personalized Energy Consultant Report

Here are your top 10 customized recommendations based on your appliance logs and house details:

{ac_tip}### 2. Transition to LED Bulbs 💡
**Description:** Replace all remaining incandescent and CFL bulbs with ENERGY STAR certified LED bulbs.
**Expected Monthly Savings:** ₹350
**Estimated Yearly Savings:** ₹4,200
**Carbon Footprint Reduction:** 40 lbs CO2
**Priority Level:** High

### 3. Tackle Phantom Power Load 🔌
**Description:** Unplug standby entertainment consoles, chargers, and desktop units or plug them into smart power strips.
**Expected Monthly Savings:** ₹250
**Estimated Yearly Savings:** ₹3,000
**Carbon Footprint Reduction:** 30 lbs CO2
**Priority Level:** Medium

### 4. Cold Water Washing Machine Loads 🧺
**Description:** Wash your laundry using cold water settings and hang-dry clothes outdoors.
**Expected Monthly Savings:** ₹400
**Estimated Yearly Savings:** ₹4,800
**Carbon Footprint Reduction:** 45 lbs CO2
**Priority Level:** Medium

### 5. Water Heater Thermostat Calibration 🚿
**Description:** Lower your electric water heater's maximum temperature setting from 140°F to 120°F.
**Expected Monthly Savings:** ₹600
**Estimated Yearly Savings:** ₹7,200
**Carbon Footprint Reduction:** 70 lbs CO2
**Priority Level:** High

{"### 6. Swap Cooler Pads & Clear Vents ❄️" if has_cooler else "### 6. Install Window Film / Blinds ☀️"}
**Description:** {"Replace evaporative cooler grass pads with high-efficiency honeycomb pads." if has_cooler else "Install reflective window films or thermal blinds to block direct solar heating."}
**Expected Monthly Savings:** ₹280
**Estimated Yearly Savings:** ₹3,360
**Carbon Footprint Reduction:** 28 lbs CO2
**Priority Level:** Medium

### 7. Refrigerator Coil Cleaning ❄️
**Description:** Pull out the refrigerator and vacuum dust off the condenser coils at the back.
**Expected Monthly Savings:** ₹150
**Estimated Yearly Savings:** ₹1,800
**Carbon Footprint Reduction:** 15 lbs CO2
**Priority Level:** Low

### 8. Run Large Loads Only 🍽️
**Description:** Run dishwashers and washing machines only when they are fully loaded.
**Expected Monthly Savings:** ₹200
**Estimated Yearly Savings:** ₹2,400
**Carbon Footprint Reduction:** 20 lbs CO2
**Priority Level:** Low

### 9. Optimize Natural Ventilation 🍃
**Description:** Open windows during cool evenings and close thermal curtains during peak sunny hours.
**Expected Monthly Savings:** ₹300
**Estimated Yearly Savings:** ₹3,600
**Carbon Footprint Reduction:** 32 lbs CO2
**Priority Level:** Medium

### 10. Switch Off Unused Ceiling Fans 🌀
**Description:** Turn off fans in unoccupied rooms. Remember: fans cool people, not rooms.
**Expected Monthly Savings:** ₹180
**Estimated Yearly Savings:** ₹2,160
**Carbon Footprint Reduction:** 18 lbs CO2
**Priority Level:** Low
"""
    return recommendations_md
