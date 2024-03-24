from fastapi import HTTPException
from database.models import Item, Category
from schemas.item import CategoryScheme, ItemScheme
from database.connection import redis
import json
class ItemService:

    def __init__(self, _item: Item, _category: Category) -> None:
        self._item = _item
        self._category = _category


#----------------------------------------Category---------------------------------------------------#
    async def cat_create(self, cat_data: CategoryScheme):
        await redis.delete('category')
        await self._category.create(cat_data.category_name)
        return {'message': 'Success'}
    

    async def cat_all(self):
        cat = await redis.get('category')
        if cat is not None:
            return json.loads(cat)
        else:
            cat = await self._category.all()
            cat = [{"id": item.id, "category_name": item.category_name} for item in cat]
            await redis.set('category', json.dumps(cat))
            return cat
        

    async def cat_update(self, id: int, cat_data: CategoryScheme):
        result = await self._category.update(id, category_name=cat_data.category_name)
        if not result:
            raise HTTPException(status_code=400)
        await redis.delete('category')
        return result
    
    async def cat_delete(self, id: int):
        
        result = await self._category.delete(id)
        if result:
            await redis.delete('category')
            return {'message': 'Success'}
        raise HTTPException(status_code=400)
    

#----------------------------------------ITEM------------------------------------------------------#
    async def item_create(self, item_data: ItemScheme):
        await redis.delete('item')
        await self._item.create(item_data.dict())
        return {'message': 'Success'}
    

    async def item_all(self):
        item = await redis.get('item')
        if item is not None:
            return json.loads(item)
        else:
            item = await self._item.all()
            item = [{"id": item.id, "item_name": item.item_name, "item_img": item.item_img,
            "wt": item.wt, "description": item.description, "price": item.price,
            "category_id": item.category_id} for item in item]
            await redis.set('item', json.dumps(item))
            return item

    async def item_by_id(self, id: int):
        item = await self._item.by_id(id)
        if not item:
            raise HTTPException(status_code=404)
        return item


    async def item_update(self, id: int, item_data: dict):
        keys_del = [x for x in item_data.keys() if not item_data[x]]
        for _ in keys_del:
            del item_data[_]
        result = await self._item.update(id, item_data)
        if not result:
            raise HTTPException(status_code=400)
        await redis.delete('item')
        return result


    async def item_delete(self, id: int):
        item = await self._item.delete(id)
        if item:
            await redis.delete('item')
            return {'message': 'Success'}
        raise HTTPException(status_code=400)
    


    