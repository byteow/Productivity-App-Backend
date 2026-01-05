from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, Date
from datetime import datetime, timezone
from .enums import Gender

Base = declarative_base()
timestamp = lambda: datetime.now(timezone.utc)

GenderType = Enum(Gender, name="gender")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    birthday = Column(Date, nullable=True)
    gender = Column(GenderType, nullable=False)
    created_at = Column(DateTime(timezone=True), default=timestamp)
    updated_at = Column(DateTime(timezone=True), default=timestamp, onupdate=timestamp)

class LoginSession(Base):
    __tablename__ = "login_session"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    ip = Column(String(255), nullable=False)
    os = Column(String(255), nullable=False)
    client_app = Column(String(255), nullable=False)
    is_mobile_device = Column(Boolean, nullable=False)
    created_at = Column(DateTime(timezone=True), default=timestamp)
    updated_at = Column(DateTime(timezone=True), default=timestamp, onupdate=timestamp)