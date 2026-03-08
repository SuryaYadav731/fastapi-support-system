from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.dependencies.db_dependencies import get_db
from app.dependencies.role_dependencies import require_role
from app.models.ticket_model import Ticket

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


# -----------------------------
# Dashboard Summary
# -----------------------------
@router.get("/dashboard")
def get_dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["admin"]))
):

    total_tickets = db.query(Ticket).count()

    open_tickets = db.query(Ticket).filter(Ticket.status == "open").count()

    resolved_tickets = db.query(Ticket).filter(Ticket.status == "resolved").count()

    closed_tickets = db.query(Ticket).filter(Ticket.status == "closed").count()

    high_priority = db.query(Ticket).filter(Ticket.priority == "high").count()

    medium_priority = db.query(Ticket).filter(Ticket.priority == "medium").count()

    low_priority = db.query(Ticket).filter(Ticket.priority == "low").count()

    return {
        "total_tickets": total_tickets,
        "status": {
            "open": open_tickets,
            "resolved": resolved_tickets,
            "closed": closed_tickets
        },
        "priority": {
            "high": high_priority,
            "medium": medium_priority,
            "low": low_priority
        }
    }


# -----------------------------
# Tickets Per Day Chart
# -----------------------------
@router.get("/tickets-per-day")
def tickets_per_day(
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["admin"]))
):

    result = (
        db.query(func.date(Ticket.created_at), func.count(Ticket.id))
        .group_by(func.date(Ticket.created_at))
        .all()
    )

    data = []

    for date, count in result:
        data.append({
            "date": str(date),
            "tickets": count
        })

    return data


# -----------------------------
# Agent Performance
# -----------------------------
@router.get("/agent-performance")
def agent_performance(
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["admin"]))
):

    result = (
        db.query(Ticket.agent_id, func.count(Ticket.id))
        .filter(Ticket.status == "resolved")
        .group_by(Ticket.agent_id)
        .all()
    )

    data = []

    for agent_id, count in result:
        data.append({
            "agent_id": agent_id,
            "resolved_tickets": count
        })

    return data