from src.models.database import SessionLocal
from src.models.user_model import User

def create_user(username: str, email: str, password_hash: str):
    db = SessionLocal()
    try:
        existing_user = db.query(User).filter((User.username == username) | (User.email == email)).first()

        if existing_user:
            print(f"Error: El usuario o email ya está registrado.")
            return None

        nuevo_usuario = User(username=username, email=email, password_hash=password_hash)
        
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        
        print(f"Usuario creado con éxito: {nuevo_usuario}")
        return nuevo_usuario

    except Exception as e:
        db.rollback()
        print(f"Error al crear el usuario: {e}")
        raise e
    finally:
        db.close()


def get_user_by_id(user_id: int):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            print(f"No se encontró el usuario con ID: {user_id}")
            return None
        return user
    except Exception as e:
        print(f"Error al buscar el usuario: {e}")
        return None
    finally:
        db.close()


def get_user_by_username(username: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        return user
    except Exception as e:
        print(f"Error al buscar el usuario por username: {e}")
        return None
    finally:
        db.close()


def delete_user(user_id: int):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            print(f"No se encontró el usuario con ID {user_id}")
            return False

        db.delete(user)
        db.commit()
        print(f"Usuario (ID: {user_id}) y todos sus datos asociados eliminados correctamente.")
        return True

    except Exception as e:
        db.rollback()
        print(f"Error al eliminar el usuario: {e}")
        raise e
    finally:
        db.close()