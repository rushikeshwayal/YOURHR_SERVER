from pydantic import BaseModel, Field
from typing import Optional

class UserCreate(BaseModel):
    full_name: str
    phone_number: Optional[str]
    email_address: str
    college_name: Optional[str]
    college_status: Optional[str]
    address_area: Optional[str]
    address_city: Optional[str]
    address_state: Optional[str]
    post_code: Optional[str]
    skills: Optional[str]

class UserOut(UserCreate):
    id: int
