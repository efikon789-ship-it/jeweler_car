"""
Конфигурация приложения.
Читает переменные окружения из .env через python-dotenv.
"""
from dotenv import load_dotenv
import os

load_dotenv()

# Telegram Bot
TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID", "")

# Контакты организации
PHONE: str = os.getenv("PHONE", "")
TELEGRAM_LINK: str = os.getenv("TELEGRAM_LINK", "")
WHATSAPP_LINK: str = os.getenv("WHATSAPP_LINK", "")
MAX_LINK: str = os.getenv("MAX_LINK", "")

# Режим разработки
DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
