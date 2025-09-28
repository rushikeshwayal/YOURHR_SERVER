from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime
from uuid import UUID


class ResumeCreate(BaseModel):
    user_id: int
    resume_data: Dict[str, Any]
    status: Optional[str] = "draft"


class ResumeUpdate(BaseModel):
    resume_data: Optional[Dict[str, Any]] = None
    status: Optional[str] = None


class ResumeOut(BaseModel):
    id: UUID
    user_id: int
    resume_id: UUID
    resume_data: Dict[str, Any]
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
