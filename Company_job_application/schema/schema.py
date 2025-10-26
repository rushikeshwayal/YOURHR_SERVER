from pydantic import BaseModel, EmailStr, HttpUrl
from datetime import datetime
from typing import Optional


class JobApplicationBase(BaseModel):
    email: EmailStr
    resume_link: HttpUrl
    why_hired: Optional[str] = None
    company_job_id: int


class JobApplicationCreate(JobApplicationBase):
    pass


class JobApplicationResponse(JobApplicationBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
