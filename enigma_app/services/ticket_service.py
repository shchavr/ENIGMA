from datetime import datetime

import requests
from sqlalchemy.orm import Session

from enigma_app.config import ML_URL
from enigma_app.db import Email, SupportTicket, MLRequest, Response
from enigma_app.db.models.device_problem_heatmap import DeviceProblemHeatmap


def process_email_with_ml(email_obj: Email):
    """
    Отправляет текст письма в ML-сервис
    и возвращает обработанные данные.
    """
    text_for_ml = " ".join(email_obj.body.split())
    try:
        response = requests.post(
            ML_URL,
            json={"text": text_for_ml},
            headers={"accept": "application/json"},
            timeout=10
        )

        response.raise_for_status()
        ml_response = response.json()

    except requests.RequestException as e:
        raise Exception(f"Ошибка при обращении к ML сервису: {e}")

    extracted = ml_response.get("extracted_data", {})
    sentiment_data = ml_response.get("sentiment", {})
    classification_data = ml_response.get("classification", {})
    return {
        "full_name": extracted.get("full_name"),
        "company": extracted.get("object"),
        "phone": extracted.get("phone"),
        "device_model": extracted.get("device_type"),
        "serial_numbers": extracted.get("factory_number"),
        "category": classification_data.get("category"),
        "sentiment": sentiment_data.get("label"),
        "problem_summary": extracted.get("summary"),
        "email_from_text": extracted.get("email"),
        "ml_model_version": "ml_service_v1",
        "raw_ml_response": ml_response
    }


def create_ticket_from_email(db: Session, email_obj: Email):
    existing_ticket = db.query(SupportTicket).filter(
        SupportTicket.email_id == email_obj.id
    ).first()

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
        email_from_text=ml_data.get("email_from_text"),
        status="new"
    )
    db.add(ticket)

    if ml_data["device_model"]:
        heatmap_entry = db.query(DeviceProblemHeatmap).filter(
            DeviceProblemHeatmap.device_model == ml_data["device_model"]
        ).first()

        if heatmap_entry:
            heatmap_entry.problem_count += 1
        else:
            heatmap_entry = DeviceProblemHeatmap(
                device_model=ml_data["device_model"],
                problem_count=1
            )
            db.add(heatmap_entry)

    db.commit()
    db.refresh(ticket)

    generated_text = ml_data["raw_ml_response"].get("generated_response")

    response = Response(
        ticket_id=ticket.id,
        ml_request_id=ml_request.id,
        response_text=generated_text,
        is_ai_generated=True,
        sent_to_user=True,
        sent_at=datetime.now(),
    )

    db.add(response)

    db.commit()

    print(f"Тикет {ticket.id} создан, heatmap обновлён")
    return ticket
