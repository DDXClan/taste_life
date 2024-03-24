from fastapi import FastAPI
from admin.routes.category import cat_route
from admin.routes.item import item_route

app = FastAPI()

app.include_router(cat_route)
app.include_router(item_route)