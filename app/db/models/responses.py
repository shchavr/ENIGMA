from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Response(Base):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticket_id = Column(Integer, ForeignKey("support_tickets.id"), nullable=False)
    ml_request_id = Column(Integer, ForeignKey("ml_requests.id"), nullable=True)

    response_text = Column(Text)
    is_ai_generated = Column(Boolean, default=True)
    sent_to_user = Column(Boolean, default=False)
    sent_at = Column(TIMESTAMP(timezone=True))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    ticket = relationship("SupportTicket", back_populates="responses")