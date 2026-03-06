from pydantic import BaseModel
from datetime import datetime


class TicketCreate(BaseModel):
    title: str
    description: str
    priority: str


class TicketResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    priority: str
    user_id: int
    agent_id: int | None
    created_at: datetime

    class Config:
        from_attributes = True


class AssignTicket(BaseModel):
    agent_id: int


class UpdateTicketStatus(BaseModel):
    status: str
