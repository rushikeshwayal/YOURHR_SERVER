from pydantic import BaseModel, EmailStr
from typing import List, Dict, Any, Optional
import uuid

# Pydantic schema for creating a new roadmap
class RoadMapCreate(BaseModel):
    user_email: EmailStr
    job_title: str
    company_name: Optional[str] = "N/A"
    roadmap_data: List[Dict[str, Any]]

# Pydantic schema for returning a roadmap from the API
class RoadMapOut(BaseModel):
    id: uuid.UUID
    user_email: EmailStr
    job_title: str
    company_name: Optional[str] = "N/A"
    roadmap_id: uuid.UUID
    roadmap_data: List[Dict[str, Any]]
    status: str
    
    class Config:
        orm_mode = True # Enables an object to be created from an ORM model