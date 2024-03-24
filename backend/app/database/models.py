from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, select, update
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from database.connection import operation_session
from util import delete


Base = declarative_base()

relationship_config = 'all, delete'


class Category(Base):
    __tablename__ = 'Category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String, unique=True, nullable=False)
    item = relationship('Item', cascade=relationship_config)


    @staticmethod
    async def create(category_name: str):
        async def op(session: AsyncSession):
            category = Category(category_name=category_name)
            session.add(category)
            await session.commit()
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
    item_name = Column(String, unique=True, nullable=False)
    item_img = Column(String, default='placeholder.png')
    wt = Column(Integer, nullable=False, default=0)
    description = Column(String, nullable=False)
    price = Column(Integer, default=0)
    category_id = Column(ForeignKey(Category.id), nullable=False)


    @staticmethod
    async def create(data: dict):
        async def op(session: AsyncSession):
            item = Item(**data)
            session.add(item)
            await session.commit()
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
            item = await session.execute(select(Item).where(Item.id == id))
            return item.scalar_one_or_none()
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
    role_name = Column(String, nullable=False, unique=True)
    user = relationship('User', cascade=relationship_config)


    @staticmethod
    async def create(role_name: str) -> Optional['Role']:
        async def op(session: AsyncSession):
            role = Role(role_name=role_name)
            session.add(role)
            await session.commit()
            return role
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
            role = await session.execute(select(Role).where(Role.id == id))
            return role.scalar_one_or_none()
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
    username = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    user_img = Column(String, default='placeholder.png')
    role_id = Column(ForeignKey(Role.id), nullable=False, default=1)

    @staticmethod
    async def create(data: dict) -> Optional['User']:
        async def op(session: AsyncSession):
            user = User(**data)
            session.add(user)
            await session.commit()
            return user
        return await operation_session(op)
    

    @staticmethod
    async def by_id(id: int) -> Optional['User']:
        async def op(session: AsyncSession):
            user = await session.execute(select(User).where(User.id == id))
            return user.scalar_one_or_none()
        return await operation_session(op)
    
    @staticmethod
    async def by_username(username: str) -> Optional['User']:
        async def op(session: AsyncSession):
            user = await session.execute(select(User).where(User.username == username))
            return user.scalar_one_or_none()
        return await operation_session(op)