from sqlalchemy import Column, Integer, String, Text, CheckConstraint
from database import Base
from sqlalchemy.dialects.postgresql import UUID as uuid
from sqlalchemy.dialects.postgresql import UUID
import uuid as uuid_lib

class UserDetail(Base):
    __tablename__ = "user_details"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid_lib.uuid4)

    full_name = Column(String(100), nullable=False)
    phone_number = Column(String(15))
    email_address = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=True)  # Optional for Google users
