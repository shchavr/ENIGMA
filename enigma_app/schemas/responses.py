from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ResponseBase(BaseModel):
    response_text: str
    is_ai_generated: Optional[bool] = True
    sent_to_user: Optional[bool] = False

class ResponseCreate(ResponseBase):
    ticket_id: int
    ml_request_id: Optional[int]

class ResponseRead(ResponseBase):
    id: int
    ticket_id: int
    ml_request_id: Optional[int]
    sent_at: Optional[datetime]
    created_at: datetime

    model_config = {
        "from_attributes": True
    }