from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime, date

class JobBase(BaseModel):
    company_id: str
    title: str
    role: str
    location: str
    job_type: str  # Full-time, Part-time, etc.
    salary_range: Optional[str] = None
    experience_required: Optional[str] = None
    skills_required: Optional[str] = None
    description: Optional[str] = None
    responsibilities: Optional[str] = None
    benefits: Optional[str] = None
    application_deadline: Optional[datetime] = None
    status: Optional[str] = "Active"
    apply_link: Optional[HttpUrl] = None

class JobCreate(JobBase):
    pass

class JobUpdate(BaseModel):
    title: Optional[str] = None
    role: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    salary_range: Optional[str] = None
    experience_required: Optional[str] = None
    skills_required: Optional[str] = None
    description: Optional[str] = None
    responsibilities: Optional[str] = None
    benefits: Optional[str] = None
    application_deadline: Optional[datetime] = None
    status: Optional[str] = None
    apply_link: Optional[HttpUrl] = None

class JobResponse(JobBase):
    id: int
    job_id: str
    posted_date: datetime
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
