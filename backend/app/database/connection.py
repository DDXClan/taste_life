from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from redis import asyncio as aioredis
async_engine = create_async_engine('sqlite+aiosqlite:///backend.db')

"""
    С БД Я ПОКА ЧТО ПРОСТО ИГРАЮСЬ ПОТОМ ПОМЕНЯЮ ЕЕ НА ДРУГУЮ
"""

async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

async def operation_session(op):
    try:
        async with async_session() as session: 
            result = await op(session)
            return result
    except Exception:
        return None
    
redis = aioredis.from_url('redis://localhost')


