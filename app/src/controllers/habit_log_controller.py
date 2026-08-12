from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from sqlalchemy.orm import Session
from src.models.database import get_db
from src.schemas.habit_log_schema import HabitLogCreate, HabitLogResponse
from src.services import habit_log_service, streak_service

router = APIRouter(prefix="/habit-logs", tags=["Habit Logs"])

@router.post("/", response_model=HabitLogResponse, status_code=status.HTTP_201_CREATED)
def log_habit_completion(log_data: HabitLogCreate, db: Session = Depends(get_db)):
    try:
        new_log = habit_log_service.log_habit_completion(db=db, habit_id=log_data.habit_id, notes=log_data.notes)
        
        if not new_log:
            raise HTTPException(status_code=400, detail="Could not log habit completion (Habit might not exist).")

        streak_service.update_streak_on_completion(db=db, habit_id=log_data.habit_id)

        return new_log
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/habit/{habit_id}", response_model=List[HabitLogResponse])
def get_logs_by_habit(habit_id: int, db: Session = Depends(get_db)):
    logs = habit_log_service.get_habit_logs(db=db, habit_id=habit_id)
    return logs

@router.delete("/{log_id}")
def delete_habit_log(log_id: int, db: Session = Depends(get_db)):
    success = habit_log_service.delete_log(db=db, log_id=log_id)
    if not success:
        raise HTTPException(status_code=404, detail="Habit log not found")
    return {"message": "Habit log deleted successfully"}