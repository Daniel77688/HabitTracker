from src.models.database import SessionLocal
from src.models.habit_model import Habit, Freq, Status

def create_habit(user_id: int, title: str, description: str = None, frequency_type: Freq = Freq.daily, target_days: list = None):
    db = SessionLocal()
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
        
        print(f"Hábito creado con éxito: {habit}")
        return habit
    
    except Exception as e:
        db.rollback()
        print(f"Error al crear el hábito: {e}")
        raise e
    finally:
        db.close()
        

def read_habit(habit_id: int):
    db = SessionLocal()
    try:
        habit = db.query(Habit).filter(Habit.id == habit_id).first()
        if not habit:
            print(f"No se encontró el hábito con ID: {habit_id}")
            return None
            
        return habit
    
    except Exception as e:
        print(f"Error al buscar el hábito: {e}")
        return None
    finally:
        db.close()


def get_habits_by_user(user_id: int):
    db = SessionLocal()
    try:
        habits = db.query(Habit).filter(Habit.user_id == user_id).all()
        return habits
    except Exception as e:
        print(f"Error al listar los hábitos del usuario: {e}")
        return []
    finally:
        db.close()
        

def update_habit(habit_id: int, title: str = None, description: str = None, frequency_type: Freq = None, target_days: list = None, status: Status = None):
    db = SessionLocal()
    try:
        habit = db.query(Habit).filter(Habit.id == habit_id).first()
        
        if not habit:
            print(f"No se encontró el hábito con ID: {habit_id}")
            return False
            
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
        
        print(f"Hábito actualizado con éxito: {habit}")
        return habit
        
    except Exception as e:
        db.rollback()
        print(f"Error al actualizar el hábito: {e}")
        raise e
    finally:
        db.close()
        

def delete_habit(habit_id: int):
    db = SessionLocal()
    try:
        habit = db.query(Habit).filter(Habit.id == habit_id).first()
        
        if not habit:
            print(f"No se encontró el hábito con ID: {habit_id}")
            return False
            
        db.delete(habit)
        db.commit()        
        print(f"Hábito con ID {habit_id} eliminado correctamente.")
        return True
    
    except Exception as e:
        db.rollback()
        print(f"Error al eliminar el hábito: {e}")
        raise e
    finally:
        db.close()