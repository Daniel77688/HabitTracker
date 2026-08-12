from sqlalchemy.orm import Session
from src.models.user_model import User
from src.services.security import verify_password


def authenticate_user(db: Session, username_or_email: str, password: str) -> User:
    user = db.query(User).filter((User.username == username_or_email) | (User.email == username_or_email)).first()
    if not user or not verify_password(password, user.password_hash):
        return None
    return user
