from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MLRequestBase(BaseModel):
    ml_model_version: Optional[str]
    raw_ml_response: Optional[dict]

class MLRequestCreate(MLRequestBase):
    email_id: int

class MLRequestRead(MLRequestBase):
    id: int
    email_id: int
    sent_to_ml_at: datetime
    created_at: datetime

    model_config = {
        "from_attributes": True
    }