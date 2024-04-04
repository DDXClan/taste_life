from fastapi import APIRouter, Depends
from database.models import User, OrderStatus
from service.order import OrderService, OrderItem
from schemas.order import BasketItem
from depends import get_current_user, get_order_service

order_route = APIRouter(prefix='/orders', tags=['Order'])

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

@order_route.post('/basket', status_code=201)
async def add_in_backet(data: BasketItem, user: User = Depends(get_current_user),
                        service: OrderService = Depends(get_order_service)):
    return await service.add_busket(user.id, data.item_id, data.quantity)

@order_route.get('/backet')
async def basket(user: User = Depends(get_current_user), service: OrderService = Depends(get_order_service)):
    return await service.get_basket(user.id)

@order_route.post('/basket/order')
async def create_order_by_basket(user: User = Depends(get_current_user),
                                 service: OrderService = Depends(get_order_service)):
    return await service.order_by_basket(user.id)