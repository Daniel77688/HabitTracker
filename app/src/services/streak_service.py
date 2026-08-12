import logging
from datetime import date
from sqlalchemy.orm import Session
from src.models.streak_model import Streak

logger = logging.getLogger(__name__)

def get_or_create_streak(db: Session, habit_id: int):
    try:
        streak = db.query(Streak).filter(Streak.habit_id == habit_id).first()
        hoy = date.today()
        
        if not streak:
            streak = Streak(habit_id=habit_id, current_streak=0, longest_streak=0)
            db.add(streak)
            db.commit()
            db.refresh(streak)
        else:
            if streak.last_completed_date and (hoy - streak.last_completed_date).days > 1:
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
        if not streak:
            streak = Streak(habit_id=habit_id, current_streak=0, longest_streak=0)
            db.add(streak)
            db.commit()

        hoy = date.today()
        
        if streak.last_completed_date == hoy:
            return streak

        if streak.last_completed_date is None:
            streak.current_streak = 1
        else:
            diferencia_dias = (hoy - streak.last_completed_date).days
            
            if diferencia_dias == 1:
                streak.current_streak += 1
            elif diferencia_dias == 0:
                pass
            else:
                streak.current_streak = 1

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