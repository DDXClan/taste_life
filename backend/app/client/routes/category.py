from fastapi import Depends, APIRouter
from depends import get_item_service
from service.item import ItemService

cat_route = APIRouter(prefix='/category', tags=['category'])

@cat_route.get('/')
async def get_all(service: ItemService = Depends(get_item_service)):
    category = await service.cat_all()
    return category

