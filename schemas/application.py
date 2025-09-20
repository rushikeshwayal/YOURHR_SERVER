from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ApplicationCreate(BaseModel):
    email: str
    resume_link: Optional[str]
    why_hired: Optional[str]
    job_id: int

class ApplicationOut(ApplicationCreate):
    id: int
    created_at: datetime
