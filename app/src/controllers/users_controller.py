from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from src.models.database import get_db
from src.schemas.users_schema import UserCreate, UserResponse
from src.services import users_service

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_new_user(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = users_service.create_user(db=db, username=user_data.username, email=user_data.email, password=user_data.password)
        
        if not new_user:
            raise HTTPException(status_code=400, detail="Username or email already exists.")
            
        return new_user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = users_service.get_user_by_id(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}")
def delete_existing_user(user_id: int, db: Session = Depends(get_db)):
    success = users_service.delete_user(db=db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User and all related data deleted successfully"}