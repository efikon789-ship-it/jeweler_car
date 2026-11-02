# ЮвелирКар — Сайт центра кузовного ремонта

Коммерческий сайт кузовного центра «ЮвелирКар» (Краснодар).  
Стек: Python, FastAPI, Jinja2, HTML, CSS, JavaScript.

## Быстрый старт

### 1. Клонировать репозиторий

```bash
git clone https://github.com/ВАШ_ЛОГИН/yuvelirkar.git
cd yuvelirkar
```

### 2. Создать виртуальное окружение и установить зависимости

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Настроить переменные окружения

```bash
# Скопировать шаблон
copy .env.example .env   # Windows
cp .env.example .env     # Linux/Mac

# Открыть .env и заполнить:
# TELEGRAM_BOT_TOKEN — токен бота от @BotFather
# TELEGRAM_CHAT_ID   — chat_id руководителя
```

### 4. Запустить сайт локально

```bash
uvicorn app.main:app --reload
```

Открой браузер: [http://localhost:8000](http://localhost:8000)

## Структура проекта

```
Car/
├── app/
│   ├── main.py          # Точка входа FastAPI
│   ├── routers/         # Маршруты (страницы и API)
│   ├── services/        # Бизнес-логика (Telegram, валидация)
│   └── config.py        # Настройки из .env
├── templates/           # HTML-шаблоны Jinja2
│   ├── base.html        # Базовый шаблон
│   ├── index.html       # Главная страница
│   └── services/        # Страницы услуг
├── static/
│   ├── css/             # Стили
│   ├── js/              # JavaScript
│   └── img/             # Изображения
├── .env.example         # Шаблон переменных окружения
├── .gitignore
├── requirements.txt
├── README.md
└── MISSING_DATA.md      # Список недостающих данных
```

## Telegram-заявки

Заявки с сайта отправляются напрямую в Telegram руководителю через Bot API.  
База данных не используется.

Подробности настройки бота — в `.env.example`.
