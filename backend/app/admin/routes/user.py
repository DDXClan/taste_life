from fastapi import APIRouter, Depends, HTTPException, Request
from service.user import UserService
from schemas.user import UserUpdateForAdmin
from database.models import User
from depends import get_user_service
from util import limiter

user_route = APIRouter(prefix='/users', tags=['User'])

@user_route.get('/')
@limiter.limit('5/minutes')
async def all(request: Request, service: UserService = Depends(get_user_service)):
    return await service.all()

@user_route.put('/{username}')
@limiter.limit('5/minutes')
async def update(request: Request, username: str, data: UserUpdateForAdmin, service: UserService = Depends(get_user_service)):
    user = await User.by_username(username)
    if not user:
        raise HTTPException(status_code=404)
    return await service.update(user.id, data.dict())

@user_route.delete('/{username}')
@limiter.limit('3/minutes')
async def delete(request: Request, username: str, service: UserService = Depends(get_user_service)):
    user = await User.by_username(username)
    if not user:
        raise HTTPException(status_code=404)
    return await service.delete(user.id)