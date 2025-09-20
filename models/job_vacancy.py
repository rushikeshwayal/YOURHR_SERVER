from sqlalchemy import Column, Integer, String, Text, Date, TIMESTAMP
from sqlalchemy.sql import func
from database import Base

class JobVacancy(Base):
    __tablename__ = "job_vacancies"

    job_id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String(255), nullable=False)
    company_name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    employment_type = Column(String(50), nullable=False)
    job_description = Column(Text, nullable=False)
    salary_range = Column(String(50))
    skills_required = Column(Text)
    experience_required = Column(String(100))
    education_required = Column(String(255))
    benefits = Column(Text)
    application_deadline = Column(Date)
    job_posted_date = Column(TIMESTAMP, server_default=func.now())
    job_status = Column(String(20), server_default="Open")
    contact_email = Column(String(255), nullable=False)
    application_url = Column(String(255))
