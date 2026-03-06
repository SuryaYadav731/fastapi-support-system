from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import SessionLocal
from app.models.ticket_model import Ticket
from app.dependencies.db_dependencies import get_db
from app.dependencies.role_dependencies import require_role

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/dashboard")
def get_dashboard(
    db: Session = Depends(get_db), current_user=Depends(require_role(["admin"]))
):

    total_tickets = db.query(Ticket).count()

    open_tickets = db.query(Ticket).filter(Ticket.status == "open").count()

    resolved_tickets = db.query(Ticket).filter(Ticket.status == "resolved").count()

    return {
        "total_tickets": total_tickets,
        "open_tickets": open_tickets,
        "resolved_tickets": resolved_tickets,
    }


@router.get("/tickets-per-day")
def tickets_per_day(
    db: Session = Depends(get_db), current_user=Depends(require_role(["admin"]))
):

    result = (
        db.query(func.date(Ticket.created_at), func.count(Ticket.id))
        .group_by(func.date(Ticket.created_at))
        .all()
    )

    data = []

    for date, count in result:
        data.append({"date": str(date), "tickets": count})

    return data


@router.get("/agent-performance")
def agent_performance(
    db: Session = Depends(get_db), current_user=Depends(require_role(["admin"]))
):

    result = (
        db.query(Ticket.agent_id, func.count(Ticket.id))
        .filter(Ticket.status == "resolved")
        .group_by(Ticket.agent_id)
        .all()
    )

    data = []

    for agent_id, count in result:
        data.append({"agent_id": agent_id, "resolved_tickets": count})

    return data
