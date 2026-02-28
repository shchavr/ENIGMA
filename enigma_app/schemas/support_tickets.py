from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SupportTicketBase(BaseModel):
    full_name: Optional[str]
    company: Optional[str]
    phone: Optional[str]
    device_model: Optional[str]
    serial_numbers: Optional[str]
    category: Optional[str]
    sentiment: Optional[str]
    problem_summary: Optional[str]

class SupportTicketCreate(SupportTicketBase):
    email_id: int

class SupportTicketRead(BaseModel):
    id: int
    email_id: int

    full_name: str | None
    company: str | None
    phone: str | None
    device_model: str | None
    serial_numbers: str | None
    category: str | None
    sentiment: str | None
    problem_summary: str | None
    status: str

    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

class TicketRead(BaseModel):
    id: int
    date: str
    full_name: str
    subject: str
    object: str
    phone: str
    email: str
    serial_numbers: str
    device_model: str
    sentiment: str
    raw_body: str
    status: str
    ai_generated_response: str | None

    class Config:
        from_attributes = True


class TicketReplyRequest(BaseModel):
    subject: str
    body: str