from fastapi import Depends, APIRouter, File, UploadFile, HTTPException, Request
from depends import get_item_service
from service.item import ItemService, ItemScheme
from util import add_img, limiter
item_route = APIRouter(prefix='/items', tags=['Item'])


@item_route.post('/')
@limiter.limit('30/minutes')
async def create(request: Request, item_data: ItemScheme, 
                 service: ItemService  = Depends(get_item_service)):
    return await service.item_create(item_data)


@item_route.put('/{id}')
@limiter.limit('5/minutes')
async def update(request: Request, id: int, item_data: ItemScheme,
                 service: ItemService = Depends(get_item_service)):
    return await service.item_update(id, item_data.dict())


@item_route.put('/{id}/img')
@limiter.limit('30/minutes')
async def update_img(request: Request,id: int, image: UploadFile = File(...),
                     service: ItemService = Depends(get_item_service)):
    item = await service.item_update(id, {'item_img': image.filename})
    if item:
        await add_img(image)
        return await service.item_by_id(id)
    else:
        raise HTTPException(status_code=400)


@item_route.delete('/{id}')
@limiter.limit('30/minutes')
async def delete(request: Request,id: int, service: ItemService = Depends(get_item_service)):
    return await service.item_delete(id)

