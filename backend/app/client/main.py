from fastapi import FastAPI
from client.routes.category import cat_route
from client.routes.item import item_route
from client.routes.order import order_route
from client.routes.user import user_route


app = FastAPI()

app.include_router(cat_route)
app.include_router(item_route)
app.include_router(order_route)
app.include_router(user_route)