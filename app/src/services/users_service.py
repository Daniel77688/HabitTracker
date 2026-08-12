import logging
from sqlalchemy.orm import Session
from src.models.user_model import User
from src.services.security import hash_password

logger = logging.getLogger(__name__)

def create_user(db: Session, username: str, email: str, password: str):
    try:
        existing_user = db.query(User).filter((User.username == username) | (User.email == email)).first()

        if existing_user:
            logger.warning("El usuario o email ya está registrado.")
            return None

        hashed_pwd = hash_password(password)
        nuevo_usuario = User(username=username, email=email, password_hash=hashed_pwd)
        
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        
        logger.info(f"Usuario creado con éxito: {nuevo_usuario.username}")
        return nuevo_usuario

    except Exception as e:
        db.rollback()
        logger.error(f"Error al crear el usuario: {e}")
        raise e


def get_user_by_id(db: Session, user_id: int):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            logger.warning(f"No se encontró el usuario con ID: {user_id}")
            return None
        return user
    except Exception as e:
        logger.error(f"Error al buscar el usuario: {e}")
        return None


def get_user_by_username(db: Session, username: str):
    try:
        user = db.query(User).filter(User.username == username).first()
        return user
    except Exception as e:
        logger.error(f"Error al buscar el usuario por username: {e}")
        return None


def delete_user(db: Session, user_id: int):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            logger.warning(f"No se encontró el usuario con ID {user_id}")
            return False

        db.delete(user)
        db.commit()
        logger.info(f"Usuario (ID: {user_id}) eliminado correctamente.")
        return True

    except Exception as e:
        db.rollback()
        logger.error(f"Error al eliminar el usuario: {e}")
        raise e