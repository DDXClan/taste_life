from fastapi import HTTPException
from database.models import User
from schemas.user import UserScheme

class UserService:
    

    @staticmethod
    async def info(id: int):
        result = await User.by_id(id)
        if not result:
            raise HTTPException(status_code=404)
        return result

    @staticmethod
    async def update(id:int, data: dict):
        keys_del = [x for x in data.keys() if not data[x]]
        for key in keys_del:
            del data[key]
        result = await User.update(id, data)
        if not result:
            return HTTPException(status_code=400)
        return result
    
    @staticmethod
    async def delete(id: int):
        result = await User.delete(id)
        if not result:
            raise HTTPException(status_code=409)
        return {'message': 'Success'}        