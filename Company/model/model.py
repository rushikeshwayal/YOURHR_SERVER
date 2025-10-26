# models/company.py
from sqlalchemy import Column, String, Integer, Text
from database import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(String, unique=True, index=True)
    user_email = Column(String)
    poster = Column(String)
    name = Column(String)
    company_type = Column(String)
    ceo_name = Column(String)
    ceo_image_url = Column(String, nullable=True)
    description = Column(Text)
    industry = Column(String)
    mission = Column(Text)
    vision = Column(Text)
    goals = Column(Text)
    website = Column(String)
    phone_number = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    founded_year = Column(Integer)
    employee_count = Column(Integer)
    linkedin_url = Column(String)
    logo_url = Column(String)
