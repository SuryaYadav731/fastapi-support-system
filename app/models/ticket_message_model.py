from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from app.database import Base

class TicketMessage(Base):

    __tablename__ = "ticket_messages"

    id = Column(Integer, primary_key=True, index=True)

    ticket_id = Column(Integer, ForeignKey("tickets.id"))

    sender_id = Column(Integer, ForeignKey("users.id"))

    message = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)