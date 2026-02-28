import asyncio
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from enigma_app.config import EMAIL_USER, EMAIL_PASSWORD

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587  # STARTTLS

async def send_email(to_email: str, subject: str, body: str) -> datetime:
    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    def _send():
        try:
            with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(EMAIL_USER, EMAIL_PASSWORD)
                server.send_message(msg)
        except smtplib.SMTPException as e:
            raise Exception(f"Ошибка при отправке письма: {e}")

    # Запуск синхронной функции в отдельном потоке
    await asyncio.to_thread(_send)
    return datetime.utcnow()