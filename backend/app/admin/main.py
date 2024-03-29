from fastapi import FastAPI, Depends
from admin.routes.category import cat_route
from admin.routes.item import item_route
from admin.routes.order import order_route
from depends import get_current_user


app = FastAPI(dependencies=[Depends(get_current_user)])

app.include_router(cat_route)
app.include_router(item_route)
app.include_router(order_route)