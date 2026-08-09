from datetime import date
from src.models.database import SessionLocal
from src.models.habit_log_model import HabitLog
from src.models.habit_model import Habit

def log_habit_completion(habit_id: int, notes: str = None):
    db = SessionLocal()
    
    try:
        habit = db.query(Habit).filter(Habit.id == habit_id).first()
        
        if not habit:
            print(f"Cant register habit with ID: {habit_id}")
            return None

        hoy = date.today()
        existing_log = db.query(HabitLog).filter(HabitLog.habit_id == habit_id, HabitLog.completed_date == hoy).first()

        if existing_log:
            print(f"The habit: '{habit.title}', has already been completed.")
            return existing_log

        nuevo_log = HabitLog(habit_id=habit_id, completed_date=hoy, notes=notes)
        
        db.add(nuevo_log)
        db.commit()
        db.refresh(nuevo_log)
        
        print(f"Habit: '{habit.title}', successfully completed today ({hoy})")
        return nuevo_log

    except Exception as e:
        db.rollback()
        print(f"Error registering the completition of the habit: {e}")
        raise e
    finally:
        db.close()


def get_habit_logs(habit_id: int):
    db = SessionLocal()
    try:
        logs = db.query(HabitLog).filter(HabitLog.habit_id == habit_id).all()
        return logs
    except Exception as e:
        print(f"Error obtaining the logs of the habit: {e}")
        return []
    finally:
        db.close()


def delete_log(log_id: int):
    db = SessionLocal()
    try:
        log = db.query(HabitLog).filter(HabitLog.id == log_id).first()
        if not log:
            print(f"Didnt find log with ID {log_id}")
            return False

        db.delete(log)
        db.commit()
        print(f"Compliance record (ID: {log_id}) successfully removed")
        return True

    except Exception as e:
        db.rollback()
        print(f"Error removing log: {e}")
        raise e
    finally:
        db.close()