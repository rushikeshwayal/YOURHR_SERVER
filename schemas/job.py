from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime

class JobCreate(BaseModel):
    job_title: str
    company_name: str
    location: str
    employment_type: str
    job_description: str
    salary_range: Optional[str]
    skills_required: Optional[str]
    experience_required: Optional[str]
    education_required: Optional[str]
    benefits: Optional[str]
    application_deadline: date
    job_status: Optional[str] = "Open"
    contact_email: str
    application_url: Optional[str]

class JobOut(JobCreate):
    job_id: int
    job_posted_date: datetime
