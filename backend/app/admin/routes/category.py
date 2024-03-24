from fastapi import Depends, APIRouter
from depends import get_item_service
from schemas.item import CategoryScheme
from service.item import ItemService

cat_route = APIRouter(prefix='/api/category', tags=['category'])


@cat_route.post('/', status_code=201)
async def create(cat_data: CategoryScheme, service: ItemService  = Depends(get_item_service)):
    return await service.cat_create(cat_data)

@cat_route.put('/{id}')
async def update(id: int, cat_data: CategoryScheme, 
                     service: ItemService = Depends(get_item_service)):
    return await service.cat_update(id, cat_data)


@cat_route.delete('/{id}')
async def delete(id: int, service: ItemService = Depends(get_item_service)):
    return await service.cat_delete(id)
