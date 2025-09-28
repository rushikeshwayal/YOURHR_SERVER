from sqlalchemy import Column, ForeignKey, String, DateTime, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID
import uuid as uuid_lib  # Python module for generating UUIDs
from database import Base
from datetime import datetime



class Resume(Base):
    __tablename__ = "resumes"

    id = Column(UUID, primary_key=True, default=uuid_lib.uuid4)
    user_id = Column(Integer, ForeignKey("user_details.id"), nullable=False)

    resume_id = Column(UUID, unique=True, default=uuid_lib.uuid4, nullable=False)
    resume_data = Column(JSONB, nullable=False)
    status = Column(String, default="draft")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
