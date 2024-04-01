from fastapi import Depends, APIRouter, Request
from depends import get_item_service
from service.item import ItemService, CategoryScheme
from util import limiter
cat_route = APIRouter(prefix='/category', tags=['category'])


@cat_route.post('/', status_code=201)
@limiter.limit('30/minutes')
async def create(request: Request, cat_data: CategoryScheme, service: ItemService  = Depends(get_item_service)):
    return await service.cat_create(cat_data)

@cat_route.put('/{id}')
@limiter.limit('5/minutes')
async def update(request: Request, id: int, cat_data: CategoryScheme, 
                     service: ItemService = Depends(get_item_service)):
    return await service.cat_update(id, cat_data)


@cat_route.delete('/{id}')
@limiter.limit('5/minutes')
async def delete(request: Request, id: int, service: ItemService = Depends(get_item_service)):
    return await service.cat_delete(id)
