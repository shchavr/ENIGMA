from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin
from app.db import Email
from app.db.session import get_db
from app.schemas.emails import EmailRead

router = APIRouter(prefix="/emails", tags=["emails"])


@router.get("/", response_model=List[EmailRead])
def get_emails(
        db: Session = Depends(get_db),
        admin: dict = Depends(get_current_admin)
):
    """Получение всех писем (только для админов)."""
    emails = db.query(Email).order_by(Email.received_at.desc()).all()
    return emails
