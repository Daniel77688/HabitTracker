from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from sqlalchemy.orm import Session
from src.models.database import get_db
from src.schemas.habit_schema import HabitCreate, HabitUpdate, HabitResponse
from src.services import habit_service

router = APIRouter(prefix="/habits", tags=["Habits"])

@router.post("/", response_model=HabitResponse, status_code=status.HTTP_201_CREATED)
def create_new_habit(habit_data: HabitCreate, db: Session = Depends(get_db)):
    try:
        new_habit = habit_service.create_habit(db=db, user_id=habit_data.user_id, title=habit_data.title, description=habit_data.description, frequency_type=habit_data.frequency_type, target_days=habit_data.target_days)
        return new_habit
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/user/{user_id}", response_model=List[HabitResponse])
def get_habits_by_user(user_id: int, db: Session = Depends(get_db)):
    habits = habit_service.get_habits_by_user(db=db, user_id=user_id)
    return habits

@router.get("/{habit_id}", response_model=HabitResponse)
def get_habit(habit_id: int, db: Session = Depends(get_db)):
    habit = habit_service.read_habit(db=db, habit_id=habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit

@router.put("/{habit_id}", response_model=HabitResponse)
def update_existing_habit(habit_id: int, habit_data: HabitUpdate, db: Session = Depends(get_db)):
    updated = habit_service.update_habit(db=db, habit_id=habit_id, title=habit_data.title, description=habit_data.description, frequency_type=habit_data.frequency_type, target_days=habit_data.target_days, status=habit_data.status)
    if not updated:
        raise HTTPException(status_code=404, detail="Habit not found")
    return updated

@router.delete("/{habit_id}")
def delete_existing_habit(habit_id: int, db: Session = Depends(get_db)):
    success = habit_service.delete_habit(db=db, habit_id=habit_id)
    if not success:
        raise HTTPException(status_code=404, detail="Habit not found")
    return {"message": "Habit deleted successfully"}