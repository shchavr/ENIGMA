from datetime import datetime

from sqlalchemy.orm import Session

from app.db import Email, SupportTicket, MLRequest


def process_email_with_ml(email_obj: Email):
    """
    Заглушка ML: возвращает словарь с нужными полями.
    На практике здесь вызов модели или API.
    """
    return {
        "full_name": "Иван Иванов",
        "company": "ООО Ромашка",
        "phone": "+79991234567",
        "device_model": "iPhone 14",
        "serial_numbers": "SN123456",
        "category": "Hardware",
        "sentiment": "neutral",
        "problem_summary": email_obj.body[:200],
        "ml_model_version": "v1.0",
        "raw_ml_response": {"text": email_obj.body}
    }


def create_ticket_from_email(db: Session, email_obj: Email):
    existing_ticket = db.query(SupportTicket).filter(SupportTicket.email_id == email_obj.id).first()
    if existing_ticket:
        return existing_ticket

    ml_data = process_email_with_ml(email_obj)

    ml_request = MLRequest(
        email_id=email_obj.id,
        sent_to_ml_at=datetime.utcnow(),
        ml_model_version=ml_data["ml_model_version"],
        raw_ml_response=ml_data["raw_ml_response"]
    )
    db.add(ml_request)
    db.commit()
    db.refresh(ml_request)

    ticket = SupportTicket(
        email_id=email_obj.id,
        full_name=ml_data["full_name"],
        company=ml_data["company"],
        phone=ml_data["phone"],
        device_model=ml_data["device_model"],
        serial_numbers=ml_data["serial_numbers"],
        category=ml_data["category"],
        sentiment=ml_data["sentiment"],
        problem_summary=ml_data["problem_summary"],
        status="new"
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    print(f"Создан тикет: {ticket.id} по письму {email_obj.subject}")
    return ticket
