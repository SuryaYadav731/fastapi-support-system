from sqlalchemy.orm import Session
from app.repository import user_repository
from app.schemas.user_schema import UserCreate
from app.schemas.auth_schema import LoginRequest
from app.core.security import hash_password, verify_password
from app.core.jwt_handler import create_access_token


def register_user(db: Session, user_data: UserCreate):

    existing_user = user_repository.get_user_by_email(db, user_data.email)

    if existing_user:
        raise Exception("Email already registered")

    user_data.password = hash_password(user_data.password)

    return user_repository.create_user(db, user_data)


def login_user(db: Session, login_data: LoginRequest):

    user = user_repository.get_user_by_email(db, login_data.email)

    if not user:
        raise Exception("Invalid email")

    if not verify_password(login_data.password, user.password):
        raise Exception("Invalid password")

    token = create_access_token({"user_id": user.id})

    return {"access_token": token, "token_type": "bearer"}


def create_admin_if_not_exists(db):

    from app.models.user_model import User
    from app.core.security import hash_password

    admin = db.query(User).filter(User.role == "admin").first()

    if not admin:

        admin_user = User(
            name="Admin",
            email="suryayadav7310@gmail.com",
            password=hash_password("Surya@123"),
            role="admin",
            is_active=True
        )

        db.add(admin_user)
        db.commit()

        print("Admin user created")