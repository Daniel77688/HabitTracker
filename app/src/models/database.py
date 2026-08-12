import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../../habits.db")

engine = create_engine(f"sqlite:///{DB_PATH}", echo=True) # True = U can see Querys in Terminal

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def init_db():
    """Create the ddbb tables if they dont already exist"""
    
    import src.models.habit_model  # noqa: F401
    import src.models.habit_log_model
    import src.models.streak_model
    import src.models.user_model
    
    Base.metadata.create_all(bind=engine)
    
    print(" > DataBase successfully initialized.\n\n")

def get_db():
    """Dependency generator for database sessions in FastAPI routes"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()