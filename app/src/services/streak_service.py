from datetime import date
from src.models.database import SessionLocal
from src.models.streak_model import Streak

def get_or_create_streak(habit_id: int):
    db = SessionLocal()
    try:
        streak = db.query(Streak).filter(Streak.habit_id == habit_id).first()
        if not streak:
            streak = Streak(habit_id=habit_id, current_streak=0, longest_streak=0)
            db.add(streak)
            db.commit()
            db.refresh(streak)
        return streak
    except Exception as e:
        db.rollback()
        print(f"Error al obtener/crear la racha: {e}")
        return None
    finally:
        db.close()


def update_streak_on_completion(habit_id: int):
    db = SessionLocal()
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
        print(f"Racha actualizada -> Actual: {streak.current_streak} | Máxima: {streak.longest_streak}")
        return streak

    except Exception as e:
        db.rollback()
        print(f"Error al actualizar la racha: {e}")
        raise e
    finally:
        db.close()