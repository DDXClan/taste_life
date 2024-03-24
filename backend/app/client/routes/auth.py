from fastapi import APIRouter, Depends, Form
from database.models import User, Role
from schemas.user import UserScheme
from service.auth import AuthService
from depends import get_auth_service, get_current_user

auth_route = APIRouter(prefix='/api/auth', tags=['Auth'])


async def gen_role():
    try:
        await Role.create('user')
        await Role.create('admin')
    except Exception:
        pass

auth_route.add_event_handler('startup', gen_role)


@auth_route.post('/registration', status_code=201)
async def reg(user_data: UserScheme, service: AuthService = Depends(get_auth_service)):
    return await service.reg(user_data)

@auth_route.post('/login')
async def login(username: str = Form(...), password: str = Form(...),
                service: AuthService = Depends(get_auth_service)):
    return await service.login(username, password)

@auth_route.post('/refresh')
async def refresh(token: str = Form(...), service: AuthService = Depends(get_auth_service)):
    return await service.refresh(token)

@auth_route.delete('/exit')
async def exit(user: User = Depends(get_current_user), 
               service: AuthService = Depends(get_auth_service)):
    return await service.exit(user.username)