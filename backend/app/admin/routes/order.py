from fastapi import Depends, APIRouter, File, UploadFile, HTTPException
from depends import get_order_service
from service.order import OrderService
from util import add_img
order_route = APIRouter(prefix='/order', tags=['Order'])


@order_route.get('/')
async def all(service: OrderService  = Depends(get_order_service)):
    return await service.all()




