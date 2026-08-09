from sqlalchemy import Column, Integer, String, Date, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from src.models.database import Base

class HabitLog(Base):
    __tablename__ = "habit_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    habit_id = Column(Integer, ForeignKey("habits.id", ondelete="CASCADE"), nullable=False)
    completed_date = Column(Date, nullable=False)
    notes = Column(String(255), nullable=True) # Optional Note of that day
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    
    habit = relationship("Habit", back_populates='logs')
    
    def __repr__(self):
        return f"<HabitLog(id={self.id}, habit_id={self.habit_id}, date='{self.completed_date}')>"