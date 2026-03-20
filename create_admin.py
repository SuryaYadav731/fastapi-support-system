from app.database import SessionLocal
from app.models.user_model import User
from app.core.security import hash_password


def create_admin():

    db = SessionLocal()

    admin = User(
        name="Surya ",
        email="suryayadav222003@gmail.com",
        password=hash_password(""),
        role="admin"
    )

    db.add(admin)
    db.commit()

    print("Admin created successfully")


if __name__ == "__main__":
    create_admin()