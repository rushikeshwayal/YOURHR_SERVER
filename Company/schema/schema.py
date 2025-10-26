from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional
from datetime import datetime

# Schema for creating a new company
class CompanyCreate(BaseModel):
    user_email: str
    name: str
    company_type: str
    ceo_name: Optional[str] = None
    ceo_image_url: Optional[HttpUrl] = None
    description: str
    industry: str
    mission: str
    vision: str
    goals: str
    website: Optional[HttpUrl] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    founded_year: Optional[int] = None
    employee_count: Optional[int] = None
    linkedin_url: Optional[HttpUrl] = None
    logo_url: Optional[HttpUrl] = None


# Schema for updating existing company (all fields optional)
class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    company_type: Optional[str] = None
    ceo_name: Optional[str] = None
    ceo_image_url: Optional[HttpUrl] = None
    description: Optional[str] = None
    industry: Optional[str] = None
    mission: Optional[str] = None
    vision: Optional[str] = None
    goals: Optional[str] = None
    website: Optional[HttpUrl] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    founded_year: Optional[int] = None
    employee_count: Optional[int] = None
    linkedin_url: Optional[HttpUrl] = None
    logo_url: Optional[HttpUrl] = None


# Response model (includes DB-generated fields)
class CompanyResponse(BaseModel):
    id: int
    company_id: str
    user_email: str
    name: str
    company_type: str
    ceo_name: Optional[str]
    ceo_image_url: Optional[str]
    description: Optional[str]
    industry: Optional[str]
    mission: Optional[str]
    vision: Optional[str]
    goals: Optional[str]
    website: Optional[str]
    phone_number: Optional[str]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    founded_year: Optional[int]
    employee_count: Optional[int]
    linkedin_url: Optional[str]
    logo_url: Optional[str]

    class Config:
        orm_mode = True