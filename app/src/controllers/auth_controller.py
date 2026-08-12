from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.models.database import get_db
from src.schemas.users_schema import UserCreate, UserResponse, LoginRequest
from src.services import users_service
from src.services.auth_service import authenticate_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    new_user = users_service.create_user(db=db, username=user_data.username, email=user_data.email, password=user_data.password)
    if not new_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El nombre de usuario o correo electrónico ya está registrado.")
    return new_user

@router.post("/login", response_model=UserResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db=db, username_or_email=login_data.username_or_email, password=login_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales incorrectas (usuario/email o contraseña)")
    return user
