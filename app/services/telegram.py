"""
Сервис отправки заявок в Telegram через Bot API.
Заявки не сохраняются в базу данных — только пересылаются руководителю.
"""
import httpx
from app.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


def build_message(data: dict) -> str:
    """Формирует текст сообщения для Telegram."""
    lines = ["📋 *Новая заявка с сайта ЮвелирКар*", ""]

    if data.get("name"):
        lines.append(f"👤 Имя: {data['name']}")

    lines.append(f"📞 Телефон: {data['phone']}")
    lines.append(f"🚗 Автомобиль: {data['car_make']} {data['car_model']}")

    if data.get("service"):
        lines.append(f"🔧 Услуга: {data['service']}")

    return "\n".join(lines)


async def send_to_telegram(data: dict) -> bool:
    """
    Отправляет заявку в Telegram.
    Возвращает True при успехе, False при ошибке.
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        raise ValueError(
            "Не настроены TELEGRAM_BOT_TOKEN или TELEGRAM_CHAT_ID в .env"
        )

    text = build_message(data)
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        return result.get("ok", False)
