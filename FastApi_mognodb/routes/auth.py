from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from models.user import User
from utils.security import (
    hash_password,
    verify_password,
    create_access_token
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    phone: str   # Ab yeh required ban gaya hai jo form se aayega
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

@router.post("/register")
async def register(user: UserRegister):
    existing_email = User.objects(email=user.email).first()
    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = hash_password(user.password)

    # Yahan user.full_name ki jagah user.name use kiya gaya hai
    new_user = User(
        full_name=user.name,
        email=user.email,
        phone=user.phone,
        password=hashed_password
    )
    new_user.save()

    return {
        "message": "User Registered Successfully ✅",
        "user_id": str(new_user.id)
    }

@router.post("/login")
async def login(user: UserLogin):
    existing_user = User.objects(email=user.email).first()
    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    password_valid = verify_password(
        user.password,
        existing_user.password
    )

    if not password_valid:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        str(existing_user.id)
    )

    return {
        "message": "Login Successfully ✅",
        "access_token": access_token,
        "token_type": "bearer"
    }