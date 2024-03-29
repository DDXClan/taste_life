from fastapi import FastAPI, Depends, Form
from starlette.middleware.cors import CORSMiddleware
from database.models import User, Role
from schemas.user import UserScheme
from service.auth import AuthService
from depends import get_auth_service, get_current_user

app = FastAPI(prefix='/auth')


async def gen_role():
    try:
        await Role.create('user')
        await Role.create('admin')
    except Exception:
        pass

app.add_event_handler('startup', gen_role)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем запросы от всех доменов
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы запросов (GET, POST, PUT, DELETE и др.)
    allow_headers=["*"],  # Разрешаем все заголовки
)


@app.post('/registration', status_code=201)
async def reg(user_data: UserScheme, service: AuthService = Depends(get_auth_service)):
    return await service.reg(user_data)

@app.post('/login')
async def login(username: str = Form(...), password: str = Form(...),
                service: AuthService = Depends(get_auth_service)):
    return await service.login(username, password)

@app.post('/refresh')
async def refresh(token: str = Form(...), service: AuthService = Depends(get_auth_service)):
    return await service.refresh(token)

@app.delete('/exit')
async def exit(user: User = Depends(get_current_user), 
               service: AuthService = Depends(get_auth_service)):
    return await service.exit(user.username)