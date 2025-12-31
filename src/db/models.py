from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime, timezone
from .enums import Gender, Service

Base = declarative_base()
timestamp = lambda: datetime.now(timezone.utc)

GenderType = Enum(Gender, name="gender")
SmsCodesService = Enum(Service, name="service")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(GenderType, nullable=False)
    created_at = Column(DateTime(timezone=True), default=timestamp)
    updated_at = Column(DateTime(timezone=True), default=timestamp, onupdate=timestamp)

class SmsCodes(Base):
    __tablename__ = "sms_codes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255))
    code = Column(Integer)
    service = Column(SmsCodesService, nullable=False)
    created_at = Column(DateTime(timezone=True), default=timestamp)