from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.user_schema import UserCreate, UserResponse
from app.schemas.auth_schema import LoginRequest, TokenResponse
from app.services import auth_service
from app.dependencies.db_dependencies import get_db


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return auth_service.register_user(db, user)


@router.post("/login", response_model=TokenResponse)
def login_user(login_data: LoginRequest, db: Session = Depends(get_db)):
    return auth_service.login_user(db, login_data)
