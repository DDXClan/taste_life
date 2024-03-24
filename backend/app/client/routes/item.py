from fastapi import Depends, APIRouter
from fastapi.responses import FileResponse
from depends import get_item_service
from schemas.item import ItemScheme
from service.item import ItemService
from util import image_path

item_route = APIRouter(prefix='/api/item', tags=['Item'])

@item_route.get('/')
async def all(service: ItemService = Depends(get_item_service)):
    category = await service.item_all()
    return category

@item_route.get('/{id}')
async def by_id(id: int, service: ItemService = Depends(get_item_service)):
    return await service.item_by_id(id)

@item_route.get('/img/{image_name}')
async def image(image_name: str):
    return FileResponse(f'{image_path}/{image_name}')