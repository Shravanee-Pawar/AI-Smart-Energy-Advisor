from app.core.firebase import db


def get_profile(uid: str):
    doc = db.collection("users").document(uid).get()

    if not doc.exists:
        return None

    profile = doc.to_dict()

    # Default values for older user documents
    profile.setdefault("uid", uid)
    profile.setdefault("name", "")
    profile.setdefault("email", "")
    profile.setdefault("phone", "")
    profile.setdefault("address", "")
    profile.setdefault("household_size", 1)
    profile.setdefault("tariff", "Residential")

    return profile


def update_profile(uid: str, profile_data: dict):
    db.collection("users").document(uid).update(profile_data)

    updated_doc = db.collection("users").document(uid).get()

    profile = updated_doc.to_dict()

    profile.setdefault("uid", uid)
    profile.setdefault("name", "")
    profile.setdefault("email", "")
    profile.setdefault("phone", "")
    profile.setdefault("address", "")
    profile.setdefault("household_size", 1)
    profile.setdefault("tariff", "Residential")

    return profile