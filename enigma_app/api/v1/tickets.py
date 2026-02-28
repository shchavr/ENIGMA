from typing import List


from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from enigma_app.api.deps import get_current_admin
from enigma_app.db import SupportTicket
from enigma_app.db.session import get_db
from enigma_app.schemas.support_tickets import SupportTicketRead

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.get("/", response_model=List[SupportTicketRead])
def get_tickets(
        db: Session = Depends(get_db),
        admin: dict = Depends(get_current_admin),
):
    """Получение всех тикетов (только для админов)."""
    tickets = (
        db.query(SupportTicket)
        .order_by(SupportTicket.created_at.desc())
        .all()
    )
    return tickets
