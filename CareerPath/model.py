from sqlalchemy import Column, ForeignKey, String, DateTime, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID
import uuid as uuid_lib  # Python module for generating UUIDs
from database import Base
from datetime import datetime

class RoadMap(Base):
    __tablename__ = "roadmaps"

    id = Column(UUID, primary_key=True, default=uuid_lib.uuid4)
    user_email = Column(String, nullable=False)

    roadmap_id = Column(UUID, unique=True, default=uuid_lib.uuid4, nullable=False)
    job_title = Column(String, nullable=False)
    company_name = Column(String, nullable=True)
    roadmap_data = Column(JSONB, nullable=False)
    status = Column(String, default="draft")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)