from sqlalchemy import Column, Integer, String, TIMESTAMP, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from enigma_app.db.base import Base


class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(String, unique=True, nullable=False)
    sender_email = Column(String, nullable=False)
    subject = Column(String)
    body = Column(Text, nullable=False)
    received_at = Column(TIMESTAMP(timezone=True), nullable=False)
    processing_status = Column(String, default="received")
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    tickets = relationship("SupportTicket", back_populates="email")