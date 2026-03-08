from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import os
from app.repository import ticket_repository
from app.schemas.ticket_schema import TicketCreate


# ======================================
# Create Ticket
# ======================================
def create_ticket(
    db: Session,
    title: str,
    description: str,
    priority: str,
    user_id: int,
    file=None
):

    file_path = None

    if file:
        upload_folder = "uploads"
        os.makedirs(upload_folder, exist_ok=True)

        file_path = f"{upload_folder}/{file.filename}"

        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

    ticket = ticket_repository.create_ticket(
        db,
        title,
        description,
        priority,
        user_id,
        file_path
    )

    return ticket

# ======================================
# Get All Tickets
# ======================================
def get_all_tickets(db: Session):

    return ticket_repository.get_all_tickets(db)


# ======================================
# Get Ticket By ID
# ======================================
def get_ticket_by_id(
    db: Session,
    ticket_id: int
):

    ticket = ticket_repository.get_ticket_by_id(
        db,
        ticket_id
    )

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    return ticket


# ======================================
# Assign Ticket to Agent
# ======================================
def assign_ticket(
    db: Session,
    ticket_id: int,
    agent_id: int
):

    ticket = ticket_repository.assign_ticket(
        db,
        ticket_id,
        agent_id
    )

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    return ticket


# ======================================
# Update Ticket Status
# ======================================
def update_ticket_status(
    db: Session,
    ticket_id: int,
    status: str
):

    ticket = ticket_repository.update_ticket_status(
        db,
        ticket_id,
        status
    )

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    return ticket


# ======================================
# Filter + Pagination
# ======================================
def get_tickets_filtered(
    db: Session,
    page: int,
    limit: int,
    status: str | None = None,
    priority: str | None = None,
    search: str | None = None,
):

    skip = (page - 1) * limit

    return ticket_repository.get_tickets_filtered(
        db,
        skip,
        limit,
        status,
        priority,
        search
    )


# ======================================
# Upload Ticket Attachment
# ======================================
def upload_attachment(
    db: Session,
    ticket_id: int,
    file_path: str
):

    ticket = ticket_repository.add_attachment(
        db,
        ticket_id,
        file_path
    )

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    return ticket


def get_tickets_by_role(
    db,
    user,
    page: int,
    limit: int
):

    skip = (page - 1) * limit

    # Customer → only own tickets
    if user.role == "customer":

        return ticket_repository.get_tickets_by_user(
            db,
            user.id,
            skip,
            limit
        )

    # Admin / Agent → all tickets
    return ticket_repository.get_all_tickets(
        db,
        skip,
        limit
    )