from pydantic import BaseModel
from typing import Optional
from datetime import date

class StreakResponse(BaseModel):
    id: int
    habit_id: int
    current_streak: int
    longest_streak: int
    last_completed_date: Optional[date] = None

    class Config:
        from_attributes = True