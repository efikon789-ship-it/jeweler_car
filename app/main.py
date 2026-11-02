"""
Точка входа FastAPI-приложения «ЮвелирКар».
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import pages, api

app = FastAPI(
    title="ЮвелирКар",
    description="Центр кузовного ремонта в Краснодаре",
    docs_url=None,   # отключаем Swagger UI в продакшне
    redoc_url=None,
)

# Статические файлы (CSS, JS, изображения)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Подключаем маршруты
app.include_router(pages.router)
app.include_router(api.router)
