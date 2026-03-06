from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.comment_schema import CommentCreate, CommentResponse
from app.services import comment_service

from app.dependencies.db_dependencies import get_db
from app.dependencies.auth_dependencies import get_current_user


router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/", response_model=CommentResponse)
def add_comment(
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    return comment_service.add_comment(db, comment, current_user.id)


@router.get("/{ticket_id}", response_model=list[CommentResponse])
def get_comments(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    return comment_service.get_comments(db, ticket_id)
