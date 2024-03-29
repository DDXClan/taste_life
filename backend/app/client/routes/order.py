from fastapi import APIRouter, Depends
from database.models import User, OrderStatus
from service.order import OrderService, OrderItem
from depends import get_current_user, get_order_service

order_route = APIRouter(prefix='/ortder', tags=['Order'])

async def gen_status():
    try:
        await OrderStatus.create('В рассмотрении')
        await OrderStatus.create('Готовится')
        await OrderStatus.create('Готов к выдаче')
    except Exception:
        pass

order_route.add_event_handler('startup', gen_status)

@order_route.post('/', status_code=201)
async def create(data: OrderItem, user: User = Depends(get_current_user),
                 order_service: OrderService = Depends(get_order_service)):
    return await order_service.create_order(user.id, data)

@order_route.get('/')
async def all(user: User = Depends(get_current_user), 
              order_service: OrderService = Depends(get_order_service)):
    return await order_service.by_user(user.id)