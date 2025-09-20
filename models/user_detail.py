from sqlalchemy import Column, Integer, String, Text, CheckConstraint
from database import Base

class UserDetail(Base):
    __tablename__ = "user_details"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    phone_number = Column(String(15))
    email_address = Column(String(255), unique=True, nullable=False)
    college_name = Column(String(255))
    college_status = Column(String(20))
    address_area = Column(String(255))
    address_city = Column(String(100))
    address_state = Column(String(100))
    post_code = Column(String(20))
    skills = Column(Text)
    __table_args__ = (
        CheckConstraint(
            "college_status IN ('Pursuing', 'Completed')",
            name="user_details_college_status_check"
        ),
    )
