from fastapi import APIRouter, HTTPException
from src.schemas.streak_schema import StreakResponse
from src.services import streak_service

router = APIRouter(prefix="/streaks", tags=["Streaks"])

@router.get("/habit/{habit_id}", response_model=StreakResponse)
def get_habit_streak(habit_id: int):
    streak = streak_service.get_or_create_streak(habit_id)
    if not streak:
        raise HTTPException(status_code=404, detail="Could not retrieve or create streak for this habit.")
    return streak