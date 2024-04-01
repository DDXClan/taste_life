from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware
from admin.routes.category import cat_route
from admin.routes.item import item_route
from admin.routes.order import order_route
from admin.routes.user import user_route
from depends import get_current_user
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from util import limiter

app = FastAPI(dependencies=[Depends(get_current_user)])


app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


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