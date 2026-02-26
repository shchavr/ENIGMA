import threading
import time

from fastapi import FastAPI

from app.api.utilits.create_admin import create_default_admin
from app.api.v1 import admins, tickets, emails
from app.services.email_processing_service import fetch_and_process_emails

app = FastAPI(title="Support AI")

app.include_router(emails.router, prefix="/api/v1")
app.include_router(tickets.router, prefix="/api/v1")
app.include_router(admins.router, prefix="/api/v1")


# Email
#   ↓
# MLRequest
#   ↓
# SupportTicket (status=new)
#   ↓
# ML генерирует ответ
#   ↓
# Response (is_ai_generated=True)
#   ↓
# Email отправляется клиенту
#   ↓
# SupportTicket.status = "answered"
#   ↓
# AdminLog (action="auto_answered")

def email_polling_loop():
    while True:
        try:
            fetch_and_process_emails()
        except Exception as e:
            print(f"[ERROR] Ошибка в email_polling_loop: {e}")
        time.sleep(60)


@app.on_event("startup")
def start_email_polling():
    thread = threading.Thread(target=email_polling_loop, daemon=True)
    thread.start()


@app.on_event("startup")
def startup_event():
    create_default_admin()
