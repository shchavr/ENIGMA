from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, JSON
from sqlalchemy.sql import func

from app.db.base import Base


class MLRequest(Base):
    __tablename__ = "ml_requests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email_id = Column(Integer, ForeignKey("emails.id"), nullable=False)
    sent_to_ml_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    ml_model_version = Column(String)
    raw_ml_response = Column(JSON)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
