from fastapi import APIRouter, HTTPException
from typing import List
from src.schemas.habit_log_schema import HabitLogCreate, HabitLogResponse
from src.services import habit_log_service, streak_service

router = APIRouter(prefix="/habit-logs", tags=["Habit Logs"])

@router.post("/", response_model=dict)
def log_habit_completion(log_data: HabitLogCreate):
    try:
        new_log = habit_log_service.log_habit_completion(habit_id=log_data.habit_id, notes=log_data.notes)
        
        if not new_log: raise HTTPException(status_code=400, detail="Could not log habit completion (Habit might not exist).")

        streak_service.update_streak_on_completion(habit_id=log_data.habit_id)

        return {
            "message": "Habit completed and streak updated successfully",
            "log_id": new_log.id,
            "completed_date": str(new_log.completed_date)
        }
    except Exception as e: raise HTTPException(status_code=400, detail=str(e))

@router.get("/habit/{habit_id}", response_model=List[HabitLogResponse])
def get_logs_by_habit(habit_id: int):
    logs = habit_log_service.get_habit_logs(habit_id)
    return logs

@router.delete("/{log_id}")
def delete_habit_log(log_id: int):
    success = habit_log_service.delete_log(log_id)
    if not success:
        raise HTTPException(status_code=404, detail="Habit log not found")
    return {"message": "Habit log deleted successfully"}