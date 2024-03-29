from fastapi import HTTPException
from database.models import Item, Category
from schemas.item import CategoryScheme, ItemScheme
from database.connection import redis
import json
class ItemService:

#----------------------------------------Category---------------------------------------------------#
    @staticmethod
    async def cat_create(cat_data: CategoryScheme):
        await redis.delete('category')
        await Category.create(cat_data.category_name)
        return {'message': 'Success'}
    

    @staticmethod
    async def cat_all():
        cat = await redis.get('category')
        if cat is not None:
            return json.loads(cat)
        else:
            cat = await Category.all()
            if not cat:
                raise HTTPException(status_code=404)
            cat = [{"id": item.id, "category_name": item.category_name} for item in cat]
            await redis.set('category', json.dumps(cat))
            return cat
        

    @staticmethod
    async def cat_update(id: int, cat_data: CategoryScheme):
        result = await Category.update(id, category_name=cat_data.category_name)
        if not result:
            raise HTTPException(status_code=400)
        await redis.delete('category')
        return result
    

    @staticmethod
    async def cat_delete( id: int):
        
        result = await Category.delete(id)
        if result:
            await redis.delete('category')
            return {'message': 'Success'}
        raise HTTPException(status_code=409)
    

#----------------------------------------ITEM------------------------------------------------------#
    @staticmethod
    async def item_create(item_data: ItemScheme):
        await redis.delete('item')
        await Item.create(item_data.dict())
        return {'message': 'Success'}
    

    @staticmethod
    async def item_all():
        item = await redis.get('item')
        if item is not None:
            return json.loads(item)
        else:
            item = await Item.all()
            if not item:
                raise HTTPException(status_code=404)
            item = [{"id": item.id, "item_name": item.item_name, "item_img": item.item_img,
            "wt": item.wt, "description": item.description, "price": item.price,
            "category_id": item.category_id} for item in item]
            await redis.set('item', json.dumps(item))
            return item
    @staticmethod
    async def item_by_id(id: int):
        item = await Item.by_id(id)
        if not item:
            raise HTTPException(status_code=404)
        return item

    @staticmethod
    async def item_update(id: int, item_data: dict):
        keys_del = [x for x in item_data.keys() if not item_data[x]]
        for _ in keys_del:
            del item_data[_]
        result = await Item.update(id, item_data)
        if not result:
            raise HTTPException(status_code=400)
        await redis.delete('item')
        return result

    @staticmethod
    async def item_delete(id: int):
        item = await Item.delete(id)
        if item:
            await redis.delete('item')
            return {'message': 'Success'}
        raise HTTPException(status_code=409)
    


    