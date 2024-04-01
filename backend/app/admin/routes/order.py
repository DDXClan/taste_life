from fastapi import Depends, APIRouter, HTTPException, Request
from depends import get_order_service
from service.order import OrderService, OrderUpdateStatus
from database.models import User
from util import limiter


order_route = APIRouter(prefix='/orders', tags=['Order'])


@order_route.get('/')
@limiter.limit('30/minutes')
async def all(request: Request, service: OrderService  = Depends(get_order_service)):
    return await service.all()


@order_route.put('/')
@limiter.limit('5/minutes')
async def update_status(request: Request, data: OrderUpdateStatus, 
                        serivce: OrderService = Depends(get_order_service)):
    return await serivce.update_status(data)


@order_route.get('/user/{username}')
@limiter.limit('5/minutes')
async def by_user(request: Request, username: str, 
                  service: OrderService = Depends(get_order_service)):
    user = await User.by_username(username)
    if not user:
        raise HTTPException(status_code=404)
    return await service.by_user(user.id)