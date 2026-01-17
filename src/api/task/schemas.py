from pydantic import BaseModel, Field
from db import TaskPriority, TaskStatus
from typing import Optional

class CreateTaskSchema(BaseModel):
    category: str = Field(max_length=255)
    description: str = Field(max_length=255)
    priority: TaskPriority
    is_pinned: bool

class UpdateTaskSchema(BaseModel):
    task_id: int
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None

class DeleteTaskSchema(BaseModel):
    task_id: int