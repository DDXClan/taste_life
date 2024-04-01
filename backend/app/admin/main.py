from fastapi import FastAPI, Depends, Request
from starlette.middleware.cors import CORSMiddleware
from admin.routes.category import cat_route
from admin.routes.item import item_route
from admin.routes.order import order_route
from admin.routes.user import user_route
from depends import get_current_user
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from util import limiter
from pythonjsonlogger import jsonlogger
import logging
from starlette.types import ASGIApp, Receive, Scope, Send

app = FastAPI(dependencies=[Depends(get_current_user)])


app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

log_handler = logging.FileHandler(filename='app.log')
log_handler.setFormatter(jsonlogger.JsonFormatter())

logger = logging.getLogger()
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)

class LoggingMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] == "http":
            request = Request(scope, receive=receive)

            client_ip = scope.get("client")  # Получение IP-адреса клиента

            # Логирование информации о запросе и отправителе
            logger.info({
                "client_ip": client_ip,
                "method": request.method,
                "url": str(request.url)
            })

            async def send_wrapper(message):
                if message["type"] == "http.response.start":
                    # Логирование информации о коде ответа
                    logger.info({
                        "status_code": message["status"]
                    })
                await send(message)

            await self.app(scope, receive, send_wrapper)
        else:
            await self.app(scope, receive, send)

app.add_middleware(LoggingMiddleware)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем запросы от всех доменов
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы запросов (GET, POST, PUT, DELETE и др.)
    allow_headers=["*"],  # Разрешаем все заголовки
)

app.include_router(cat_route)
app.include_router(item_route)
app.include_router(order_route)
app.include_router(user_route)