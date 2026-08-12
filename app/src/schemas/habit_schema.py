from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from src.models.habit_model import Freq, Status

class HabitCreate(BaseModel):
    user_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    frequency_type: Freq = Freq.daily
    target_days: Optional[List[int]] = None

class HabitUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    frequency_type: Optional[Freq] = None
    target_days: Optional[List[int]] = None
    status: Optional[Status] = None

class HabitResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str] = None
    frequency_type: Freq
    target_days: Optional[List[int]] = None
    status: Status

    model_config = ConfigDict(from_attributes=True)
