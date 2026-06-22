from fastapi import APIRouter
from backend.schemas.user import UserResponse, UserCreate

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register_user(user_in: UserCreate):
    """Stub for user registration."""
    import datetime
    return {
        "id": 1,
        "email": user_in.email,
        "created_at": datetime.datetime.utcnow(),
        "updated_at": datetime.datetime.utcnow()
    }
