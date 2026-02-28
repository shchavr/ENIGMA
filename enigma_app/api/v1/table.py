from io import BytesIO
from typing import List

import openpyxl
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from enigma_app.api.deps import get_current_admin
from enigma_app.db import SupportTicket, AdminLog, Response
from enigma_app.db.session import get_db
from enigma_app.schemas.support_tickets import TicketRead, TicketReplyRequest
from enigma_app.services.email_sender import send_email

router = APIRouter(prefix="/admin/tickets", tags=["admin_tickets"])


@router.get("/", response_model=List[TicketRead])
def get_tickets(
        db: Session = Depends(get_db),
        admin: dict = Depends(get_current_admin)
):
    """Получение всех тикетов для админа в виде таблицы с сырой почтой и приоритетом email из текста."""
    tickets = (
        db.query(SupportTicket)
        .join(SupportTicket.email)
        .order_by(SupportTicket.created_at.desc())
        .all()
    )

    result = []
    for t in tickets:
        email_to_show = t.email_from_text or (t.email.sender_email if t.email else "")

        result.append(
            TicketRead(
                id=t.id,
                date=t.created_at.strftime("%Y-%m-%d %H:%M"),
                full_name=t.full_name or "",
                subject=t.problem_summary or "",
                object=t.company or "",
                category=t.category or "",
                phone=t.phone or "",
                email=email_to_show,
                serial_numbers=t.serial_numbers or "",
                device_model=t.device_model or "",
                sentiment=t.sentiment or "",
                status=t.status or "",
                raw_body=t.email.body if t.email else "",
                ai_generated_response=t.responses[-1].response_text if t.responses else None,
            )
        )

    return result


@router.get("/export")
def export_tickets(
        db: Session = Depends(get_db)
):
    """Выгрузка всех тикетов в Excel"""
    tickets = (
        db.query(SupportTicket)
        .join(SupportTicket.email)
        .order_by(SupportTicket.created_at.desc())
        .all()
    )

    # Создаем рабочую книгу и лист
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Tickets"

    # Заголовки
    headers = [
        "ID", "Дата", "ФИО", "Тема", "Компания", "Телефон",
        "Email", "Серийные номера", "Модель устройства", "Сентимент", "Статус", "Текст письма"
    ]
    ws.append(headers)

    for t in tickets:
        email_to_show = t.email_from_text or (t.email.sender_email if t.email else "")
        ws.append([
            t.id,
            t.created_at.strftime("%Y-%m-%d %H:%M"),
            t.full_name or "",
            t.problem_summary or "",
            t.company or "",
            t.phone or "",
            email_to_show,
            t.serial_numbers or "",
            t.device_model or "",
            t.sentiment or "",
            t.status or "",
            t.email.body if t.email else ""
        ])

    # Сохраняем в буфер
    stream = BytesIO()
    wb.save(stream)
    stream.seek(0)

    return StreamingResponse(
        stream,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=tickets.xlsx"}
    )


@router.post("/{ticket_id}/reply")
async def reply_to_ticket(
        ticket_id: int,
        data: TicketReplyRequest,
        db: Session = Depends(get_db),
        admin: dict = Depends(get_current_admin),
):
    """Отправка письма пользователю по тикету с приоритетом email из текста"""
    ticket = db.query(SupportTicket).filter(SupportTicket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Тикет не найден")

    to_email = ticket.email_from_text or (ticket.email.sender_email if ticket.email else None)
    if not to_email:
        raise HTTPException(status_code=400, detail="Email пользователя не найден")

    try:
        sent_time = await send_email(to_email, data.subject, data.body)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при отправке письма: {e}")

    response = Response(
        ticket_id=ticket.id,
        response_text=data.body,
        is_ai_generated=False,
        sent_to_user=True,
        sent_at=sent_time,
    )
    db.add(response)

    ticket.status = "answered"

    log = AdminLog(
        user_id=admin["id"],
        ticket_id=ticket.id,
        action="reply_sent"
    )
    db.add(log)
    db.commit()

    return {"message": "Письмо успешно отправлено"}
