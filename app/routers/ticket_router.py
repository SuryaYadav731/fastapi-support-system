from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.ticket_schema import UpdateTicketStatus
from app.dependencies.role_dependencies import require_role
from app.schemas.ticket_schema import TicketCreate, TicketResponse
from app.services import ticket_service
from app.dependencies.role_dependencies import require_role
from app.dependencies.auth_dependencies import get_current_user
from app.schemas.ticket_schema import AssignTicket
from app.dependencies.role_dependencies import require_role
from app.dependencies.db_dependencies import get_db
from fastapi import UploadFile, File
import shutil
import os
from fastapi import BackgroundTasks
from app.utils.email import send_email
from fastapi_cache.decorator import cache

router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.get("/", response_model=list[TicketResponse])
@cache(expire=60)
def get_tickets(
    page: int = 1,
    limit: int = 10,
    status: str | None = None,
    priority: str | None = None,
    search: str | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["agent", "admin"])),
):

    return ticket_service.get_tickets_filtered(
        db,
        page,
        limit,
        status,
        priority,
        search,
    )


@router.post("/", response_model=TicketResponse)
def create_ticket(
    ticket: TicketCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["customer"])),
):

    new_ticket = ticket_service.create_ticket(db, ticket, current_user.id)

    subject = "Ticket Created"
    body = f"Your ticket '{ticket.title}' has been created."

    background_tasks.add_task(send_email, current_user.email, subject, body)

    return new_ticket


@router.put("/assign/{ticket_id}")
def assign_ticket(
    ticket_id: int,
    data: AssignTicket,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["admin"])),
):

    ticket = ticket_service.assign_ticket(db, ticket_id, data.agent_id)

    subject = "Ticket Assigned"
    body = f"Ticket {ticket.id} has been assigned to you."

    background_tasks.add_task(send_email, "agent@email.com", subject, body)

    return ticket


@router.put("/status/{ticket_id}", response_model=TicketResponse)
def update_ticket_status(
    ticket_id: int,
    data: UpdateTicketStatus,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user=Depends(require_role(["agent", "admin"])),
):

    ticket = ticket_service.update_ticket_status(db, ticket_id, data.status)

    # Send email if ticket resolved
    if data.status == "resolved":

        subject = "Ticket Resolved"
        body = f"Your ticket '{ticket.title}' has been resolved."

        background_tasks.add_task(send_email, ticket.user.email, subject, body)

    return ticket


@router.post("/{ticket_id}/upload")
def upload_ticket_file(
    ticket_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    upload_folder = "uploads"

    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    file_path = f"{upload_folder}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    ticket = ticket_service.upload_attachment(db, ticket_id, file_path)

    return {
        "message": "File uploaded successfully",
        "file_path": file_path,
        "ticket_id": ticket.id,
    }
