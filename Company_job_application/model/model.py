from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base


class JobApplication(Base):
    __tablename__ = "company_job_applications"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False)
    resume_link = Column(String(255), nullable=False)
    why_hired = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    company_job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
