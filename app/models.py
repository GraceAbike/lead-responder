from sqlalchemy import Column, Integer, String, DateTime
from .db import Base
import datetime

class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    customer_phone = Column(String, nullable=False)
    status = Column(String, default="New")
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
