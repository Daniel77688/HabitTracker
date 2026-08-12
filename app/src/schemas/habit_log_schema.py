from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)