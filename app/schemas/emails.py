from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class EmailBase(BaseModel):
    sender_email: EmailStr
    subject: Optional[str]
    body: str


class EmailCreate(EmailBase):
    pass


class EmailRead(BaseModel):
    id: int
    message_id: str
    sender_email: str
    subject: str | None
    body: str
    received_at: datetime
    processing_status: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
