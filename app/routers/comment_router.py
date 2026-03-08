from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.db_dependencies import get_db
from app.dependencies.auth_dependencies import get_current_user
from app.schemas.comment_schema import CommentCreate, CommentUpdate
from app.services import comment_service

router = APIRouter(prefix="/comments", tags=["Comments"])


# ===============================
# Get comments by ticket
# ===============================
@router.get("/ticket/{ticket_id}")
def get_comments(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return comment_service.get_comments_by_ticket(db, ticket_id)


# ===============================
# Add comment
# ===============================
@router.post("/")
def add_comment(
    data: CommentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return comment_service.create_comment(
        db,
        data,
        current_user.id
    )


# ===============================
# Update comment
# ===============================
@router.put("/{comment_id}")
def update_comment(
    comment_id: int,
    data: CommentUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return comment_service.update_comment(
        db,
        comment_id,
        data,
        current_user
    )


# ===============================
# Delete comment
# ===============================
@router.delete("/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return comment_service.delete_comment(
        db,
        comment_id,
        current_user
    )