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

class SupportTicketRead(SupportTicketBase):
    id: int
    email_id: int
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }