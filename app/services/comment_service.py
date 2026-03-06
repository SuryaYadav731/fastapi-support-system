from sqlalchemy.orm import Session
from app.repository import comment_repository
from app.schemas.comment_schema import CommentCreate


def add_comment(db: Session, comment_data: CommentCreate, user_id: int):

    return comment_repository.add_comment(db, comment_data, user_id)


def get_comments(db: Session, ticket_id: int):

    return comment_repository.get_comments_by_ticket(db, ticket_id)
