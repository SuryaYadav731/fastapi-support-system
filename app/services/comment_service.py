from fastapi import HTTPException
from app.repository import comment_repository


def get_comments_by_ticket(db, ticket_id):

    return comment_repository.get_comments_by_ticket(db, ticket_id)


def create_comment(db, data, user_id):

    return comment_repository.create_comment(
        db,
        data,
        user_id
    )


def update_comment(db, comment_id, data, user):

    comment = comment_repository.get_comment(db, comment_id)

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.user_id != user.id and user.role not in ["admin","agent"]:
        raise HTTPException(status_code=403, detail="Not allowed")

    return comment_repository.update_comment(db, comment_id, data)


def delete_comment(db, comment_id, user):

    comment = comment_repository.get_comment(db, comment_id)

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.user_id != user.id and user.role not in ["admin","agent"]:
        raise HTTPException(status_code=403, detail="Not allowed")

    return comment_repository.delete_comment(db, comment_id)