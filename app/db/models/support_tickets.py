from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class SupportTicket(Base):
    __tablename__ = "support_tickets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email_id = Column(Integer, ForeignKey("emails.id"), nullable=False)

    full_name = Column(String)
    company = Column(String)
    phone = Column(String)
    device_model = Column(String)
    serial_numbers = Column(String)
    category = Column(String)
    sentiment = Column(String)  # positive, neutral, negative
    problem_summary = Column(Text)

    status = Column(String, default="new")  # new, answered, closed
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    email = relationship("Email")
    responses = relationship("Response", backref="ticket")
    logs = relationship("AdminLog", backref="ticket")