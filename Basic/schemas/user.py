from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class UserCreate(BaseModel):
    user_id: Optional[str]
    full_name: str
    phone_number: Optional[str]
    email_address: str
    password: Optional[str]  # Optional for Google users

class GoogleUserCreate(BaseModel):
    full_name: str
    email_address: str
    phone_number: Optional[str] = None
    photo_url: Optional[str] = None

class UserOut(BaseModel):
    id: int
    user_id: str  # Convert UUID to string
    full_name: str
    phone_number: Optional[str]
    email_address: str
    password: Optional[str]
    
    class Config:
        from_attributes = True
