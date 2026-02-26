import email
import imaplib
from datetime import datetime
from email.header import decode_header

from app.config import EMAIL_HOST, EMAIL_PORT, EMAIL_PASSWORD, EMAIL_USER
from app.db import Email
from app.db.session import get_db


def get_email_body(msg):
    """Безопасно достаём текст письма с учетом кодировки."""
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                payload = part.get_payload(decode=True)
                charset = part.get_content_charset() or "utf-8"
                try:
                    body += payload.decode(charset)
                except Exception:
                    body += payload.decode(charset, errors="replace")
    else:
        payload = msg.get_payload(decode=True)
        charset = msg.get_content_charset() or "utf-8"
        try:
            body = payload.decode(charset)
        except Exception:
            body = payload.decode(charset, errors="replace")
    return body


def decode_mime_header(header_value):
    """Декодируем MIME-заголовки, например Subject или From."""
    if not header_value:
        return ""
    decoded_fragments = decode_header(header_value)
    decoded_string = ""
    for fragment, charset in decoded_fragments:
        if isinstance(fragment, bytes):
            try:
                decoded_string += fragment.decode(charset or "utf-8", errors="replace")
            except Exception:
                decoded_string += fragment.decode("utf-8", errors="replace")
        else:
            decoded_string += fragment
    return decoded_string


def fetch_and_save_emails():
    db = next(get_db())
    new_email_objs = []
    mail = imaplib.IMAP4_SSL(EMAIL_HOST, EMAIL_PORT)
    mail.login(EMAIL_USER, EMAIL_PASSWORD)
    mail.select("inbox")

    status, data = mail.search(None, "UNSEEN")
    for num in data[0].split():
        status, msg_data = mail.fetch(num, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        body = get_email_body(msg)
        subject = decode_mime_header(msg.get("Subject"))
        sender = decode_mime_header(msg.get("From"))

        email_obj = Email(
            message_id=msg.get("Message-ID"),
            sender_email=sender,
            subject=subject,
            body=body,
            received_at=datetime.utcnow(),
            processing_status="received"
        )
        db.add(email_obj)
        db.commit()
        db.refresh(email_obj)

        new_email_objs.append(email_obj)
        print(f"Сохранено письмо: {subject}")

    mail.logout()
    return new_email_objs
