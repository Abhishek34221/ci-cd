from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    name: str          # 'full_name' ki jagah 'name' kar diya gaya hai
    email: EmailStr
    phone: str = "N/A" # Optional bana diya gaya hai taaki missing error na aaye
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str