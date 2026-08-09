from sqlalchemy.orm import relationship
import enum
from sqlalchemy import Column, Integer, String, Enum, JSON, TIMESTAMP, func, ForeignKey
from src.models.database import Base

class Freq(enum.Enum):
    daily = 1
    weekly = 2
    monthly = 3
    custom = 4
    
class Status(enum.Enum):
    active = 1
    archived = 2
    deleted = 3
    
class Habit(Base):
    __tablename__ = "habits"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    frequency_type = Column(Enum(Freq), nullable=False)
    target_days = Column(JSON, nullable=True)
    status = Column(Enum(Status), default=Status.active, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    
    user = relationship("User", back_populates="habits")
    logs = relationship("HabitLog", back_populates="habit", cascade="all, delete-orphan")
    streak = relationship("Streak", back_populates="habit", uselist=False, cascade="all, delete-orphan")
    
    def __repr__(self): # Purely for debugging purposes: if you prints habits it will sow what it contains
        return f"<Habit(id={self.id}, title='{self.title}', status='{self.status.name}')>"