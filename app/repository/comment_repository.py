from app.models.comment_model import Comment


def get_comments_by_ticket(db, ticket_id):

    return (
        db.query(Comment)
        .filter(Comment.ticket_id == ticket_id)
        .order_by(Comment.created_at)
        .all()
    )


def create_comment(db, data, user_id):

    comment = Comment(
        ticket_id=data.ticket_id,
        message=data.message,
        user_id=user_id
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment


def get_comment(db, comment_id):

    return db.query(Comment).filter(Comment.id == comment_id).first()


def update_comment(db, comment_id, data):

    comment = db.query(Comment).filter(Comment.id == comment_id).first()

    comment.message = data.message

    db.commit()
    db.refresh(comment)

    return comment


def delete_comment(db, comment_id):

    comment = db.query(Comment).filter(Comment.id == comment_id).first()

    db.delete(comment)
    db.commit()

    return {"message": "Comment deleted"}