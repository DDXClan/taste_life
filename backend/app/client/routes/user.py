from fastapi import APIRouter, Depends, Request, UploadFile, File, HTTPException
from database.models import User
from service.user import UserService, UserScheme
from depends import get_user_service, get_current_user
from util import add_img
from util import limiter

user_route = APIRouter(prefix='/users', tags=['User'])

@user_route.get('/')
async def info(service: UserService = Depends(get_user_service),
               user: User = Depends(get_current_user)):
    return await service.info(user.id)


@user_route.put('/')
@limiter.limit('5/minutes')
async def update(request: Request, data: UserScheme, service: UserService = Depends(get_user_service),
                 user: User = Depends(get_current_user)):
    return await service.update(user.id, data.dict())


@user_route.put('/img')
@limiter.limit('5/minutes')
async def update_img(request: Request, image: UploadFile = File(...),
                     service: UserService = Depends(get_user_service), 
                     user: User = Depends(get_current_user)):
    item = await service.update(user.id, {'user_img': image.filename})
    if item:
        await add_img(image)
        return item
    else:
        raise HTTPException(status_code=400)


@user_route.delete('/')
async def delete(service: UserService = Depends(get_user_service),
                 user: User = Depends(get_current_user)):
    return await service.delete(user.id)


