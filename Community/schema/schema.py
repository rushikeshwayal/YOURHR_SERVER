from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Request model for creating a message
class MessageCreate(BaseModel):
    user_email: EmailStr
    text: Optional[str] = None  # Optional text message

# Response model for returning messages
class MessageResponse(BaseModel):
    id: int
    channel_id: int
    user_email: EmailStr
    text: Optional[str] = None
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    file_url: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True
