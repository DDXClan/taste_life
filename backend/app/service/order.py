import time, random
from fastapi import HTTPException
from typing import List
from database.models import OrderStatus, Order, Item
from schemas.order import OrderItem

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
        return item.price

    async def by_user(self, user_id: int):
        order = await Order.unique_key_by_user(user_id)
        return [
            {
                'unique_key': ord,
                'items': [{'item': await Item.by_id(item.item_id), 'quantity': item.quantity} for item in await Order.by_unique_key(ord)],
                'price': sum([order.quantity * await self.get_item_price(order.item_id) for order in await Order.by_unique_key(ord)])
            } for ord in order
        ]