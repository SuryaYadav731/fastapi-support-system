from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    created_at: datetime

    class Config:
        from_attributes = True



class UserProfile(BaseModel):

    id: int
    name: str
    email: EmailStr
    role: str

    class Config:
        orm_mode = True


class UpdateProfile(BaseModel):

    name: str


class ChangePassword(BaseModel):

    old_password: str
    new_password: str