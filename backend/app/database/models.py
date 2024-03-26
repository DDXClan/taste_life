from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, select, update
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime
from database.connection import operation_session
from util import delete, create
# 

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
    async def update(id: int, category_name: str) -> Optional['Category'] | None:
        async def op(session: AsyncSession):
            await session.execute(update(Category).
                                  values(category_name=category_name).
                                  where(Category.id == id))
            await session.commit()
            result = await Category.by_id(id)
            return result
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
    oreder_item = relationship('OrderItem', cascade=relationship_config)

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
            result = await Item.by_id(id)
            return result
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

    @staticmethod
    async def create(data: dict) -> Optional['User']:
        async def op(session: AsyncSession):
            return await create(session, User(**data))
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
# ПОТОМ ДОПИШУ ФУНКЦИОНАЛ ПОД ЮЗЕРА СЕЙЧАС ПОКА ВАЖНЕЕ ДРУГОЕ 
    

class OrderItem(Base):
    __tablename__ = 'OrderItem'
    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(ForeignKey(Item.id), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    user_order = relationship('UserOrder', cascade=relationship_config)


    @staticmethod
    async def create(data: dict) -> Optional['OrderItem']:
        async def op(session: AsyncSession):
            return await create(session, OrderItem(**data))
        return await operation_session(op)


    @staticmethod
    async def all() -> List['OrderItem']:
        async def op(session: AsyncSession):
            result = await session.execute(select(OrderItem))
            return result.scalars().all()
        return await operation_session(op)
    

    @staticmethod
    async def by_id(id: int) -> Optional['OrderItem']:
        async def op(session: AsyncSession):
            result = await session.execute(select(OrderItem).where(OrderItem.id == id))
            return result.scalar_one_or_none()
        return await operation_session(op)


    @staticmethod
    async def delete(id: int) -> Optional[bool]:
        async def op(session: AsyncSession):
            result = await OrderItem.by_id(id)
            return await delete(session, result)
        return await operation_session(op)


class OrderStatus(Base):
    __tablename__ = 'OrderStatus'
    id = Column(Integer, primary_key=True, autoincrement=True)
    status_name = Column(String(255), nullable=False, unique=True)
    user_order = relationship('UserOrder', cascade=relationship_config)


    @staticmethod
    async def create(status_name: str) -> Optional['OrderStatus']:
        async def op(session: AsyncSession):
            return await create(session, OrderItem(status_name=status_name))
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
    

class UserOrder(Base):
    __tablename__ = 'UserOrder'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(ForeignKey(User.id), nullable=False)
    order_id = Column(ForeignKey(OrderItem.id), nullable=False)
    date_order = Column(DateTime, nullable=False, default=datetime.now)
    order_status = Column(ForeignKey(OrderStatus.id), nullable=False, default=1)

    @staticmethod
    async def create(data: dict) -> Optional['UserOrder']:
        async def op(session: AsyncSession):
            return await create(session, OrderItem(**data))
        return await operation_session(op)
    
    @staticmethod
    async def all() -> List['UserOrder']:
        async def op(session: AsyncSession):
            result = await session.execute(select(UserOrder))
            return result.scalars().all()
        return await operation_session(op)
    
    @staticmethod
    async def by_id(id: int) -> Optional['UserOrder']:
        async def op(session: AsyncSession):
            result = await session.execute(select(UserOrder).where(UserOrder.id == id))
            return result.scalars().all()
        return await operation_session(op)
    
    @staticmethod
    async def delete(id: int) -> Optional[bool]:
        async def op(session: AsyncSession):
            result = await UserOrder.by_id(id)
            return await delete(session, result)
        return await operation_session(op)

    