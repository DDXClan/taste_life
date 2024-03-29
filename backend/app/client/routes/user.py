from fastapi import APIRouter, Depends
from database.models import User
from service.user import UserService, UserScheme
from depends import get_user_service, get_current_user

user_route = APIRouter(prefix='/user', tags=['User'])

@user_route.get('/')
async def info(service: UserService = Depends(get_user_service),
               user: User = Depends(get_current_user)):
    return await service.info(user.id)


@user_route.put('/')
async def update(data: UserScheme, service: UserService = Depends(get_user_service),
                 user: User = Depends(get_current_user)):
    return await service.update(user.id, data.dict())


@user_route.delete('/')
async def delete(service: UserService = Depends(get_user_service),
                 user: User = Depends(get_current_user)):
    return await service.delete(user.id)