from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Ticket(Base):

    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    description = Column(Text)

    status = Column(String, default="open")

    priority = Column(String, default="medium")

    user_id = Column(Integer, ForeignKey("users.id"))

    agent_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", foreign_keys=[user_id])

    agent = relationship("User", foreign_keys=[agent_id])
    attachment = Column(String, nullable=True)
