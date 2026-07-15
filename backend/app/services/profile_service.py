from app.core.firebase import db


def get_profile(uid: str):
    doc = db.collection("users").document(uid).get()

    if not doc.exists:
        return None

    return doc.to_dict()


def update_profile(uid: str, profile_data: dict):
    db.collection("users").document(uid).update(profile_data)

    updated_doc = db.collection("users").document(uid).get()

    return updated_doc.to_dict()