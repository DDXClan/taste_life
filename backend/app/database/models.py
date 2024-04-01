from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, select, update, func, distinct
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime
from database.connection import operation_session
from util import delete, create


Base = declarative_base()

relationship_config = 'all, delete'


class Category(Base):
    __tablename__ = 'Category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(255), unique=True, nullable=False)
    item = relationship('Item', cascade=relationship_config)


    @staticmethod
    async def create(category_name: str) -> Optional['Category']:
        async def op(session: AsyncSession):
            return await create(session, Category(category_name=category_name))
        return await operation_session(op)


    @staticmethod
    async def all() -> List['Category']:
        async def op(session: AsyncSession):
            result = await session.execute(select(Category))
            return result.scalars().all()
        return await operation_session(op)

    @staticmethod
    async def by_id(id: int) -> Optional['Category']:
        async def op(session: AsyncSession):
            result = await session.execute(select(Category).where(Category.id == id))
            return result.scalar_one_or_none()
        return await operation_session(op)
    
    @staticmethod
    async def delete(id: int) -> Optional[bool]:
        async def op(session: AsyncSession):
            result = await Category.by_id(id)
            return await delete(session, result)
        return await operation_session(op)

    @staticmethod
    async def update(id: int, category_name: str) -> Optional['Category']:
        async def op(session: AsyncSession):
            await session.execute(update(Category).
                                  values(category_name=category_name).
                                  where(Category.id == id))
            await session.commit()
            return await Category.by_id(id)
        return await operation_session(op)


class Item(Base): 
    __tablename__ = 'Item'
    id = Column(Integer, primary_key=True , autoincrement=True)
    item_name = Column(String(255), unique=True, nullable=False)
    item_img = Column(String(255), default='placeholder.png')
    wt = Column(Integer, nullable=False, default=0)
    description = Column(String(255), nullable=False)
    price = Column(Integer, default=0)
    category_id = Column(ForeignKey(Category.id), nullable=False)
    oreder = relationship('Order', cascade=relationship_config)

    @staticmethod
    async def create(data: dict) -> Optional['Item']:
        async def op(session: AsyncSession):
            return await create(session, Item(**data))
        return await operation_session(op)
    

    @staticmethod
    async def all() -> List['Item']:
        async def op(session: AsyncSession):
            result = await session.execute(select(Item))
            return result.scalars().all()
        return await operation_session(op)
 

    @staticmethod
    async def by_id(id: int) -> Optional['Item']:
        async def op(session: AsyncSession):
            result = await session.execute(select(Item).where(Item.id == id))
            return result.scalar_one_or_none()
        return await operation_session(op)
    
    
    @staticmethod
    async def delete(id: int) -> Optional[bool]:
        async def op(session: AsyncSession):
            result = await Item.by_id(id)
            return await delete(session, result)
        return await operation_session(op)
    
    @staticmethod
    async def update(id: int, data: dict) -> Optional['Item']:
        async def op(session: AsyncSession):
            await session.execute(update(Item).values(**data).where(Item.id == id))
            await session.commit()
            return await Item.by_id(id)
        return await operation_session(op)
    

class Role(Base):
    __tablename__ = 'Role'
    id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(255), nullable=False, unique=True)
    user = relationship('User', cascade=relationship_config)


    @staticmethod
    async def create(role_name: str) -> Optional['Role']:
        async def op(session: AsyncSession):
            return await create(session,  Role(role_name=role_name))
        return await operation_session(op)


    @staticmethod
    async def all() -> List['Role']:
        async def op(session: AsyncSession):
            result = await session.execute(select(Role))
            return result.scalars().all()
        return await operation_session(op)
    

    @staticmethod
    async def by_id(id: int) -> Optional['Role']:
        async def op(session: AsyncSession):
            result = await session.execute(select(Role).where(Role.id == id))
            return result.scalar_one_or_none()
        return await operation_session(op)


    @staticmethod
    async def delete(id: int) -> Optional[bool]:
        async def op(session: AsyncSession):
            result = await Role.by_id(id)
            return await delete(session, result)
        return await operation_session(op)


class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    user_img = Column(String(255), default='placeholder.png')
    role_id = Column(ForeignKey(Role.id), nullable=False, default=1)
    order = relationship('Order', cascade=relationship_config)


    @staticmethod
    async def create(data: dict) -> Optional['User']:
        async def op(session: AsyncSession):
            return await create(session, User(**data))
        return await operation_session(op)
    

    @staticmethod
    async def all() -> List['User']:
        async def op(session: AsyncSession):
            result = await session.execute(select(User))
            return result.scalars().all()
        return await operation_session(op)

    @staticmethod
    async def by_id(id: int) -> Optional['User']:
        async def op(session: AsyncSession):
            result = await session.execute(select(User).where(User.id == id))
            return result.scalar_one_or_none()
        return await operation_session(op)
    

    @staticmethod
    async def by_username(username: str) -> Optional['User']:
        async def op(session: AsyncSession):
            result = await session.execute(select(User).where(User.username == username))
            return result.scalar_one_or_none()
        return await operation_session(op)
    
    
    @staticmethod 
    async def update(id: int, data: dict) -> Optional['User']:
        async def op(session: AsyncSession):
            await session.execute(update(User).values(**data).where(User.id == id))
            await session.commit()
            return await User.by_id(id) 
        return await operation_session(op)
    
    @staticmethod
    async def delete(id: int) -> Optional[bool]:
        async def op(session: AsyncSession):
            result = await User.by_id(id)
            return await delete(session, result)
        return await operation_session(op)
# ПОТОМ ДОПИШУ ФУНКЦИОНАЛ ПОД ЮЗЕРА СЕЙЧАС ПОКА ВАЖНЕЕ ДРУГОЕ 
    
class OrderStatus(Base):
    __tablename__ = 'OrderStatus'
    id = Column(Integer, primary_key=True, autoincrement=True)
    status_name = Column(String(255), nullable=False, unique=True)
    order = relationship('Order', cascade=relationship_config)

    @staticmethod
    async def create(status_name: str) -> Optional['OrderStatus']:
        async def op(session: AsyncSession):
            return await create(session, OrderStatus(status_name=status_name))
        return await operation_session(op)

    @staticmethod
    async def all() -> List['OrderStatus']:
        async def op(session: AsyncSession):
            result = await session.execute(select(OrderStatus))
            return result.scalars().all()
        return await operation_session(op)
    
    @staticmethod
    async def update(id: int, status_name: str) -> Optional['OrderStatus']:
        async def op(session: AsyncSession):
            await session.execute(update(OrderStatus).
                                  values(status_name=status_name).
                                  where(OrderStatus.id == id))
            await session.commit()
            result = await Category.by_id(id)
            return result
        return await operation_session(op)
    
    @staticmethod
    async def by_id(id: int) -> Optional['OrderStatus']:
        async def op(session: AsyncSession):
            result = await session.execute(select(OrderStatus).where(OrderStatus.id == id))
            return result.scalar_one_or_none()
        return await operation_session(op)
    

class Order(Base):
    __tablename__ = 'Order'
    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(ForeignKey(Item.id), nullable=False)
    user_id = Column(ForeignKey(User.id), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unique_key = Column(String(255), nullable=False)
    data_order = Column(DateTime, default=datetime.now)
    order_status = Column(ForeignKey(OrderStatus.id), default=1, nullable=False)

    @staticmethod
    async def create(data: dict) -> Optional['Order']:
        async def op(session: AsyncSession):
            return await create(session, Order(**data))
        return await operation_session(op)


    @staticmethod
    async def all() -> List['Order']:
        async def op(session: AsyncSession):
            result = await session.execute(select(Order.unique_key).distinct())
            return result.scalars().all()
        return await operation_session(op)

    

    @staticmethod
    async def by_id(id: int) -> Optional['Order']:
        async def op(session: AsyncSession):
            result = await session.execute(select(Order).where(Order.id == id))
            return result.scalar_one_or_none()
        return await operation_session(op)


    @staticmethod
    async def delete(id: int) -> Optional[bool]:
        async def op(session: AsyncSession):
            result = await Order.by_id(id)
            return await delete(session, result)
        return await operation_session(op)


    @staticmethod
    async def unique_key_by_user(user_id: int):
        async def op(session: AsyncSession):
            orders = await session.execute(select(Order.unique_key).where(Order.user_id == user_id).distinct())
            return orders.scalars().all()
        return await operation_session(op)

    @staticmethod
    async def by_unique_key(unique_key: str) -> List['Order']:
        async def op(session: AsyncSession):
            order = await session.execute(select(Order).where(Order.unique_key == unique_key))
            return order.scalars().all()
        return await operation_session(op)

    @staticmethod
    async def update_status_by_unique_key(unique_key: str, order_status: int):
        async def op(session: AsyncSession):
            await session.execute(update(Order).values(order_status=order_status).where(Order.unique_key == unique_key))
            await session.commit()
            return True
        return await operation_session(op)


