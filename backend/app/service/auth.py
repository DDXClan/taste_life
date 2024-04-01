from fastapi import HTTPException
from typing import Optional
from passlib.hash import pbkdf2_sha256
from datetime import timedelta, datetime
import jwt
from database.models import User, Role
from database.connection import redis
from schemas.user import UserScheme

class AuthService:

    def __init__(self) -> None:
        self._SECRET_KEY = '78804631189851e2760a0e3147f83ad4cc80fc35eef18f1c2ed86be740f42517'
        self._ALGORITHM = 'HS256'
        self._EXPIRATION_TIME = timedelta(minutes=30)
        self._EXPIRATION_TIME_REFRESH = timedelta(hours=2)

    @staticmethod
    async def reg(user_data: UserScheme):
        user_data.password = pbkdf2_sha256.hash(user_data.password)
        user = await User.create(user_data.dict())
        if not user:
            raise HTTPException(status_code= 400)
        return {'message': 'Success'}
    

    @staticmethod
    async def verify_password(password: str, hash_pass: str):
        return pbkdf2_sha256.verify(hash_pass, password)


    async def gen_jwt(self, username: str, exp: timedelta):
        expiraion_time = datetime.now() + exp
        data = {'sub': username, 'exp': expiraion_time}
        return jwt.encode(data, self._SECRET_KEY, algorithm=self._ALGORITHM)
         

    async def gen_tokens(self, username: str):
        refresh_token = await self.gen_jwt(username, self._EXPIRATION_TIME_REFRESH)
        await redis.set(username, refresh_token)
        return {'type': 'bearer',
                'access_token': await self.gen_jwt(username, self._EXPIRATION_TIME),
                'refresh_token': refresh_token}


    async def decode_token(self, token: str):
        try:
            decode_data = jwt.decode(token, self._SECRET_KEY, algorithms=self._ALGORITHM)
            return decode_data
        except Exception:
            return None
        

    async def login(self, username: str, password: str):
        user = await User.by_username(username)
        if not user or not await self.verify_password(user.password, password):
            raise HTTPException(status_code=400)
        return await self.gen_tokens(user.username)
        

    async def refresh(self, refresh_token: str):
        decode_data = await self.decode_token(refresh_token)
        if not decode_data:
            raise HTTPException(status_code=401)
        redis_data = await redis.get(decode_data['sub'])
        if redis_data != refresh_token:
            raise HTTPException(status_code=401)
        await redis.delete(decode_data['sub'])
        return await self.gen_tokens(decode_data['sub'])
    

    async def get_current_user(self, token: str) -> Optional[User]:
        decode_data = await self.decode_token(token)
        if not decode_data:
            raise HTTPException(status_code=401)
        user = await User.by_username(decode_data['sub'])
        if not user:
            raise HTTPException(status_code=401)
        return user
    

    async def get_current_admin(self, token: str) -> Optional[User]:
        user = await self.get_current_user(token)
        if Role.by_id(user.role_id) == 'admin':
            return user
        raise HTTPException(status_code=403)

    async def exit(self, username: str):
        await redis.delete(username)
        return {'message': 'Success'}