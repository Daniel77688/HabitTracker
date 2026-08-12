import logging
from datetime import date
from sqlalchemy.orm import Session
from src.models.habit_log_model import HabitLog
from src.models.habit_model import Habit

logger = logging.getLogger(__name__)

def log_habit_completion(db: Session, habit_id: int, notes: str = None):
    try:
        habit = db.query(Habit).filter(Habit.id == habit_id).first()
        
        if not habit:
            logger.warning(f"No se puede registrar log para el hábito con ID: {habit_id}")
            return None

        hoy = date.today()
        existing_log = db.query(HabitLog).filter(HabitLog.habit_id == habit_id, HabitLog.completed_date == hoy).first()

        if existing_log:
            logger.info(f"El hábito '{habit.title}' ya ha sido completado hoy.")
            return existing_log

        nuevo_log = HabitLog(habit_id=habit_id, completed_date=hoy, notes=notes)
        
        db.add(nuevo_log)
        db.commit()
        db.refresh(nuevo_log)
        
        logger.info(f"Hábito '{habit.title}' completado hoy ({hoy})")
        return nuevo_log

    except Exception as e:
        db.rollback()
        logger.error(f"Error registrando el cumplimiento del hábito: {e}")
        raise e


def get_habit_logs(db: Session, habit_id: int):
    try:
        logs = db.query(HabitLog).filter(HabitLog.habit_id == habit_id).all()
        return logs
    except Exception as e:
        logger.error(f"Error obteniendo los logs del hábito: {e}")
        return []


def delete_log(db: Session, log_id: int):
    try:
        log = db.query(HabitLog).filter(HabitLog.id == log_id).first()
        if not log:
            logger.warning(f"No se encontró log con ID {log_id}")
            return False

        db.delete(log)
        db.commit()
        logger.info(f"Registro de cumplimiento (ID: {log_id}) eliminado correctamente")
        return True

    except Exception as e:
        db.rollback()
        logger.error(f"Error eliminando log: {e}")
        raise e