import enum
from sqlalchemy import Column, Integer, String, Boolean, Enum
from app.database import Base


class Priority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(120), nullable=False)
    description = Column(String(500), nullable=True)
    priority = Column(Enum(Priority), default=Priority.medium, nullable=False)
    done = Column(Boolean, default=False, nullable=False)
