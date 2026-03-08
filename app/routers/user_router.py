from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.db_dependencies import get_db
from app.dependencies.auth_dependencies import get_current_user
from app.dependencies.role_dependencies import require_role

from app.schemas.user_schema import UserProfile, UpdateProfile, ChangePassword, UserCreate
from app.models.user_model import User

from app.services import user_service
from app.core.security import hash_password


router = APIRouter(prefix="/users", tags=["Users"])


# ================================
# USER PROFILE
# ================================

# 1️⃣ Get Profile
@router.get("/me", response_model=UserProfile)
def get_profile(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return user_service.get_profile(db, current_user.id)


# 2️⃣ Update Profile
@router.put("/update")
def update_profile(
    data: UpdateProfile,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return user_service.update_profile(db, current_user.id, data.name)


# 3️⃣ Change Password
@router.put("/change-password")
def change_password(
    data: ChangePassword,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return user_service.change_password(
        db,
        current_user.id,
        data.old_password,
        data.new_password
    )


# ================================
# ADMIN FUNCTIONS
# ================================

# 4️⃣ Get All Users (Admin only)
@router.get("/")
def get_users(
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["admin"]))
):

    users = db.query(User).all()

    return users


# 5️⃣ Create Agent (Admin only)
@router.post("/create-agent")
def create_agent(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["admin"]))
):

    agent = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        role="agent"
    )

    db.add(agent)
    db.commit()
    db.refresh(agent)

    return agent


# 6️⃣ Change User Role
@router.put("/change-role/{user_id}")
def change_role(
    user_id: int,
    role: str,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["admin"]))
):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = role

    db.commit()

    return {"message": "Role updated successfully"}


# 7️⃣ Deactivate User
@router.put("/deactivate/{user_id}")
def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role(["admin"]))
):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = False

    db.commit()

    return {"message": "User deactivated successfully"}

@router.get("/agents")
def get_agents(
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["admin"]))
):

    agents = db.query(User).filter(User.role == "agent").all()

    return agents