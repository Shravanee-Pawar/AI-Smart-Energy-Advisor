from fastapi import HTTPException
from firebase_admin import auth
from firebase_admin._auth_utils import EmailAlreadyExistsError

from app.core.firebase import db
from app.schemas.auth import UserResponse


def create_user(name: str, email: str, password: str, phone: str):
    """
    Create a new user in Firebase Authentication
    and store additional details in Firestore.
    """

    try:
        # Create user in Firebase Authentication
        user = auth.create_user(
            email=email,
            password=password,
            display_name=name
        )

        # Save user profile in Firestore
        db.collection("users").document(user.uid).set({
            "uid": user.uid,
            "name": name,
            "email": email,
            "phone": phone
        })

        # Return response
        return UserResponse(
            uid=user.uid,
            name=name,
            email=email,
            phone=phone
        )

    except EmailAlreadyExistsError:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


def get_user(uid: str):
    """
    Get a user's profile from Firestore.
    """

    doc = db.collection("users").document(uid).get()

    if doc.exists:
        return doc.to_dict()

    return None


def verify_user(id_token: str):
    """
    Verify Firebase ID token and return user information.
    """

    try:
        # Verify Firebase ID token
        decoded_token = auth.verify_id_token(id_token)

        uid = decoded_token["uid"]

        # Get user profile from Firestore
        user = get_user(uid)

        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User profile not found"
            )

        return user

    except auth.InvalidIdTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid ID token"
        )

    except auth.ExpiredIdTokenError:
        raise HTTPException(
            status_code=401,
            detail="ID token has expired"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )