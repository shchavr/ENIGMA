from enigma_app.db.session import get_db
from enigma_app.services.email_service import fetch_and_save_emails
from enigma_app.services.ticket_service import create_ticket_from_email


async def fetch_and_process_emails():
    db = next(get_db())
    new_emails = fetch_and_save_emails()
    for email_obj in new_emails:
        await create_ticket_from_email(db, email_obj)