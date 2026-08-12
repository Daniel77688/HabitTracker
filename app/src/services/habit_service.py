import logging
from sqlalchemy.orm import Session
from src.models.habit_model import Habit, Freq, Status

logger = logging.getLogger(__name__)

def create_habit(db: Session, user_id: int, title: str, description: str = None, frequency_type: Freq = Freq.daily, target_days: list = None):
    try:
        habit = Habit(
            user_id=user_id,
            title=title,
            description=description,
            frequency_type=frequency_type,
            target_days=target_days
        )
        db.add(habit)    
        db.commit()
        db.refresh(habit)
        
        logger.info(f"Hábito creado con éxito: {habit.title} (ID: {habit.id})")
        return habit
    
    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear el hábito: {e}")
        raise e
        

def read_habit(db: Session, habit_id: int):
    try:
        habit = db.query(Habit).filter(Habit.id == habit_id).first()
        if not habit:
            logger.warning(f"No se encontró el hábito con ID: {habit_id}")
            return None
            
        return habit
    
    except Exception as e:
        logger.error(f"Error al buscar el hábito: {e}")
        return None


def get_habits_by_user(db: Session, user_id: int):
    try:
        habits = db.query(Habit).filter(Habit.user_id == user_id).all()
        return habits
    except Exception as e:
        logger.error(f"Error al listar los hábitos del usuario: {e}")
        return []
        

def update_habit(db: Session, habit_id: int, title: str = None, description: str = None, frequency_type: Freq = None, target_days: list = None, status: Status = None):
    try:
        habit = db.query(Habit).filter(Habit.id == habit_id).first()
        
        if not habit:
            logger.warning(f"No se encontró el hábito con ID: {habit_id}")
            return None
            
        if title is not None:
            habit.title = title
        if description is not None:
            habit.description = description
        if frequency_type is not None:
            habit.frequency_type = frequency_type
        if target_days is not None:
            habit.target_days = target_days
        if status is not None:
            habit.status = status
            
        db.commit()
        db.refresh(habit)
        
        logger.info(f"Hábito actualizado con éxito: {habit.title}")
        return habit
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error al actualizar el hábito: {e}")
        raise e
        

def delete_habit(db: Session, habit_id: int):
    try:
        habit = db.query(Habit).filter(Habit.id == habit_id).first()
        
        if not habit:
            logger.warning(f"No se encontró el hábito con ID: {habit_id}")
            return False
            
        db.delete(habit)
        db.commit()        
        logger.info(f"Hábito con ID {habit_id} eliminado correctamente.")
        return True
    
    except Exception as e:
        db.rollback()
        logger.error(f"Error al eliminar el hábito: {e}")
        raise e