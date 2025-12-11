from pydantic import BaseModel, EmailStr, ConfigDict


# Shared properties
class UserBase(BaseModel):
    email: EmailStr


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str


# Properties to return via API
class User(UserBase):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
