from fastapi import APIRouter, Depends, UploadFile, File, Form, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from fastapi_cache.decorator import cache
import os
import shutil

from app.dependencies.db_dependencies import get_db
from app.dependencies.role_dependencies import require_role
from app.dependencies.auth_dependencies import get_current_user

from app.models.ticket_model import Ticket
from app.models.ticket_message_model import TicketMessage

from app.schemas.ticket_message_schema import MessageCreate
from app.schemas.ticket_schema import (
    TicketResponse,
    AssignTicket,
    UpdateTicketStatus
)

from app.services import ticket_service
from app.utils.email import send_email

router = APIRouter(prefix="/tickets", tags=["Tickets"])


# =====================================
# Get Tickets (Role Based + Pagination)
# =====================================
@router.get("/", response_model=list[TicketResponse])
@cache(expire=60)
def get_tickets(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return ticket_service.get_tickets_by_role(
        db,
        current_user,
        page,
        limit
    )


# =====================================
# Create Ticket (Customer)
# =====================================
@router.post("/", response_model=TicketResponse)
def create_ticket(
    title: str = Form(...),
    description: str = Form(...),
    priority: str = Form(...),
    file: UploadFile | None = File(None),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["customer"]))
):

    ticket = ticket_service.create_ticket(
        db,
        title,
        description,
        priority,
        current_user.id,
        file
    )

    # Send email notification
    subject = "Ticket Created"
    body = f"Your ticket '{title}' has been created."

    if background_tasks:
        background_tasks.add_task(
            send_email,
            current_user.email,
            subject,
            body
        )

    return ticket


# =====================================
# Assign Ticket (Admin)
# =====================================
@router.put("/{ticket_id}/assign", response_model=TicketResponse)
def assign_ticket(
    ticket_id: int,
    data: AssignTicket,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["admin"]))
):

    ticket = ticket_service.assign_ticket(
        db,
        ticket_id,
        data.agent_id
    )

    subject = "Ticket Assigned"
    body = f"Ticket {ticket.id} has been assigned to you."

    background_tasks.add_task(
        send_email,
        "agent@email.com",
        subject,
        body
    )

    return ticket


# =====================================
# Update Ticket Status (Agent/Admin)
# =====================================
@router.patch("/{ticket_id}/status", response_model=TicketResponse)
def update_ticket_status(
    ticket_id: int,
    data: UpdateTicketStatus,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["agent", "admin"]))
):

    ticket = ticket_service.update_ticket_status(
        db,
        ticket_id,
        data.status
    )

    if data.status == "resolved":

        subject = "Ticket Resolved"
        body = f"Your ticket '{ticket.title}' has been resolved."

        background_tasks.add_task(
            send_email,
            ticket.user.email,
            subject,
            body
        )

    return ticket


# =====================================
# Upload Ticket Attachment
# =====================================
@router.post("/{ticket_id}/upload")
def upload_ticket_file(
    ticket_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    upload_folder = "uploads"
    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    ticket = ticket_service.upload_attachment(
        db,
        ticket_id,
        file_path
    )

    return {
        "message": "File uploaded successfully",
        "file_path": file_path,
        "ticket_id": ticket.id
    }


# =====================================
# Agent → My Assigned Tickets
# =====================================
@router.get("/my-tickets")
def get_my_tickets(
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["agent"]))
):

    tickets = db.query(Ticket).filter(
        Ticket.agent_id == current_user.id
    ).all()

    return tickets


# =====================================
# Reply System (Customer ↔ Agent)
# =====================================
@router.post("/{ticket_id}/reply")
def reply_ticket(
    ticket_id: int,
    data: MessageCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    message = TicketMessage(
        ticket_id=ticket_id,
        sender_id=current_user.id,
        message=data.message
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return {
        "message": "Reply added successfully",
        "data": message
    }