from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Comment(Base):

    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)

    ticket_id = Column(Integer, ForeignKey("tickets.id"))

    user_id = Column(Integer, ForeignKey("users.id"))

    message = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)

    ticket = relationship("Ticket")

    user = relationship("User")
