from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .db import Base

class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    kyc_status = Column(String, default="PENDING")
    created_at = Column(DateTime, default=datetime.utcnow)
