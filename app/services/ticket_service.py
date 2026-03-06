from sqlalchemy.orm import Session
from app.repository import ticket_repository
from app.schemas.ticket_schema import TicketCreate


def create_ticket(db: Session, ticket_data: TicketCreate, user_id: int):

    return ticket_repository.create_ticket(db, ticket_data, user_id)


def get_all_tickets(db: Session):

    return ticket_repository.get_all_tickets(db)


def get_ticket_by_id(db: Session, ticket_id: int):

    ticket = ticket_repository.get_ticket_by_id(db, ticket_id)

    if not ticket:
        raise Exception("Ticket not found")

    return ticket


def assign_ticket(db, ticket_id: int, agent_id: int):

    return ticket_repository.assign_ticket(db, ticket_id, agent_id)


def update_ticket_status(db, ticket_id: int, status: str):

    return ticket_repository.update_ticket_status(db, ticket_id, status)


def get_tickets_filtered(
    db,
    page: int,
    limit: int,
    status: str = None,
    priority: str = None,
    search: str = None,
):

    skip = (page - 1) * limit

    return ticket_repository.get_tickets_filtered(
        db,
        skip,
        limit,
        status,
        priority,
        search,
    )


def upload_attachment(db, ticket_id: int, file_path: str):

    return ticket_repository.add_attachment(db, ticket_id, file_path)
