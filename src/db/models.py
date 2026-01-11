from sqlalchemy.orm import declarative_base, relationship, Mapped
from typing import Optional
from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    Boolean, 
    DateTime, 
    Enum, 
    Date,
    JSON,
    ForeignKey
)
from datetime import datetime, timezone
from .enums import Gender, SurveyStatus, TaskPriority, TaskStatus

Base = declarative_base()
timestamp = lambda: datetime.now(timezone.utc)

GenderType = Enum(Gender, name="gender")
SurveyStatusType = Enum(SurveyStatus, name="survey_status")
TaskStatusType = Enum(TaskStatus, name="task_status")
TaskPriorityType = Enum(TaskPriority, name="task_priority")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    birthday = Column(Date, nullable=True)
    gender = Column(GenderType, nullable=False)
    created_at = Column(DateTime(timezone=True), default=timestamp)
    updated_at = Column(DateTime(timezone=True), default=timestamp, onupdate=timestamp)

    streak = relationship("Streak", back_populates="user", uselist=False)

class LoginSession(Base):
    __tablename__ = "login_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    ip = Column(String(255), nullable=False)
    os = Column(String(255), nullable=False)
    client_app = Column(String(255), nullable=False)
    is_mobile_device = Column(Boolean, nullable=False)
    created_at = Column(DateTime(timezone=True), default=timestamp)
    updated_at = Column(DateTime(timezone=True), default=timestamp, onupdate=timestamp)

class SurveyAnswers(Base):
    __tablename__ = "surveys_answers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    survey_id = Column(Integer, ForeignKey("surveys.id"), nullable=False, index=True)
    schema = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), default=timestamp)
    updated_at = Column(DateTime(timezone=True), default=timestamp, onupdate=timestamp)

    survey: Mapped["Survey"] = relationship(back_populates="answers")

class Survey(Base):
    __tablename__ = "surveys"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    status = Column(SurveyStatusType, nullable=False)
    schema = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), default=timestamp, index=True)
    updated_at = Column(DateTime(timezone=True), default=timestamp, onupdate=timestamp)

    answers: Mapped[Optional["SurveyAnswers"]] = relationship(back_populates="survey")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    category = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    status = Column(TaskStatusType, nullable=False)
    priority = Column(TaskPriorityType, nullable=False)
    is_pinned = Column(Boolean, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), default=timestamp, index=True)
    updated_at = Column(DateTime(timezone=True), default=timestamp, onupdate=timestamp)

class Streak(Base):
    __tablename__ = "streaks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, index=True)
    streak_days = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False)
    penalty_days = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), default=timestamp)
    updated_at = Column(DateTime(timezone=True), default=timestamp, onupdate=timestamp)

    user = relationship("User", back_populates="streak")