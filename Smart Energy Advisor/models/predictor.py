import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import datetime

# Global model variables
_model = None
_r2_score = 0.85  # Default fallback R² score

HOUSE_TYPE_MAP = {
    "Apartment": 0,
    "Independent House": 1,
    "Villa": 2
}

def generate_synthetic_data(num_samples=250):
    """Generate a realistic synthetic energy usage dataset for training the ML model."""
    np.random.seed(42)
    
    # Generate random features
    family_members = np.random.randint(1, 7, size=num_samples)
    ac_hours = np.random.uniform(0, 16, size=num_samples)
    fan_hours = np.random.uniform(2, 24, size=num_samples)
    tv_hours = np.random.uniform(0, 8, size=num_samples)
    
    refrigerator = np.random.choice([0, 1], size=num_samples, p=[0.1, 0.9])
    washing_machine = np.random.choice([0, 1], size=num_samples, p=[0.3, 0.7])
    cooler = np.random.choice([0, 1], size=num_samples, p=[0.6, 0.4])
    other_appliances = np.random.choice([0, 1], size=num_samples, p=[0.2, 0.8])
    
    house_type_idx = np.random.randint(0, 3, size=num_samples)
    
    # Underlying physical billing function
    # Base load + parameters * weights + appliance draws + random Gaussian noise
    noise = np.random.normal(0, 15, size=num_samples)
    consumption = (
        50.0 + 
        family_members * 25.0 + 
        ac_hours * 42.0 + 
        fan_hours * 4.5 + 
        tv_hours * 2.8 + 
        refrigerator * 35.0 + 
        washing_machine * 20.0 + 
        cooler * 55.0 + 
        other_appliances * 45.0 + 
        house_type_idx * 75.0 + 
        noise
    )
    
    # Clip consumption to positive values
    consumption = np.clip(consumption, 40.0, None)
    
    df = pd.DataFrame({
        "family_members": family_members,
        "house_type_idx": house_type_idx,
        "ac_hours": ac_hours,
        "fan_hours": fan_hours,
        "tv_hours": tv_hours,
        "refrigerator": refrigerator,
        "washing_machine": washing_machine,
        "cooler": cooler,
        "other_appliances": other_appliances,
        "consumption": consumption
    })
    return df

def train_predictor_model():
    """Train a RandomForestRegressor model on synthetic energy data."""
    global _model, _r2_score
    
    df = generate_synthetic_data()
    
    X = df.drop(columns=["consumption"])
    y = df["consumption"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestRegressor(n_estimators=100, random_state=42, min_samples_split=4)
    model.fit(X_train, y_train)
    
    # Calculate R² score to represent predictor confidence
    y_pred = model.predict(X_test)
    _r2_score = r2_score(y_test, y_pred)
    
    _model = model
    print(f"[Smart Energy Advisor] Energy Predictor ML Model Trained successfully. R2 Score (Confidence): {_r2_score:.4f}")

def predict_energy_usage(family_members, house_type, ac_hours, fan_hours, tv_hours, 
                         refrigerator, washing_machine, cooler, other_appliances):
    """Predict consumption (kWh) using the trained Random Forest model."""
    global _model, _r2_score
    
    if _model is None:
        train_predictor_model()
        
    house_idx = HOUSE_TYPE_MAP.get(house_type, 0)
    
    # Construct input vector for inference
    input_data = pd.DataFrame([{
        "family_members": int(family_members),
        "house_type_idx": int(house_idx),
        "ac_hours": float(ac_hours),
        "fan_hours": float(fan_hours),
        "tv_hours": float(tv_hours),
        "refrigerator": int(refrigerator),
        "washing_machine": int(washing_machine),
        "cooler": int(cooler),
        "other_appliances": int(other_appliances)
    }])
    
    prediction = _model.predict(input_data)[0]
    
    # Calculate confidence percent based on model R² score, scaling between 80% and 98%
    confidence_pct = max(80.0, min(98.0, _r2_score * 100.0 + np.random.uniform(-1, 1)))
    
    return {
        "predicted_units": round(float(prediction), 1),
        "confidence_score": round(confidence_pct, 1),
        "prediction_date": datetime.date.today().strftime("%B %d, %Y")
    }
