from pydantic import BaseModel
from datetime import datetime

class MessageCreate(BaseModel):

    message: str


class MessageResponse(BaseModel):

    id: int
    message: str
    sender_id: int
    created_at: datetime

    class Config:
        from_attributes = True