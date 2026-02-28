import os

from dotenv import load_dotenv

CATEGORIES = [
    "неисправность",
    "калибровка",
    "запрос документации",
    "интеграция с PLC",
    "проблема связи",
    "другое"
]



load_dotenv()


AI_TOKEN = os.getenv("AI_TOKEN")
