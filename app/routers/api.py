"""
API-маршруты: приём и обработка заявок.
"""
import re
import time
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, validator
from app.services.telegram import send_to_telegram

router = APIRouter(prefix="/api")

# Простая защита от повторных отправок: храним время последней заявки по IP
# (сбрасывается при перезапуске сервера — этого достаточно для базовой защиты)
_last_submission: dict[str, float] = {}
RATE_LIMIT_SECONDS = 60  # не чаще одной заявки в минуту с одного IP

# Список услуг для валидации
VALID_SERVICES = [
    "Кузовной ремонт",
    "Покраска",
    "Удаление вмятин без покраски",
    "Другое",
]


class ApplicationForm(BaseModel):
    name: str = ""
    phone: str
    car_make: str
    car_model: str
    service: str = "Другое"

    @validator("phone")
    def validate_phone(cls, v):
        cleaned = re.sub(r"[\s\-\(\)\+]", "", v)
        if not re.match(r"^\d{10,15}$", cleaned):
            raise ValueError("Некорректный номер телефона")
        return v

    @validator("car_make", "car_model")
    def validate_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Поле не может быть пустым")
        return v.strip()

    @validator("name")
    def validate_name(cls, v):
        return v.strip()

    @validator("service")
    def validate_service(cls, v):
        if v and v not in VALID_SERVICES:
            raise ValueError("Недопустимое значение услуги")
        return v


@router.post("/application")
async def submit_application(request: Request, form: ApplicationForm):
    # Проверка rate limit по IP
    client_ip = request.client.host if request.client else "unknown"
    now = time.time()
    last = _last_submission.get(client_ip, 0)

    if now - last < RATE_LIMIT_SECONDS:
        remaining = int(RATE_LIMIT_SECONDS - (now - last))
        raise HTTPException(
            status_code=429,
            detail=f"Пожалуйста, подождите {remaining} секунд перед повторной отправкой.",
        )

    try:
        success = await send_to_telegram(form.dict())
    except ValueError as e:
        # Telegram не настроен
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail="Не удалось отправить заявку. Пожалуйста, позвоните нам напрямую.",
        )

    if success:
        _last_submission[client_ip] = now
        return JSONResponse({"ok": True, "message": "Заявка отправлена! Мы перезвоним вам в ближайшее время."})

    raise HTTPException(
        status_code=502,
        detail="Заявка не была доставлена. Пожалуйста, попробуйте ещё раз или позвоните нам.",
    )
