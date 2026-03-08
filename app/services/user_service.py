from fastapi import HTTPException
from app.repository import user_repository
from app.core.security import verify_password, hash_password
from sqlalchemy.orm import Session
from app.models.user_model import User


def get_profile(db: Session, user_id: int):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise Exception("User not found")

    return user

def update_profile(db, user_id, name):

    return user_repository.update_user_name(db, user_id, name)


def change_password(db, user_id, old_password, new_password):

    user = user_repository.get_user_by_id(db, user_id)

    if not verify_password(old_password, user.password):

        raise HTTPException(status_code=400, detail="Old password incorrect")

    hashed = hash_password(new_password)

    return user_repository.update_user_password(db, user_id, hashed)