from fastapi import APIRouter, HTTPException
from src.schemas.habit_schema import HabitCreate, HabitUpdate
from src.services import habit_service

router = APIRouter(prefix="/habits", tags=["Habits"])

@router.post("/", response_model=dict)
def create_new_habit(habit_data: HabitCreate):
    try:
        new_habit = habit_service.create_habit(user_id=habit_data.user_id, title=habit_data.title, description=habit_data.description, frequency_type=habit_data.frequency_type, target_days=habit_data.target_days)
        return {"message": "Habit created successfully", "habit_id": new_habit.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/user/{user_id}", response_model=list)
def get_habits_by_user(user_id: int):
    habits = habit_service.get_habits_by_user(user_id)
    return habits

@router.get("/{habit_id}")
def get_habit(habit_id: int):
    habit = habit_service.read_habit(habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit

@router.put("/{habit_id}")
def update_existing_habit(habit_id: int, habit_data: HabitUpdate):
    updated = habit_service.update_habit( habit_id=habit_id, title=habit_data.title, description=habit_data.description, frequency_type=habit_data.frequency_type, target_days=habit_data.target_days, status=habit_data.status)
    if not updated:
        raise HTTPException(status_code=404, detail="Habit not found")
    return {"message": "Habit updated successfully"}

@router.delete("/{habit_id}")
def delete_existing_habit(habit_id: int):
    success = habit_service.delete_habit(habit_id)
    if not success:
        raise HTTPException(status_code=404, detail="Habit not found")
    return {"message": "Habit deleted successfully"}