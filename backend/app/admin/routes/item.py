from fastapi import Depends, APIRouter, File, UploadFile, HTTPException
from depends import get_item_service
from schemas.item import ItemScheme
from service.item import ItemService
from util import add_img
item_route = APIRouter(prefix='/api/item', tags=['Item'])


@item_route.post('/')
async def create(item_data: ItemScheme, service: ItemService  = Depends(get_item_service)):
    return await service.item_create(item_data)


@item_route.put('/{id}')
async def update(id: int, item_data: ItemScheme, service: ItemService = Depends(get_item_service)):
    return await service.item_update(id, item_data.dict())


@item_route.put('/{id}/img')
async def update_img(id: int, image: UploadFile = File(...),
                     service: ItemService = Depends(get_item_service)):
    item = await service.item_update(id, {'item_img': image.filename})
    if item:
        await add_img(image)
        return await service.item_by_id(id)
    else:
        raise HTTPException(status_code=400)

@item_route.delete('/{id}')
async def delete(id: int, service: ItemService = Depends(get_item_service)):
    return await service.item_delete(id)

