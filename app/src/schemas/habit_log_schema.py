from pydantic import BaseModel
from typing import Optional
from datetime import date

class HabitLogCreate(BaseModel):
    habit_id: int
    notes: Optional[str] = None

class HabitLogResponse(BaseModel):
    id: int
    habit_id: int
    completed_date: date
    notes: Optional[str] = None

    class Config:
        from_attributes = True  # Permite mapear modelos de SQLAlchemy directamente a Pydantic