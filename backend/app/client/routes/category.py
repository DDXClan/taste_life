from fastapi import Depends, APIRouter
from depends import get_item_service
from schemas.item import CategoryScheme
from service.item import ItemService

cat_route = APIRouter(prefix='/api/category', tags=['category'])

@cat_route.get('/')
async def get_all(service: ItemService = Depends(get_item_service)):
    category = await service.cat_all()
    return category

