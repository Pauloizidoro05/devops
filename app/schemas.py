from typing import Optional
from pydantic import BaseModel, Field
from app.models import Priority


class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: Optional[str] = Field(default=None, max_length=500)
    priority: Priority = Priority.medium
    done: bool = False


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=120)
    description: Optional[str] = Field(default=None, max_length=500)
    priority: Optional[Priority] = None
    done: Optional[bool] = None


class TaskOut(TaskBase):
    id: int

    class Config:
        from_attributes = True
