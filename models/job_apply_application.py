from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from database import Base

class JobApplyApplication(Base):
    __tablename__ = "job_apply_applications"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False)
    resume_link = Column(String(255))
    why_hired = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    job_id = Column(Integer, ForeignKey("job_vacancies.job_id"), nullable=False)
