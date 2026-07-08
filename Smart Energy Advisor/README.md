# ⚡ Smart Energy Advisor

Smart Energy Advisor is a complete, production-quality web application designed to help homeowners forecast electricity usage, estimate utility bills, visualize consumption analytics, and receive AI-powered energy-saving action plans.

The application leverages **Flask** for the backend, **Tailwind CSS** for UI, **Chart.js** for interactive analytics, **SQLite** for secure database logging, **Scikit-learn** for machine learning forecasts, and the **Google Gemini API** for generative AI consulting.

---

## 🛠️ Project Structure

```text
Smart Energy Advisor/
│
├── database/
│   └── schema.sql        # Database initialization schema
│
├── models/
│   └── predictor.py      # Random Forest ML model training & inference logic
│
├── routes/
│   ├── auth.py           # Registration, login, and logout controllers
│   ├── main.py           # Core views (dashboard, usage entry, estimated bill, charts)
│   └── ai.py             # AI Chat assistant and recommendation engines
│
├── services/
│   ├── db.py             # SQLite helper functions for database CRUD operations
│   └── gemini.py         # Google Gemini generative API client (with mock fallbacks)
│
├── static/
│   ├── css/
│   │   └── style.css     # Glassmorphism styling and keyframe animations
│   └── js/
│       ├── main.js       # Form validations and UI interactive states
│       ├── charts.js     # Responsive Chart.js graph definitions
│       └── chat.js       # Asynchronous AJAX chatbot engine & typing indicator
│
├── templates/
│   ├── base.html         # Base template with responsive sidebar & toast alerts
│   ├── landing.html      # Landing hero page with UN SDG 7 information
│   ├── register.html     # User registration form with validation checks
│   ├── login.html        # Login portal with "Remember Me"
│   ├── dashboard.html    # Core admin panel featuring glassmorphism cards
│   ├── usage.html        # Monthly units & heavy appliance draw log form
│   ├── prediction.html   # ML-predicted results page
│   ├── bill.html         # Detailed invoice estimate including 18% GST
│   ├── analytics.html    # Visualizations layout for interactive Chart.js canvases
│   ├── ai_assistant.html # ChatGPT-style chatbot page
│   ├── recommendations.html # Priority-prioritized action savings cards
│   └── profile.html      # Profile settings and password management
│
├── utils/
│   └── helpers.py        # Hashing checks, email validations, and bill calculations
│
├── app.py                # Main application initialization entry point
├── requirements.txt      # Project backend Python package dependencies
├── .env                  # Local environment file containing configuration variables
├── .env.example          # Sample environment variables file
└── README.md             # Project documentation (this file)
```

---

## 💻 Tech Stack

* **Backend**: Python, Flask, SQLite3
* **Machine Learning**: Scikit-learn (RandomForestRegressor), Pandas, NumPy
* **Generative AI**: Google Gemini API (`google-generativeai`)
* **Frontend**: HTML5, Tailwind CSS, JavaScript (ES6), Chart.js (v4), Font Awesome Icons

---

## 🚀 Getting Started

Follow these steps to run the application locally:

### 1. Prerequisites
Make sure you have **Python 3.8+** installed on your machine.

### 2. Configure Virtual Environment
**On Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file (one has been pre-created for you) or copy `.env.example`:
```bash
# On Windows powershell:
copy .env.example .env
```
Inside `.env`, you can optionally add your `GEMINI_API_KEY` for live AI generation. If left blank, the application automatically runs in **Mock Mode**, providing realistic mock recommendations and chatbot answers so you can preview all features immediately.

### 5. Launch the Application
```bash
python app.py
```
This initializes the database, trains the Random Forest model on dynamic synthetic data, and spins up the Flask server on **[http://localhost:5000](http://localhost:5000)**.
