from sqlalchemy.orm import Session
from app.models.ticket_model import Ticket
from sqlalchemy.orm import Session
from app.models.ticket_model import Ticket
from app.schemas.ticket_schema import TicketCreate


def create_ticket(
    db: Session,
    title: str,
    description: str,
    priority: str,
    user_id: int,
    file_path: str | None = None
):

    ticket = Ticket(
        title=title,
        description=description,
        priority=priority,
        user_id=user_id,
        attachment=file_path
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket

def create_ticket(
    db: Session,
    title: str,
    description: str,
    priority: str,
    user_id: int,
    file_path: str | None = None
):

    ticket = Ticket(
        title=title,
        description=description,
        priority=priority,
        user_id=user_id,
        attachment=file_path
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket


def get_all_tickets(
    db,
    skip: int,
    limit: int
):

    return (
        db.query(Ticket)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_ticket_by_id(db: Session, ticket_id: int):

    return db.query(Ticket).filter(Ticket.id == ticket_id).first()


def update_ticket_status(db: Session, ticket_id: int, status: str):

    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if ticket:
        ticket.status = status
        db.commit()
        db.refresh(ticket)

    return ticket


def assign_ticket(db, ticket_id: int, agent_id: int):

    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if ticket:
        ticket.agent_id = agent_id
        ticket.status = "in_progress"

        db.commit()
        db.refresh(ticket)

    return ticket


def update_ticket_status(db, ticket_id: int, status: str):

    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if ticket:
        ticket.status = status
        db.commit()
        db.refresh(ticket)

    return ticket


def get_tickets_paginated(db, skip: int, limit: int):

    return db.query(Ticket).offset(skip).limit(limit).all()


def get_tickets_filtered(
    db,
    skip: int,
    limit: int,
    status: str = None,
    priority: str = None,
    search: str = None,
):

    query = db.query(Ticket)

    if status:
        query = query.filter(Ticket.status == status)

    if priority:
        query = query.filter(Ticket.priority == priority)

    if search:
        query = query.filter(Ticket.title.ilike(f"%{search}%"))

    return query.offset(skip).limit(limit).all()


def add_attachment(db, ticket_id: int, file_path: str):

    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if ticket:
        ticket.attachment = file_path
        db.commit()
        db.refresh(ticket)

    return ticket
def get_tickets_by_user(
    db,
    user_id: int,
    skip: int,
    limit: int
):

    return (
        db.query(Ticket)
        .filter(Ticket.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )