from pydantic import BaseModel
from typing import Optional, List
from src.models.habit_model import Freq, Status

class HabitCreate(BaseModel):
    user_id: int
    title: str
    description: Optional[str] = None
    frequency_type: Freq
    target_days: Optional[List[int]] = None

class HabitUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    frequency_type: Optional[Freq] = None
    target_days: Optional[List[int]] = None
    status: Optional[Status] = None