"""
Маршруты HTML-страниц.
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Данные об услугах — используются на главной странице и в навигации
SERVICES = [
    {
        "slug": "kuzovnoj-remont",
        "title": "Кузовной ремонт",
        "short": "Рихтовка, сварка, стапель. Полный цикл в одном цехе.",
        "works": [
            "Рихтовка крыльев, дверей, капота, крыши, порогов",
            "Ремонт вмятин",
            "Замена кузовных элементов",
            "Работа на стапеле — восстановление геометрии",
            "Сварочные работы",
            "Замена лобового стекла",
        ],
        "icon": "icon-body.svg",
    },
    {
        "slug": "pokraska",
        "title": "Покраска",
        "short": "Покраска в собственной камере с компьютерным подбором цвета.",
        "works": [
            "Покраска отдельных элементов",
            "Полная покраска автомобиля",
            "Компьютерный подбор цвета",
            "Покраска бамперов и пластика",
            "Покраска сколов и мелких деталей",
        ],
        "icon": "icon-paint.svg",
    },
    {
        "slug": "udalenie-vmyatin",
        "title": "Удаление вмятин",
        "short": "Метод PDR — без покраски, с сохранением заводского ЛКП.",
        "works": [
            "Удаление вмятин без покраски (PDR)",
            "Ремонт после града",
            "Устранение вмятин после парковочных ударов",
            "Ремонт крыши, капота, дверей, крыльев",
        ],
        "icon": "icon-dent.svg",
    },
]


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "services": SERVICES},
    )


@router.get("/uslugi/{slug}", response_class=HTMLResponse)
async def service_page(request: Request, slug: str):
    service = next((s for s in SERVICES if s["slug"] == slug), None)
    if not service:
        return templates.TemplateResponse(
            "404.html", {"request": request}, status_code=404
        )
    return templates.TemplateResponse(
        "services/service.html",
        {"request": request, "service": service, "services": SERVICES},
    )
