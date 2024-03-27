from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from database.models import Item, Category, User
from service.item import ItemService
from service.auth import AuthService
from service.order import OrderService


item_service = ItemService()

async def get_item_service() -> ItemService:
    return item_service


auth_service = AuthService()

oauth2scheme = OAuth2PasswordBearer('/api/auth/login')

async def get_auth_service() -> AuthService:
    return auth_service

async def get_current_user(token: str = Depends(oauth2scheme)) -> User:
    return await auth_service.get_current_user(token)

order_service = OrderService()

async def get_order_service() -> OrderService:
    return order_service