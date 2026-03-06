from sqlalchemy.orm import Session
from app.models.user_model import User


def create_user(db: Session, user_data):

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=user_data.password,
        role="customer",
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_user_by_email(db: Session, email: str):

    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int):

    return db.query(User).filter(User.id == user_id).first()
