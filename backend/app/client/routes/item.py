from fastapi import Depends, APIRouter
from depends import get_item_service
from service.item import ItemService

item_route = APIRouter(prefix='/items', tags=['Item'])

@item_route.get('/')
async def all(service: ItemService = Depends(get_item_service)):
    category = await service.item_all()
    return category

@item_route.get('/{id}')
async def by_id(id: int, service: ItemService = Depends(get_item_service)):
    return await service.item_by_id(id)

