from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False

# schema for reading user


class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True

# schema for creating a user


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None


class UserAuth(BaseModel):
    email: EmailStr
    password: str
