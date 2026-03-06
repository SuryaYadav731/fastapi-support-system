from sqlalchemy.orm import Session
from app.models.comment_model import Comment


def add_comment(db: Session, comment_data, user_id):

    new_comment = Comment(
        ticket_id=comment_data.ticket_id, message=comment_data.message, user_id=user_id
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment


def get_comments_by_ticket(db: Session, ticket_id: int):

    return db.query(Comment).filter(Comment.ticket_id == ticket_id).all()
