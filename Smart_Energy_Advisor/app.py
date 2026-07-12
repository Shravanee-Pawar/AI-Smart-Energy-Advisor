import os
from flask import Flask, redirect, url_for
from dotenv import load_dotenv

# Load env variables from .env file
load_dotenv()

from services.db import init_db
from models.predictor import train_predictor_model
from routes.auth import auth_bp
from routes.main import main_bp
from routes.ai import ai_bp

def create_app():
    """Application factory for Smart Energy Advisor Flask app."""
    app = Flask(__name__)
    
    # Session Secret Key config
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "smart-energy-fallback-key-54321")
    
    # Initialize SQLite Database & tables
    print("[Smart Energy Advisor] Initializing SQLite database...")
    init_db()
    
    # Train the Scikit-learn Prediction Model
    print("[Smart Energy Advisor] Training Energy Prediction ML model...")
    train_predictor_model()
    
    # Register blueprints (prefix-less mapping for clean URLs)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(ai_bp)
    
    # Root error boundary redirects
    @app.errorhandler(404)
    def page_not_found(e):
        return redirect(url_for('main.index'))
        
    return app

app = create_app()

if __name__ == "__main__":
    # Start local server on Port 5000
    app.run(host="0.0.0.0", port=5000, debug=True)
