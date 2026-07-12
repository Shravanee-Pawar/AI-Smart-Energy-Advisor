import firebase_admin
from firebase_admin import credentials, firestore, auth
from pathlib import Path

# Path to firebase-key.json
BASE_DIR = Path(__file__).resolve().parent.parent.parent
cred_path = BASE_DIR / "firebase-key.json"

# Initialize Firebase only once
if not firebase_admin._apps:
    cred = credentials.Certificate(str(cred_path))
    firebase_admin.initialize_app(cred)

# Firestore database instance
db = firestore.client()