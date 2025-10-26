from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
import uuid

class Job(Base):
    __tablename__ = "company_jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, unique=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    role = Column(String, nullable=False)
    location = Column(String, nullable=False)
    job_type = Column(String, nullable=False)  # Full-time, Part-time, Internship, etc.
    salary_range = Column(String)
    experience_required = Column(String)
    skills_required = Column(Text)
    description = Column(Text)
    responsibilities = Column(Text)
    benefits = Column(Text)
    application_deadline = Column(DateTime(timezone=True))
    status = Column(String, default="Active")  # “Active” or “Inactive”
    apply_link = Column(String)
    posted_date = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
