from fastapi import APIRouter, HTTPException
from src.schemas.users_schema import UserCreate, UserResponse
from src.services import user_service

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=dict)
def create_new_user(user_data: UserCreate):
    try:
        new_user = user_service.create_user(username=user_data.username, email=user_data.email, password_hash=user_data.password_hash)
        
        if not new_user:
            raise HTTPException(status_code=400, detail="Username or email already exists.")
            
        return {"message": "User created successfully", "user_id": new_user.id}
    except Exception as e: raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    user = user_service.get_user_by_id(user_id)
    if not user: raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}")
def delete_existing_user(user_id: int):
    success = user_service.delete_user(user_id)
    if not success: raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User and all related data deleted successfully"}