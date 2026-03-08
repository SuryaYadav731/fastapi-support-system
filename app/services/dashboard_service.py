from sqlalchemy.orm import Session
from app.models.ticket_model import Ticket
from app.models.user_model import User
from sqlalchemy import func


def get_dashboard_stats(db: Session, user):

    if user.role == "admin":

        total_users = db.query(User).count()
        total_tickets = db.query(Ticket).count()
        open_tickets = db.query(Ticket).filter(Ticket.status == "open").count()
        resolved = db.query(Ticket).filter(Ticket.status == "resolved").count()

        return {
            "role": "admin",
            "total_users": total_users,
            "total_tickets": total_tickets,
            "open": open_tickets,
            "resolved": resolved
        }

    elif user.role == "agent":

        assigned = db.query(Ticket).filter(Ticket.agent_id == user.id).count()
        open_tickets = db.query(Ticket).filter(
            Ticket.agent_id == user.id,
            Ticket.status == "open"
        ).count()

        resolved = db.query(Ticket).filter(
            Ticket.agent_id == user.id,
            Ticket.status == "resolved"
        ).count()

        return {
            "role": "agent",
            "assigned": assigned,
            "open": open_tickets,
            "resolved": resolved
        }

    else:  # customer

        my_tickets = db.query(Ticket).filter(Ticket.user_id == user.id).count()

        open_tickets = db.query(Ticket).filter(
            Ticket.user_id == user.id,
            Ticket.status == "open"
        ).count()

        resolved = db.query(Ticket).filter(
            Ticket.user_id == user.id,
            Ticket.status == "resolved"
        ).count()

        return {
            "role": "customer",
            "my_tickets": my_tickets,
            "open": open_tickets,
            "resolved": resolved
        }
        



def tickets_by_status(db: Session):

    result = db.query(
        Ticket.status,
        func.count(Ticket.id)
    ).group_by(Ticket.status).all()

    return {status: count for status, count in result}


def tickets_by_priority(db: Session):

    result = db.query(
        Ticket.priority,
        func.count(Ticket.id)
    ).group_by(Ticket.priority).all()

    return {priority: count for priority, count in result}


def monthly_ticket_trend(db: Session):

    result = db.query(
        func.date_trunc("month", Ticket.created_at),
        func.count(Ticket.id)
    ).group_by(func.date_trunc("month", Ticket.created_at)).all()

    return {
        str(month.date()): count
        for month, count in result
    }