import threading
import time

from fastapi import FastAPI

from enigma_app.api.utilits.create_admin import create_default_admin
from enigma_app.api.v1 import admins, tickets, emails, table
from enigma_app.services.email_processing_service import fetch_and_process_emails

app = FastAPI(title="Support AI")

app.include_router(emails.router, prefix="/api/v1")
app.include_router(tickets.router, prefix="/api/v1")
app.include_router(admins.router, prefix="/api/v1")

app.include_router(table.router, prefix="/api/v1")

def email_polling_loop():
    while True:
        try:
            fetch_and_process_emails()
            print("Email polling")
        except Exception as e:
            print(f"[ERROR] Ошибка в email_polling_loop: {e}")
        time.sleep(10)


@app.on_event("startup")
def start_email_polling():
    thread = threading.Thread(target=email_polling_loop, daemon=True)
    thread.start()


@app.on_event("startup")
def startup_event():
    create_default_admin()
