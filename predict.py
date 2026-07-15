import joblib
import pandas as pd
import json
import sys

def predict_energy(input_json_str):
    """
    Production entry point for the backend FastAPI application.
    Accepts target inputs and historical values to yield next month's predicted units.
    """
    try:
        # Load sample input payload
        data = json.loads(input_json_str)
        
        # Structure dataframe matching original feature columns
        X_input = pd.DataFrame([{
            'Year': data['Year'],
            'Month': data['Month'],
            'lag_1': data['lag_1'],
            'lag_2': data['lag_2'],
            'rolling_mean_3': data['rolling_mean_3']
        }])
        
        # Ingest models and standard scaling pipelines
        scaler = joblib.load("models/scaler.pkl")
        model = joblib.load("models/model.pkl")
        
        # Execute transformation and inferences
        X_scaled = scaler.transform(X_input)
        prediction = model.predict(X_scaled)[0]
        
        return json.dumps({"predicted_units": int(round(prediction))})
        
    except Exception as e:
        return json.dumps({"error": str(e)})

if __name__ == "__main__":
    # Sample execution payload matching backend contract
    sample_payload = '{"Year": 2007, "Month": 8, "lag_1": 497.09, "lag_2": 595.35, "rolling_mean_3": 608.64}'
    print("Executing sample prediction payload...")
    print(predict_energy(sample_payload))
