from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from database.models import Item, Category, User
from service.item import ItemService
from service.auth import AuthService


item = Item()
category = Category()

item_service = ItemService(item, category)

async def get_item_service() -> ItemService:
    return item_service


user = User()

auth_service = AuthService(user)

oauth2scheme = OAuth2PasswordBearer('/api/auth/login')

async def get_auth_service() -> AuthService:
    return auth_service

async def get_current_user(token: str = Depends(oauth2scheme)) -> User:
    return await auth_service.get_current_user(token)