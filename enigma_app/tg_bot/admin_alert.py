import json
import os

from telegram import Bot

from enigma_app.config import ADMIN_CHAT_ID, TELEGRAM_TOKEN

bot = Bot(token=TELEGRAM_TOKEN)


def is_important_email(email: str) -> bool:
    if not email:
        return False

    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, "important_clients.json")
    if not os.path.exists(file_path):
        return False

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    important_emails = [client["email"] for client in data.get("important_clients", [])]
    return email in important_emails


async def send_admin_alert(ticket, ml_data):
    text = (
        f"⚠️ Внимание! Негативное письмо от важного клиента.\n\n"
        f"Клиент: {ml_data['full_name']}\n"
        f"Email: {ml_data.get('email_from_text', 'не указан')}\n"
        f"Компания: {ml_data['company']}\n"
        f"Сентимент: {ml_data['sentiment']}\n"
        f"Проблема: {ml_data['problem_summary']}\n"
        f"Тикет ID: {ticket.id}"
    )
    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=text)
