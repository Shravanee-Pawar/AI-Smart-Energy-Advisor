from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: str


class LoginRequest(BaseModel):
    id_token: str


class UserResponse(BaseModel):
    uid: str
    name: str
    email: EmailStr
    phone: str