import logging
from datetime import date, timedelta
from sqlalchemy.orm import Session
from src.models.streak_model import Streak
from src.models.habit_model import Habit, Freq

logger = logging.getLogger(__name__)

def _is_streak_expired(habit: Habit, last_completed_date: date, hoy: date) -> bool:
    if not last_completed_date:
        return False
        
    freq = habit.frequency_type if habit else Freq.daily
    
    if freq == Freq.daily:
        return (hoy - last_completed_date).days > 1
    elif freq == Freq.weekly:
        last_y, last_w, _ = last_completed_date.isocalendar()
        hoy_y, hoy_w, _ = hoy.isocalendar()
        week_diff = (hoy_y - last_y) * 52 + (hoy_w - last_w)
        return week_diff > 1
    elif freq == Freq.monthly:
        month_diff = (hoy.year - last_completed_date.year) * 12 + (hoy.month - last_completed_date.month)
        return month_diff > 1
    elif freq == Freq.custom:
        if not habit.target_days:
            return (hoy - last_completed_date).days > 1
        current = last_completed_date + timedelta(days=1)
        while current < hoy:
            if current.weekday() in habit.target_days:
                return True
            current += timedelta(days=1)
        return False
    return False

def get_or_create_streak(db: Session, habit_id: int):
    try:
        streak = db.query(Streak).filter(Streak.habit_id == habit_id).first()
        habit = db.query(Habit).filter(Habit.id == habit_id).first()
        hoy = date.today()
        
        if not streak:
            streak = Streak(habit_id=habit_id, current_streak=0, longest_streak=0)
            db.add(streak)
            db.commit()
            db.refresh(streak)
        else:
            if streak.last_completed_date and _is_streak_expired(habit, streak.last_completed_date, hoy):
                streak.current_streak = 0
                db.commit()
                db.refresh(streak)
                
        return streak
    except Exception as e:
        db.rollback()
        logger.error(f"Error al obtener/crear la racha: {e}")
        return None


def update_streak_on_completion(db: Session, habit_id: int):
    try:
        streak = db.query(Streak).filter(Streak.habit_id == habit_id).first()
        habit = db.query(Habit).filter(Habit.id == habit_id).first()
        
        if not streak:
            streak = Streak(habit_id=habit_id, current_streak=0, longest_streak=0)
            db.add(streak)
            db.commit()

        hoy = date.today()
        
        if streak.last_completed_date == hoy:
            return streak

        if streak.last_completed_date is None or _is_streak_expired(habit, streak.last_completed_date, hoy):
            streak.current_streak = 1
        else:
            streak.current_streak += 1

        streak.last_completed_date = hoy

        if streak.current_streak > streak.longest_streak:
            streak.longest_streak = streak.current_streak

        db.commit()
        db.refresh(streak)
        logger.info(f"Racha actualizada para hábito {habit_id} -> Actual: {streak.current_streak} | Máxima: {streak.longest_streak}")
        return streak

    except Exception as e:
        db.rollback()
        logger.error(f"Error al actualizar la racha: {e}")
        raise e