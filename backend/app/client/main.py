from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from client.routes.category import cat_route
from client.routes.item import item_route
from client.routes.order import order_route
from client.routes.user import user_route
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from util import limiter
from fastapi.responses import FileResponse
from util import image_path

app = FastAPI()


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


@app.get('/img/{image_name}')
async def image(image_name: str):
    return FileResponse(f'{image_path}/{image_name}')