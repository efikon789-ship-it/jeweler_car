# ЮвелирКар — сайт центра кузовного ремонта

Коммерческий сайт кузовного центра «ЮвелирКар» (Краснодар).

---

## Стек

- **Python 3.x** + **FastAPI** — серверная часть
- **Jinja2** — HTML-шаблоны
- **HTML / CSS / JS** — фронтенд без фреймворков
- Заявки уходят напрямую в **Telegram** через Bot API — без базы данных

## Запуск локально

```bash
# 1. Виртуальное окружение
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux / macOS

# 2. Зависимости
pip install -r requirements.txt

# 3. Переменные окружения
copy .env.example .env       # Windows
# cp .env.example .env       # Linux / macOS
# Открой .env и заполни TELEGRAM_BOT_TOKEN и TELEGRAM_CHAT_ID

# 4. Сервер
uvicorn app.main:app --reload
```

Сайт откроется на [http://localhost:8000](http://localhost:8000)

## Структура

```
├── app/
│   ├── main.py          # точка входа
│   ├── config.py        # настройки из .env
│   ├── routers/         # маршруты страниц и API
│   └── services/        # отправка заявок в Telegram
├── templates/           # HTML-шаблоны (Jinja2)
├── static/              # CSS, JS, изображения
├── .env.example         # шаблон переменных окружения
└── MISSING_DATA.md      # список данных, которые нужно заполнить
```

## Переменные окружения

| Переменная | Описание |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Токен бота от [@BotFather](https://t.me/BotFather) |
| `TELEGRAM_CHAT_ID` | ID чата, куда приходят заявки |
