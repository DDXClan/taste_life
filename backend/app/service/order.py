import time, random
from fastapi import HTTPException
from typing import List
from database.models import OrderStatus, Order, Item, User
from database.connection import redis
from schemas.order import OrderItem, OrderUpdateStatus
import json
class OrderService:


    @staticmethod
    async def create_order(user_id: int, data: OrderItem):
        items = list()
        unique_key = f'{random.randint(1000, 99999)}{int(time.time())}'
        for item_id in data.order.keys():
            order = await Order.create({'item_id': item_id, 'user_id': user_id, 'quantity': data.order[item_id], 'unique_key': unique_key})
            if not order:
                raise HTTPException(status_code=400)
            items.append({'item_id': item_id, 'quantity': data.order[item_id]})
        return {'unique_key': unique_key, 'order_list': [{'item': await Item.by_id(item['item_id']), 'quantity': item['quantity']} for item in items]}


    async def item_list_by_unique_key(self, unique_key: str) -> List[Item]:
        items = [await Item.by_id(_.item_id) for _ in await Order.by_unique_key(unique_key)]
        return items


    async def get_item_price(self, item_id: int) -> int:
        item = await Item.by_id(item_id)
        if not item:
            raise HTTPException(status_code=404)
        return item.price


    async def by_user(self, user_id: int):
        result = await Order.unique_key_by_user(user_id)
        if not result:
            raise HTTPException(status_code=404)
        return [
            {
                'unique_key': ord,
                'status' : await OrderStatus.by_id([x.order_status for x in await Order.by_unique_key(ord)][0]),
                'items': [{'item': await Item.by_id(item.item_id), 'quantity': item.quantity} for item in await Order.by_unique_key(ord)],
                'price': sum([order.quantity * await self.get_item_price(order.item_id) for order in await Order.by_unique_key(ord)])
            } for ord in result
        ]
    
    
    
    async def all(self):
        result = await Order.all()
        if not result:
            raise HTTPException(status_code=404)
        return [
            {
                'unique_key': ord,
                'status' : await OrderStatus.by_id([x.order_status for x in await Order.by_unique_key(ord)][0]),
                'user': {key: getattr(await User.by_id(order.user_id), key) for key in ['id', 'username', 'email'] for order in await Order.by_unique_key(ord)},
                'items': [{f'item': await Item.by_id(item.item_id), 'quantity': item.quantity} for item in await Order.by_unique_key(ord)],
                'final_price': sum([order.quantity * await self.get_item_price(order.item_id) for order in await Order.by_unique_key(ord)])
            } for ord in result
        ]

    @staticmethod
    async def update_status(data: OrderUpdateStatus):
        update = await Order.update_status_by_unique_key(data.unique_key, data.order_status)
        if not update:
            raise HTTPException(status_code=409)
        return {'message': 'Success'}
    

    @staticmethod
    async def add_busket(user_id: int, item_id: int, quantity: int):
        item = await Item.by_id(item_id)
        result = await redis.get(f'{user_id}_basket')
        items_dict = [{'id': item.id,
                      'item_name': item.item_name,
                      'item_price': item.price,
                      'item_img': item.item_img,
                      'quantity': quantity}]
        if result is not None:
            result = json.loads(result)
            for x in result:
                items_dict.append(x)
        await redis.set(f'{user_id}_basket', json.dumps(items_dict))
        return {'message': 'Success'}

    @staticmethod
    async def get_basket(user_id: int):
        result = await redis.get(f'{user_id}_basket')
        if result is None:
            raise HTTPException(status_code=404)
        return [x for x in json.loads(result)]
    
    
    async def order_by_basket(self, user_id: int):
        result = await redis.get(f'{user_id}_basket')
        if result is None:
            raise HTTPException(status_code=400)
        order_list = dict()
        for item in json.loads(result):
            order_list[item['id']] =item['quantity']
        order = await self.create_order(user_id, OrderItem(order=order_list))
        await redis.delete(f'{user_id}_basket')
        return order
